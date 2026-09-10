# Did the merged fixes actually work?

Merged, released and fixed are three different things. This checks all three for
every merged pull request, by **building** each published package rather than
reading its gradle file.

Re-run with `RESULTS=verify-released.csv LIBS=<list> scripts/test-libs.sh`.

## Latest run: 2026-09-10, all 56 shipped packages

76 pull requests are merged. 56 of the packages they cover have the fix
published on npm; 36 are merged but unreleased.

| Result | Count |
|---|---|
| **pass** | **37** |
| fail-baseline | 12 |
| fail-newdsl | 7 |
| **total built** | **56** |

**37 of 56 build clean under AGP 9.** The 19 that do not almost all fail on
something the collision was previously hiding:

| Cause | Count | Highest usage |
|---|---|---|
| Kotlin compile error | 7 | `react-native-iap` 0.02, `@maplibre/maplibre-react-native` 0.017 |
| Missing sibling project | 4 | the nitro packages; needs a peer installed, a harness gap not an AGP one |
| `kotlinOptions()` removed | 3 | `@lodev09/react-native-true-sheet` 0.012 |
| Collision still present | 2 | `@react-native-community/datetimepicker` 0.288 |
| dependency resolution / javac / other | 3 | low usage |

## The two that still collide are not regressions

`@react-native-community/datetimepicker` is the important one, at 0.288 the
highest-usage package in the whole set.

- The fix **is** shipped in 9.2.1, and the guard is present in the published
  tarball.
- `npx expo install` pinned **9.1.0**, because that is the version matched to the
  Expo SDK. So the first run tested a pre-fix version and reported a collision
  that no longer exists.
- Re-tested at 9.2.1 explicitly: the collision is gone, and it now fails with
  `Could not find method kotlinOptions()`.

So it needs a second pull request, not a re-run. `@criipto/verify-expo` is the
same shape: its published version predates the merge.

This is a limitation of the harness worth remembering: `expo install` resolves to
the SDK-matched version, so verifying a fix sometimes means installing the exact
version by hand. Only 1 of 56 was affected here, but it was the one that mattered
most.

## What this says overall

The guard works. Across 56 shipped packages the collision survives in exactly two
places, and in both the published version simply predates the merge. What remains
is the second wave: `kotlinOptions()` and compile errors that were unreachable
while configuration failed at plugin application.
