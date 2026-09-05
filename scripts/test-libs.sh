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
# Default high enough to be safe on its own. A run that relies on MIN_FREE_GB
# being exported is a run that silently loses the guard if it is not.
ensure_disk() {
  local avail min
  min="${MIN_FREE_GB:-12}"
  avail=$(df -g / | awk 'NR==2{print $4}')
  [ "$avail" -ge "$min" ] && return 0
  echo "== ${avail}G free, below ${min}G: pruning Gradle transforms" >&2
  (cd android && ./gradlew --stop) >/dev/null 2>&1 || true
  pkill -f GradleDaemon >/dev/null 2>&1 || true
  sleep 2
  rm -rf "$HOME"/.gradle/caches/*/transforms "$HOME"/.gradle/daemon
  echo "== $(df -g / | awk 'NR==2{print $4}')G free after prune" >&2
}

# Every external step gets a deadline. `realm` hung inside `npx expo install` for
# 19 hours: its `yarn add` finished in 6 seconds but the expo CLI wrapper never
# exited, no build was ever started, and the run sat there. A stalled run looks
# exactly like a working one from the outside, so the timeout is the only thing
# that turns a hang into a recorded result.
TIMEOUT=$(command -v gtimeout || command -v timeout)
TIMEOUT_INSTALL="${TIMEOUT_INSTALL:-900}"
TIMEOUT_BUILD="${TIMEOUT_BUILD:-2400}"

# Errors that mean the network went away, not that the package is broken.
net_error() { grep -qE "EHOSTUNREACH|ENOTFOUND|ETIMEDOUT|ECONNRESET|EAI_AGAIN|ENETDOWN|ENETUNREACH|socket hang up" "$1"; }

registry_up() { curl -sf -o /dev/null --max-time 15 https://registry.npmjs.org/react; }

wait_for_registry() {
  local waited=0
  until registry_up; do
    if [ "$waited" -ge "${NET_WAIT_MAX:-1800}" ]; then
      echo "== registry unreachable for ${waited}s, giving up" >&2
      return 1
    fi
    echo "== registry unreachable, waited ${waited}s" >&2
    sleep 60
    waited=$((waited + 60))
  done
  [ "$waited" -gt 0 ] && echo "== registry back after ${waited}s" >&2
  return 0
}

gradle() {
  ensure_disk
  rm -rf android/app/.cxx
  (cd android && "$TIMEOUT" "$TIMEOUT_BUILD" ./gradlew "$TASK" "$@")
  local rc=$?
  [ "$rc" -eq 124 ] && echo "== gradle build exceeded ${TIMEOUT_BUILD}s and was killed" >&2
  return "$rc"
}

echo "== baseline build with new DSL"
if ! gradle "${COMMON_FLAGS[@]}" "${NEW_DSL_FLAGS[@]}" >logs/_baseline.log 2>&1; then
  echo "baseline build failed, see logs/_baseline.log" >&2
  exit 1
fi

while read -r pkg <&3; do
  [ -z "$pkg" ] && continue
  grep -q "^$pkg," "$RESULTS" && continue
  log="logs/${pkg//\//__}.log"
  echo "== $pkg"

  "$TIMEOUT" "$TIMEOUT_INSTALL" npx expo install "$pkg" >"$log" 2>&1
  install_rc=$?

  # A dropped network records every remaining package as install-failed, which is
  # indistinguishable from a package that genuinely will not install. One outage
  # poisoned 306 consecutive rows before this existed. On a network-shaped error,
  # wait for the registry, retry once, and abort the run rather than record a
  # verdict the network produced. The run is resumable, so aborting costs nothing.
  if [ "$install_rc" -ne 0 ] && [ "$install_rc" -ne 124 ] && net_error "$log"; then
    echo "   network error during install, checking connectivity" >&2
    if wait_for_registry; then
      "$TIMEOUT" "$TIMEOUT_INSTALL" npx expo install "$pkg" >"$log" 2>&1
      install_rc=$?
    fi
    if [ "$install_rc" -ne 0 ] && net_error "$log"; then
      echo "registry still unreachable after retry; stopping so results stay clean" >&2
      git checkout -q -- package.json yarn.lock app.json
      rm -f "$log"
      exit 1
    fi
  fi

  if [ "$install_rc" -eq 124 ]; then
    echo "== npx expo install exceeded ${TIMEOUT_INSTALL}s and was killed" >>"$log"
    status=timeout
    version=
    pkill -f "expo install $pkg" >/dev/null 2>&1 || true
  elif [ "$install_rc" -ne 0 ]; then
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
  # Some packages copy native assets into the app source tree (llama.rn drops
  # 2.8MB of ggml-hexagon into android/app/src/main/assets). Those are untracked
  # and would otherwise persist into every later build in the run.
  git clean -qfd android/app/src/main

  echo "$pkg,$version,$status" >>"$RESULTS"
  echo "   -> $status"
  git add "$RESULTS" logs
  git commit -q -m "test($pkg): $status"
done 3<"$LIBS"

echo "done. summary:"
cut -d, -f3 "$RESULTS" | tail -n +2 | sort | uniq -c
