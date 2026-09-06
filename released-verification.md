# Did the merged fixes actually work?

Merged, released and fixed are three different things. This checks all three for
every merged pull request.

Method: for each merged PR, read the latest published version from npm, look for
the guard in the published tarball, and then **build the package** against the
AGP 9 flags rather than trusting the file contents.

## Release status of the 32 merged pull requests

| | Count |
|---|---|
| fix published on npm | 13 |
| merged but not released yet | 19 |
| gradle file not at the root path (needs a manual look) | 1 |

`react-native-purchases` (usage 0.136) is the notable unreleased one: the PR is
merged but the latest npm version predates the merge.

## Build result for the 13 published fixes

| Package | Version | Result |
|---|---|---|
| `@react-native-google-signin/google-signin` | 16.1.5 | pass |
| `@preeternal/react-native-cookie-manager` | 6.4.1 | pass |
| `react-native-volume-manager` | 2.2.0 | pass |
| `react-native-navigation-mode` | 1.2.13 | pass |
| `@dr.pogodin/react-native-fs` | 2.40.2 | pass |
| `react-native-restart-newarch` | 1.0.88 | pass |
| `react-native-screenshot-aware` | 2.1.3 | pass |
| `@alexzunik/react-native-money-input` | 0.5.4 | pass |
| `@maplibre/maplibre-react-native` | 11.3.9 | fail-newdsl |
| `@lodev09/react-native-true-sheet` | 3.11.13 | fail-newdsl |
| `@kesha-antonov/react-native-background-downloader` | 4.6.2 | fail-newdsl |
| `@bear-block/vision-camera-ocr` | 4.0.3 | fail-baseline |
| `@blazejkustra/react-native-alert` | 1.1.0 | fail-baseline |

**8 of 13 now build clean.** Raw results in `verify-released.csv`.

## The guard worked in all 13

`Cannot add extension with name 'kotlin'` appears in **zero** of the 13 logs. The
collision is gone everywhere the fix shipped, including in the five that still
fail. Those five now fail *later in the build* than before, on problems the
collision was previously hiding:

| Package | What it hits now |
|---|---|
| `@lodev09/react-native-true-sheet` | `Could not find method kotlinOptions()` — the DSL block is removed under built-in Kotlin |
| `@maplibre/maplibre-react-native` | Kotlin compile: unresolved `LocationEngine` |
| `@kesha-antonov/react-native-background-downloader` | Kotlin compile: unresolved `RNBackgroundDownloader…` |
| `@blazejkustra/react-native-alert` | Kotlin compile: `getCurrentActivity` invocation |
| `@bear-block/vision-camera-ocr` | Needs `react-native-vision-camera` installed alongside; a harness gap, not an AGP problem |

`kotlinOptions()` is the second wave predicted when the guard work started: every
one of the 269 collision packages failed at *plugin application*, the earliest
point in configuration, so nothing downstream had ever run. Now that
configuration completes, the next incompatibility surfaces. Per the
[Android migration guide](https://developer.android.com/build/migrate-to-built-in-kotlin),
`android.kotlinOptions{}` becomes `kotlin { compilerOptions { … } }`.

## What this means

The guard is doing exactly what it was meant to do, and it is not the whole
story. Expect a share of the 287 pull requests to unblock configuration and then
reveal a `kotlinOptions` or compile-time problem behind it. That is progress —
those problems were always there, just unreachable — but "merged" should not be
read as "this package now builds".

Re-run this check with `RESULTS=verify-released.csv LIBS=<list> scripts/test-libs.sh`.
