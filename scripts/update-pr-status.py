#!/usr/bin/env python3
"""Refresh upstream-prs.md from the live state of every pull request.

`upstream-prs.tsv` is the source of truth for which PRs exist. This reads it,
asks GitHub for the current state of each, and rewrites upstream-prs.md grouped
so the pending ones are easy to scan.

Usage:
  scripts/update-pr-status.py            # rewrite upstream-prs.md
  scripts/update-pr-status.py --check    # print the summary, do not write

Requires an authenticated `gh`.
"""
import concurrent.futures as cf
import csv
import json
import os
import re
import subprocess
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TSV = os.path.join(ROOT, "upstream-prs.tsv")
OUT = os.path.join(ROOT, "upstream-prs.md")
PR_RE = re.compile(r"https://github\.com/([^/]+/[^/]+)/pull/(\d+)")


def usage_map():
    u = {}
    path = os.path.join(ROOT, "lib-table.csv")
    if not os.path.exists(path):
        return u
    with open(path, newline="") as fh:
        for i, row in enumerate(csv.reader(fh)):
            if i and len(row) == 2:
                try:
                    u[row[0].strip().strip('"').strip()] = float(row[1])
                except ValueError:
                    pass
    return u


def fetch(rec):
    m = PR_RE.match(rec["url"])
    if not m:
        rec["state"] = "unknown"
        return rec
    repo, num = m.group(1), m.group(2)
    p = subprocess.run(
        ["gh", "api", f"repos/{repo}/pulls/{num}", "--jq",
         '[.state,(.merged|tostring),(.merged_at//"-"),(.comments|tostring),'
         '(.review_comments|tostring),(.additions|tostring),(.changed_files|tostring)]'
         '|join("|")'],
        capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if p.returncode != 0 or not p.stdout.strip():
        rec["state"] = "unreachable"
        return rec
    st, merged, at, comments, rcomments, adds, files = p.stdout.strip().split("|")
    rec["repo"] = repo
    rec["number"] = num
    rec["merged_at"] = at[:10] if at != "-" else ""
    rec["additions"] = adds
    rec["changed_files"] = files
    rec["discussion"] = int(comments) + int(rcomments)
    rec["state"] = "merged" if merged == "true" else st
    return rec


def main():
    usage = usage_map()
    recs = []
    with open(TSV) as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            row["pkgs"] = [p for p in row["packages"].split(",") if p]
            row["usage"] = max((usage.get(p, 0) for p in row["pkgs"]), default=0)
            recs.append(row)

    with cf.ThreadPoolExecutor(max_workers=10) as ex:
        recs = list(ex.map(fetch, recs))

    counts = Counter(r["state"] for r in recs)
    order = {"open": 0, "merged": 1, "closed": 2, "unreachable": 3, "unknown": 4}
    recs.sort(key=lambda r: (order.get(r["state"], 9), -r["usage"], r["url"]))

    def table(rows, show_merged=False):
        head = "| Package(s) | Usage | Round | Files | PR |"
        sep = "|---|---|---|---|---|"
        head += (" Merged |" if show_merged else " Discussion |") + " Note |"
        sep += "---|---|"
        out = [head, sep]
        for r in rows:
            pk = ", ".join(f"`{p}`" for p in r["pkgs"])
            last = r.get("merged_at", "") if show_merged else (
                str(r.get("discussion", 0)) if r.get("discussion") else "")
            out.append(f"| {pk} | {r['usage']:g} | {r['round']} | {r['files']} | "
                       f"{r['url']} | {last} | {r.get('note','')} |")
        return out

    L = []
    L.append("# Upstream AGP 9 pull requests")
    L.append("")
    L.append("Every pull request filed from this harness, with live state.")
    L.append("Regenerate with `scripts/update-pr-status.py`; the list of PRs itself lives")
    L.append("in `upstream-prs.tsv`.")
    L.append("")
    L.append("The bug is one thing: a library that applies `kotlin-android` or")
    L.append("`org.jetbrains.kotlin.android` unconditionally collides with the `kotlin`")
    L.append("extension AGP 9 registers itself. Two guard shapes appear. Round 1 derived the")
    L.append("answer from the AGP major version and the `android.builtInKotlin` property.")
    L.append("Round 2 checks for the registered extension directly, which needs no version")
    L.append("table and covers AGP 10, where the opt-out is removed:")
    L.append("")
    L.append("```groovy")
    L.append("if (project.extensions.findByName('kotlin') == null) {")
    L.append("    apply plugin: 'kotlin-android'")
    L.append("}")
    L.append("```")
    L.append("")
    L.append("| State | Count |")
    L.append("|---|---|")
    for k in ("open", "merged", "closed", "unreachable", "unknown"):
        if counts.get(k):
            L.append(f"| {k} | {counts[k]} |")
    L.append(f"| **total** | **{len(recs)}** |")
    L.append("")
    pkgs = {p for r in recs for p in r["pkgs"]}
    L.append(f"{len(recs)} pull requests covering {len(pkgs)} packages.")
    L.append("")

    pending = [r for r in recs if r["state"] == "open"]
    if pending:
        L.append(f"## Pending ({len(pending)})")
        L.append("")
        L.append("Waiting on maintainers. `Discussion` is the number of comments and review")
        L.append("comments, so a non-zero value is worth a look.")
        L.append("")
        L += table(pending)
        L.append("")

    merged = [r for r in recs if r["state"] == "merged"]
    if merged:
        L.append(f"## Merged ({len(merged)})")
        L.append("")
        L += table(merged, show_merged=True)
        L.append("")

    closed = [r for r in recs if r["state"] == "closed"]
    if closed:
        L.append(f"## Closed without merging ({len(closed)})")
        L.append("")
        L.append("Check each one: so far every closure has been a maintainer taking the change")
        L.append("through their own process rather than rejecting it.")
        L.append("")
        L += table(closed)
        L.append("")

    other = [r for r in recs if r["state"] in ("unreachable", "unknown")]
    if other:
        L.append(f"## Could not read ({len(other)})")
        L.append("")
        L += table(other)
        L.append("")

    text = "\n".join(L) + "\n"
    if "--check" in sys.argv:
        print(dict(counts))
        print(f"{len(recs)} PRs, {len(pkgs)} packages (not written)")
        return
    open(OUT, "w").write(text)
    print(dict(counts))
    print(f"wrote {os.path.basename(OUT)}: {len(recs)} PRs, {len(pkgs)} packages")


if __name__ == "__main__":
    main()
