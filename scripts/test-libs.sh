#!/usr/bin/env bash
# Build the app once per package in libs.txt with AGP 9 newDsl + builtInKotlin enabled.
# Writes results.csv and logs/<pkg>.log, and commits after every package. Resumable.
# Usage: scripts/test-libs.sh            # LIBS=other.txt to override
set -u
cd "$(dirname "$0")/.."

LIBS="${LIBS:-libs.txt}"
RESULTS=results.csv
TASK=:app:assembleDebug
COMMON_FLAGS=(-PreactNativeArchitectures=arm64-v8a --console=plain)
NEW_DSL_FLAGS=(-Pandroid.newDsl=true -Pandroid.builtInKotlin=true)
mkdir -p logs
[ -f "$RESULTS" ] || echo "package,version,status" >"$RESULTS"

# Gradle's artifact transform cache grows by roughly 50MB per library build and is
# never pruned. A long run fills the disk, and once writes start failing every
# build fails for a reason that has nothing to do with the DSL. Prune before a
# build rather than during one, and stop the daemons first so nothing is holding
# the files being deleted.
ensure_disk() {
  local avail
  avail=$(df -g / | awk 'NR==2{print $4}')
  [ "$avail" -ge "${MIN_FREE_GB:-8}" ] && return 0
  echo "== ${avail}G free, below ${MIN_FREE_GB:-8}G: pruning Gradle transforms" >&2
  (cd android && ./gradlew --stop) >/dev/null 2>&1 || true
  pkill -f GradleDaemon >/dev/null 2>&1 || true
  sleep 2
  rm -rf "$HOME"/.gradle/caches/*/transforms "$HOME"/.gradle/daemon
  echo "== $(df -g / | awk 'NR==2{print $4}')G free after prune" >&2
}

gradle() { ensure_disk; rm -rf android/app/.cxx; (cd android && ./gradlew "$TASK" "$@"); }

echo "== baseline build with new DSL"
if ! gradle "${COMMON_FLAGS[@]}" "${NEW_DSL_FLAGS[@]}" >logs/_baseline.log 2>&1; then
  echo "baseline build failed, see logs/_baseline.log" >&2
  exit 1
fi

# ponytail: no per-build timeout; macOS lacks `timeout`. Wrap gradle in gtimeout if a build hangs.
while read -r pkg <&3; do
  [ -z "$pkg" ] && continue
  grep -q "^$pkg," "$RESULTS" && continue
  log="logs/${pkg//\//__}.log"
  echo "== $pkg"

  if ! npx expo install "$pkg" >"$log" 2>&1; then
    status=install-failed
    version=
  else
    version=$(node -p "require('$pkg/package.json').version" 2>/dev/null)
    if gradle "${COMMON_FLAGS[@]}" "${NEW_DSL_FLAGS[@]}" >>"$log" 2>&1; then
      status=pass
    elif { echo "== retry without new DSL flags"; gradle "${COMMON_FLAGS[@]}"; } >>"$log" 2>&1; then
      status=fail-newdsl
    else
      status=fail-baseline
    fi
    yarn remove "$pkg" >>"$log" 2>&1
  fi
  git checkout -q -- package.json yarn.lock app.json

  echo "$pkg,$version,$status" >>"$RESULTS"
  echo "   -> $status"
  git add "$RESULTS" logs
  git commit -q -m "test($pkg): $status"
done 3<"$LIBS"

echo "done. summary:"
cut -d, -f3 "$RESULTS" | tail -n +2 | sort | uniq -c
