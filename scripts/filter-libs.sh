#!/usr/bin/env bash
# Filter lib-table.csv down to packages that ship Android native code.
# Output: libs.txt (one package per line). Cache: libs-skipped.txt.
# Usage: scripts/filter-libs.sh            # CSV=other.csv MIN_USAGE=0.01 to override
set -u
cd "$(dirname "$0")/.."

CSV="${CSV:-lib-table.csv}"
MIN_USAGE="${MIN_USAGE:-0.01}"
OUT=libs.txt
SKIPPED=libs-skipped.txt
touch "$OUT" "$SKIPPED"

# Packages already in package.json are part of the baseline build.
installed=$(node -p 'Object.keys(require("./package.json").dependencies||{}).join("\n")')

# Skip header, drop malformed rows (NF != 2), strip quotes/whitespace, apply threshold.
awk -F, -v min="$MIN_USAGE" 'NR>1 && NF==2 { gsub(/["[:space:]]/, "", $1); if ($1 != "" && $2+0 >= min) print $1 }' "$CSV" |
while read -r pkg <&3; do
  grep -qxF "$pkg" "$OUT" "$SKIPPED" && continue
  grep -qxF "$pkg" <<<"$installed" && { echo "skip (in package.json): $pkg" >&2; continue; }

  url=$(npm view "$pkg" dist.tarball 2>/dev/null)
  if [ -z "$url" ]; then
    echo "skip (npm view failed): $pkg" >&2
    echo "$pkg" >>"$SKIPPED"
    continue
  fi
  # ponytail: one tarball download per package, sequential. Parallelize with xargs -P if too slow.
  if curl -sL "$url" | tar -tzf - 2>/dev/null | grep -qE 'android/build\.gradle(\.kts)?$'; then
    echo "keep: $pkg" >&2
    echo "$pkg" >>"$OUT"
  else
    echo "skip (no android/build.gradle): $pkg" >&2
    echo "$pkg" >>"$SKIPPED"
  fi
done 3<&0

echo "kept $(wc -l <"$OUT" | tr -d ' ') packages in $OUT" >&2
