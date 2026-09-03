#!/usr/bin/env python3
"""Classify every package in lib-table.csv as shipping Android native code or not.

Unlike scripts/filter-libs.sh, which downloads one tarball per package, this reads
the published file list from the jsDelivr data API. That is cheap enough to run
over the whole 108k-row table instead of only the usage >= 0.01 slice.

Verified against the 345 packages filter-libs.sh had already classified:
344 agreed, 0 disagreed, 1 was a transient jsDelivr 403.

Output:
  libs-scan.tsv                    package<TAB>verdict<TAB>detail  (cache, resumable)
  libs-android.txt                 ships a buildable Android native module
  libs-android-example-only.txt    only has android/build.gradle under an
                                   example or test app, so nothing a consumer builds

verdict is one of: android, no-android, unresolved

Usage:
  scripts/scan-libs.py                 # full table, resumable
  MIN_USAGE=0.01 scripts/scan-libs.py  # restrict by usage
  WORKERS=12 scripts/scan-libs.py
"""
import concurrent.futures as cf
import csv
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, os.environ.get("CSV", "lib-table.csv"))
CACHE = os.path.join(ROOT, "libs-scan.tsv")
OUT = os.path.join(ROOT, "libs-android.txt")
EXAMPLE_OUT = os.path.join(ROOT, "libs-android-example-only.txt")
MIN_USAGE = float(os.environ.get("MIN_USAGE", "0"))
WORKERS = int(os.environ.get("WORKERS", "12"))

UA = {"User-Agent": "agp-new-dsl-filter (+https://github.com/gabrieldonadel/agp-new-dsl)"}
GRADLE = ("android/build.gradle", "android/build.gradle.kts")

_lock = threading.Lock()
_done = 0
_t0 = time.time()

# Directories whose gradle files belong to a demo or test app, not to the
# published native module. A package whose only match is under one of these
# does not ship Android code a consumer can build against.
NON_MODULE_DIRS = ("example", "examples", "demo", "demos", "template", "templates",
                   "test", "tests", "__tests__", "fixture", "fixtures", "e2e",
                   "sample", "samples", "playground", "apps")


def is_module_path(path):
    parts = [p for p in path.strip("/").split("/") if p]
    return not any(p.lower() in NON_MODULE_DIRS for p in parts[:-2])


def fetch(url, accept=None, timeout=25, tries=3):
    """GET with retries. Returns (status, body). status -1 means transport error."""
    for attempt in range(tries):
        req = urllib.request.Request(url, headers=dict(UA))
        if accept:
            req.add_header("Accept", accept)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            # 404 is a real answer; don't retry it. Back off on throttling/5xx.
            if e.code == 404:
                return 404, b""
            if attempt == tries - 1:
                return e.code, b""
            time.sleep(2 * (attempt + 1))
        except Exception:
            if attempt == tries - 1:
                return -1, b""
            time.sleep(2 * (attempt + 1))
    return -1, b""


def classify(pkg):
    q = urllib.parse.quote(pkg, safe="@/")
    status, body = fetch(f"https://registry.npmjs.org/{q}",
                         "application/vnd.npm.install-v1+json")
    if status == 404:
        return pkg, "unresolved", "not published on npm"
    if status != 200:
        return pkg, "unresolved", f"registry {status}"
    try:
        ver = json.loads(body)["dist-tags"]["latest"]
    except Exception:
        return pkg, "unresolved", "no latest dist-tag"

    status, body = fetch(f"https://data.jsdelivr.com/v1/package/npm/{q}@{ver}/flat")
    if status != 200:
        return pkg, "unresolved", f"jsdelivr {status} (v{ver})"
    try:
        files = [f["name"] for f in json.loads(body).get("files", [])]
    except Exception:
        return pkg, "unresolved", f"bad jsdelivr payload (v{ver})"

    hits = sorted(f for f in files if f.endswith(GRADLE))
    if hits:
        # Record every match, not just the first. A gradle file that only exists
        # under an example or template app is not a shippable native module, and
        # that distinction is only visible if all paths are kept.
        return pkg, "android", f"v{ver} {' '.join(hits[:6])}"
    return pkg, "no-android", f"v{ver} {len(files)} files"


# A legal npm name, optionally scoped. lib-table.csv also contains junk that is
# not a package name at all: "ngrok@^4.1.0", "react-native:7.2.0", "~utils", and
# one quoted cell holding four newline-separated names. Left unchecked, that cell
# writes multiple lines into the TSV cache and its trailing fragment collides
# with a real package's record.
NPM_NAME = re.compile(r"^(@[a-z0-9][a-z0-9._-]*/)?[a-z0-9][a-z0-9._-]*$", re.I)


def classify_via_tarball(pkg):
    """Fallback for packages jsDelivr refuses (it 403s on some, e.g. very large ones).

    Downloads the tarball and lists it, which is what filter-libs.sh always did.
    Only used for the handful the API cannot answer, so the cost stays bounded.
    """
    import subprocess
    try:
        url = subprocess.run(["npm", "view", pkg, "dist.tarball"], capture_output=True,
                             text=True, timeout=90, stdin=subprocess.DEVNULL).stdout.strip()
        if not url:
            return pkg, "unresolved", "npm view returned no tarball"
        ver = subprocess.run(["npm", "view", pkg, "version"], capture_output=True,
                             text=True, timeout=90, stdin=subprocess.DEVNULL).stdout.strip()
        tar = subprocess.run(f"curl -sL --max-time 300 {url!r} | tar -tzf -", shell=True,
                             capture_output=True, text=True, timeout=600).stdout
    except Exception as e:
        return pkg, "unresolved", f"tarball check failed: {type(e).__name__}"
    hits = sorted("/" + n.split("/", 1)[1] for n in tar.split("\n")
                  if n.endswith(GRADLE) and "/" in n)
    if hits:
        return pkg, "android", f"v{ver} {' '.join(hits[:6])}"
    return pkg, "no-android", f"v{ver} tarball-checked"


def load_targets():
    seen, out = set(), []
    skipped = 0
    with open(CSV_PATH, newline="") as fh:
        for i, row in enumerate(csv.reader(fh)):
            if i == 0 or len(row) != 2:
                continue
            name = row[0].strip().strip('"').strip()
            if not name:
                continue
            if len(name) > 214 or not NPM_NAME.match(name):
                skipped += 1
                continue
            try:
                usage = float(row[1])
            except ValueError:
                continue
            if usage < MIN_USAGE or name in seen:
                continue
            seen.add(name)
            out.append(name)
    if skipped:
        print(f"skipped {skipped} rows that are not legal npm names", file=sys.stderr)
    return out


def load_cache():
    done = {}
    if os.path.exists(CACHE):
        with open(CACHE) as fh:
            for line in fh:
                parts = line.rstrip("\n").split("\t")
                if len(parts) >= 2:
                    done[parts[0]] = parts[1]
    return done


def main():
    global _done
    targets = load_targets()
    done = load_cache()
    # retry anything previously unresolved for a transient reason, but not hard 404s
    pending = [p for p in targets
               if p not in done or (done[p] == "unresolved" and p in RETRY)]
    print(f"table: {len(targets)} distinct packages (MIN_USAGE={MIN_USAGE})", file=sys.stderr)
    print(f"cached: {len(done)}  pending: {len(pending)}  workers: {WORKERS}", file=sys.stderr)

    if "--tarball-fallback" in sys.argv:
        # Re-check only what the API could not answer, using the tarball.
        pending = sorted(FALLBACK)
        print(f"tarball fallback for {len(pending)} packages jsDelivr refused",
              file=sys.stderr)
        worker = classify_via_tarball
        workers = min(WORKERS, 6)
    else:
        worker = classify
        workers = WORKERS

    total = len(pending)
    if total:
        with open(CACHE, "a") as cache, \
                cf.ThreadPoolExecutor(max_workers=workers) as ex:
            for pkg, verdict, detail in ex.map(worker, pending):
                with _lock:
                    cache.write(f"{pkg}\t{verdict}\t{detail}\n")
                    _done += 1
                    if _done % 1000 == 0:
                        cache.flush()
                        rate = _done / max(time.time() - _t0, 1e-9)
                        eta = (total - _done) / rate / 60 if rate else 0
                        print(f"  {_done}/{total}  {rate:.0f}/s  eta {eta:.0f}m",
                              file=sys.stderr, flush=True)

    # rebuild outputs from the cache; a package may appear twice if it was retried,
    # so keep the last verdict written for it
    # A definitive verdict always beats "unresolved" for the same package, so a
    # stray corrupt record cannot demote a package that actually resolved.
    latest = {}
    with open(CACHE) as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            pkg, verdict, detail = parts[0], parts[1], parts[2]
            prev = latest.get(pkg)
            if prev and prev[0] != "unresolved" and verdict == "unresolved":
                continue
            latest[pkg] = (verdict, detail)
    counts = {}
    for verdict, _ in latest.values():
        counts[verdict] = counts.get(verdict, 0) + 1

    android, example_only = [], []
    for pkg, (verdict, detail) in latest.items():
        if verdict != "android":
            continue
        paths = [t for t in detail.split(" ") if t.startswith("/")]
        if any(is_module_path(p) for p in paths):
            android.append(pkg)
        else:
            example_only.append(pkg)
    android.sort()
    example_only.sort()
    with open(OUT, "w") as fh:
        fh.write("\n".join(android) + ("\n" if android else ""))

    with open(EXAMPLE_OUT, "w") as fh:
        fh.write("\n".join(example_only) + ("\n" if example_only else ""))

    print("\nverdict counts:", file=sys.stderr)
    for k in sorted(counts):
        print(f"  {k:12} {counts[k]}", file=sys.stderr)
    print(f"\n  of the 'android' packages:", file=sys.stderr)
    print(f"    {len(android)} ship a native module -> {os.path.basename(OUT)}",
          file=sys.stderr)
    print(f"    {len(example_only)} match only under an example/test app -> "
          f"{os.path.basename(EXAMPLE_OUT)}", file=sys.stderr)


RETRY = set()      # populated by --retry-unresolved
FALLBACK = set()   # populated by --tarball-fallback


def _current_unresolved():
    """Packages whose latest verdict is unresolved, keyed by reason."""
    latest = {}
    if not os.path.exists(CACHE):
        return latest
    with open(CACHE) as fh:
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if len(p) < 3:
                continue
            prev = latest.get(p[0])
            if prev and prev[0] != "unresolved" and p[1] == "unresolved":
                continue
            latest[p[0]] = (p[1], p[2])
    return {k: v[1] for k, v in latest.items() if v[0] == "unresolved"}


if "--retry-unresolved" in sys.argv:
    RETRY = {k for k, reason in _current_unresolved().items()
             if reason != "not published on npm"}

if "--tarball-fallback" in sys.argv:
    FALLBACK = {k for k, reason in _current_unresolved().items()
                if reason.startswith("jsdelivr")}

if __name__ == "__main__":
    main()
