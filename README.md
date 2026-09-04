# AGP 9 new DSL compatibility runner

This repo is a test harness, not an app. It answers one question: which popular
React Native libraries build when the two AGP 9 defaults are turned on?

- `android.newDsl=true`
- `android.builtInKotlin=true`

The Expo SDK 58 template opts out of both in `android/gradle.properties`. This
harness leaves those files alone and passes the flags on the Gradle command line.

## Quick start

```bash
yarn install
scripts/filter-libs.sh   # optional, libs.txt is already committed
scripts/test-libs.sh     # builds each lib, commits after each one, resumable
```

Requirements: Java 17, Android SDK, yarn 1.x, network access. Do not push.
The scripts commit locally only.

## Files

| File | Purpose |
|---|---|
| `lib-table.csv` | Raw input. `Package,Usage`. 108142 rows: 3 do not have 2 fields and 37 more are not legal npm names. Do not edit. |
| `scripts/filter-libs.sh` | Cleans the CSV into `libs.txt`. Usage >= 0.01 only. |
| `libs.txt` | Packages to test, one per line. 157 entries. |
| `libs-skipped.txt` | Cache of packages the filter rejected. Delete a line to re-check it. |
| `scripts/scan-libs.py` | Classifies the whole CSV, not just the usage >= 0.01 slice. |
| `libs-scan.tsv` | `package<TAB>verdict<TAB>detail` for every row. Cache, resumable. |
| `libs-android.txt` | 3888 packages that ship a buildable Android native module. |
| `libs-android-example-only.txt` | 94 packages whose only `android/build.gradle` is in an example or test app. |
| `upstream-prs.md` | Every pull request filed from this harness, with live state. |
| `scripts/test-libs.sh` | Builds each package in `libs.txt` and records the result. |
| `results.csv` | `package,version,status`. One row per tested package. |
| `logs/<pkg>.log` | Full install and Gradle output per package. `/` in names becomes `__`. |
| `logs/_baseline.log` | Gradle output of the untouched app with the flags on. |

## How the filter works

`scripts/filter-libs.sh`:

1. Skips the CSV header and rows that do not have exactly 2 fields.
2. Strips quotes and whitespace from package names.
3. Keeps rows with usage >= 0.01 (override with `MIN_USAGE=`).
4. Skips packages already listed in `package.json`. They are part of the baseline.
5. Downloads each remaining tarball with `npm view` + `curl` and keeps the
   package only if it contains `android/build.gradle` or `android/build.gradle.kts`.

The script is resumable. It skips any package already in `libs.txt` or
`libs-skipped.txt`.

## Full table scan

`scripts/filter-libs.sh` defaults to `MIN_USAGE=0.01`, and only 362 of the
108k rows clear that. It processed everything above the threshold, which is why
`libs.txt` has 157 entries. `scripts/scan-libs.py` classifies the whole table
instead.

It cannot work the same way. One tarball download per package is fine for 362
packages and not for 108k. Instead it reads the published file list from the
jsDelivr data API: two small JSON requests per package, no tarball. That is
about 700x cheaper and runs in an hour.

The cheap check was validated against the 345 packages `filter-libs.sh` had
already classified: 344 agreed, 0 disagreed, 1 was a transient 403. For the
107 packages jsDelivr refuses outright, `--tarball-fallback` falls back to the
old tarball listing. That found 62 more Android packages the API could not see.

### Results

| Verdict | Count |
|---|---|
| ships an Android native module | **3888** |
| Android gradle only under an example or test app | 94 |
| no Android code | 27192 |
| unresolved | 76927 |
| **total classified** | **108101** |

37 rows are not legal npm names and are skipped: `ngrok@^4.1.0`,
`react-native:7.2.0`, `~utils`, `@/api` and similar. The unresolved rows are
fully accounted for: 76802 are not published on the public registry, and 125
have no `latest` dist-tag. None are transient failures.

Most of the table is private. Names like `@acme/reorder` and
`@member-portal/shared` are internal packages that only exist inside the app
that reported them.

### The 3888 by usage

| Usage | Count |
|---|---|
| >= 0.1 | 60 |
| >= 0.01 | 166 |
| >= 0.001 | 567 |
| == 0 | 3321 |

156 of the 157 packages in `libs.txt` are in `libs-android.txt`. The one
exception is `react-native-qrcode-svg`, and the new classifier is right to drop
it: its only gradle files live in `Example/android/`, so it ships no native
module. The old regex matched any path ending in `android/build.gradle`,
including example apps. That is the same reason the 94 example-only packages
are held separately rather than counted as native.

`scan-libs.py` records every matching gradle path, not just the first, because
a package can have both a real module and an example app. Deciding on one path
would misclassify those.

### Cost of testing them

The harness runs one Gradle build per package, 1 to 3 minutes each. 3888
packages is over 100 hours sequentially. Test a slice, not the whole set:
the 166 packages at usage >= 0.01 are about 6 hours and cover everything with
measurable adoption.

## How the test works

`scripts/test-libs.sh`:

1. Builds `:app:assembleDebug` on the untouched project with both flags.
   Aborts if this fails. Fix the baseline before testing libraries.
2. For each package in `libs.txt` that is not yet in `results.csv`:
   - `npx expo install <pkg>` so expo-* packages get the SDK-matched version.
   - Builds `:app:assembleDebug` with `-Pandroid.newDsl=true -Pandroid.builtInKotlin=true`.
   - On failure, builds once more without the two flags.
   - Records one of these statuses:

| Status | Meaning |
|---|---|
| `pass` | Builds with the flags on. |
| `fail-newdsl` | Fails with the flags on, builds with them off. This is the signal we want. |
| `fail-baseline` | Fails either way. Not a DSL problem. Often needs a config plugin or manual setup. |
| `install-failed` | `npx expo install` failed. |
| `timeout` | `npx expo install` ran past `TIMEOUT_INSTALL` and was killed. No build was attempted. |

3. Removes the package, restores `package.json` and `yarn.lock` from git.
4. Commits `results.csv` and `logs/` with message `test(<pkg>): <status>`.

The loop uses `set -u` without `set -e`. One broken library never stops the run.
Stop it any time. Restart it and it continues after the last committed package.

Builds use `-PreactNativeArchitectures=arm64-v8a` to save time.

## Baseline changes and why

The stock template did not build with the flags on. These changes were needed:

1. **Removed six template dependencies**: `react-native-reanimated`,
   `react-native-worklets`, `react-native-gesture-handler`, `react-native-screens`,
   `react-native-safe-area-context`, `expo-router`. The first five apply the
   standalone `org.jetbrains.kotlin.android` plugin. That plugin cannot be applied
   under `newDsl` at all. With `builtInKotlin=false` it fails with a
   `BaseExtension` cast error. With `builtInKotlin=true` it fails with
   "extension with name 'kotlin' already registered". `expo-router` depends on
   them. All six are now in `libs.txt` and get tested individually.
2. **Replaced the JS entry** with a minimal `index.js` and set `main` in
   `package.json`. The debug build does not bundle JS, but Gradle still needs an
   entry file to exist. The `src/` folder is dead code and is not under test.
3. **Removed the `expo-router` config plugin** from `app.json`. The
   `createExpoConfig` Gradle task fails if a plugin cannot be resolved.
4. **Made the app's Kotlin plugin conditional** in `android/app/build.gradle`.
   It applies `org.jetbrains.kotlin.android` only when `android.builtInKotlin`
   is false. This lets both the flagged build and the fallback build work.

See the git log for the exact commits.

## Findings so far

502 packages tested. `libs-top500.txt` is the 500 highest-usage entries
of `libs-android.txt` with `package.json` dependencies removed; the other 2 rows
are carried over from the original `libs.txt` run.

| Status | Count |
|---|---|
| `pass` | 196 |
| `fail-newdsl` | 152 |
| `fail-baseline` | 153 |
| `timeout` | 1 |
| **total** | **502** |

### What breaks under the new DSL (152)

Cause taken from the first `* What went wrong:` block of the flagged build,
before the fallback build runs.

| Cause | Count | Share |
|---|---|---|
| Kotlin plugin collides with AGP's built-in Kotlin | 144 | 95% |
| Removed DSL property (`libraryVariants`, `bootClasspath`) | 5 | 3% |
| Kotlin compile error | 1 | 1% |
| javac compile error | 1 | 1% |
| Other | 1 | 1% |

**One bug accounts for almost all of it.** AGP 9 registers the `kotlin` extension
itself, so a library that also applies `kotlin-android` or
`org.jetbrains.kotlin.android` unconditionally fails during configuration. AGP
reports it two ways, and both are the same problem:

```
Cannot add extension with name 'kotlin', as there is an extension already registered with that name.
The 'org.jetbrains.kotlin.android' plugin is no longer required for Kotlin support since AGP 9.0.
```

The fix is to apply the plugin only when AGP is not already providing Kotlin.
See "Upstream fixes" below for the two guard shapes in use.

The remainder are unrelated to the Kotlin plugin and each needs its own work:

- **Removed DSL property (`libraryVariants`, `bootClasspath`)**: `react-native-launch-arguments`, `react-native-onetrust-cmp`, `react-native-context-menu-view`, `react-native-create-thumbnail`, `react-native-worklets-core`
- **Kotlin compile error**: `@react-native-async-storage/async-storage`
- **javac compile error**: `react-native-keyboard-controller`
- **Other**: `expo-updates` fails inside `expo-autolinking`, on a null
  `KotlinJvmAndroidCompilation.getAndroidVariant()`.

The full per-package list is `results.csv`, with one log each under `logs/`.

### How far the upstream PRs go

144 packages hit the Kotlin plugin collision. Every one that can take a pull
request now has one. The breakdown accounts for all 144:

| | Count |
|---|---|
| covered by a pull request from this harness | 126 |
| already fixed upstream before we looked | 3 |
| carrying another contributor's pull request | 2 |
| no repository field on npm, or not hosted on GitHub | 4 |
| repository returns 404 | 2 |
| repository archived and read-only | 2 |
| no unconditional apply left upstream | 4 |
| declares the plugin in a `plugins {}` block | 1 |
| **total** | **144** |

The `plugins {}` case needs a different construction than a conditional `apply`,
so it is left for manual work rather than patched by pattern.

105 pull requests cover the 126 packages, because several repositories are
monorepos where one PR fixes many: `oblador/react-native-vector-icons` is 41
files across 13 packages, `THEOplayer/react-native-connectors` is 11 files, and
`infinitered/react-native-mlkit` is 5.

### `timeout` (1)

`realm` hung inside `npx expo install` and was killed at the 900s deadline, so
no build ran and it has no verdict. Worth a manual retry with a longer
`TIMEOUT_INSTALL`.

### `fail-baseline` (153)

Fails with the flags on and with them off, so the harness cannot attribute it to
the DSL. Not investigated. Note this understates new-DSL breakage: a package
whose flagged build dies on the Kotlin collision but whose fallback build also
fails, for a missing peer dependency or its own version assert, lands here
rather than in `fail-newdsl`. `react-native-reanimated`,
`react-native-worklets` and `react-native-safe-area-context` are exactly that
case. See the notes further down.

### Upstream fixes

The 144 collision cases are one bug with one fix: apply the Kotlin plugin only
when AGP is not already providing it. `react-native-screens` already does this,
which is why it passes.

**105 pull requests are filed, covering 126 packages across 105 repositories.**
The full list with live state is [`upstream-prs.md`](upstream-prs.md).

Round 1 (22 PRs) derived the answer from the AGP major version and the
`android.builtInKotlin` property. Round 2 (83 PRs) checks for the registered
extension directly, at the suggestion of the RevenueCat maintainer who merged it:

```groovy
if (project.extensions.findByName('kotlin') == null) {
    apply plugin: 'kotlin-android'
}
```

The second form is simpler, needs no version table, and covers AGP 10 where the
opt-out is removed. It is only correct if AGP has already registered its
extensions, so the Kotlin apply must come after `apply plugin:
'com.android.library'`. That ordering was checked in every file rather than
assumed. Both forms were verified in this harness against AGP 9.2.1:
`:app:assembleDebug` succeeds with both flags on and with both flags off.

#### Not filed

| Package | Reason |
|---|---|
| react-native-gesture-handler | Already guarded upstream. Tested 3.1.0, fix not yet released. |
| lottie-react-native | Already guarded upstream. |
| react-native-pager-view | Already guarded upstream. |
| react-native-webview | Open PR from another contributor. |
| react-native-maps | Open PR from another contributor. |
| posthog-react-native-session-replay | Repo is archived and read-only. Pull requests are rejected. |

A merged PR does not change `results.csv`. The rows there record the version that
was tested, and the fixes are not released yet.

### Notes on the six removed template dependencies

All six were tested individually. Results:

| Package | Version | Status |
|---|---|---|
| react-native-gesture-handler | 3.1.0 | fail-newdsl |
| react-native-screens | 4.27.0 | pass |
| expo-router | 58.0.0-canary-20260902-26df09e | pass |
| react-native-reanimated | 4.5.1 | fail-baseline |
| react-native-worklets | 0.10.1 | fail-baseline |
| react-native-safe-area-context | 5.7.0 | fail-baseline |

`react-native-screens` passes, as expected, because it guards the plugin
behind `shouldEnableAgpFallback()`.

Reanimated, worklets and safe-area-context land in `fail-baseline` rather
than `fail-newdsl`, but their flagged builds do fail on the `kotlin`
extension conflict. Their fallback builds fail for separate reasons, so the
two-build classification cannot call them. From `logs/`:

- `react-native-reanimated` fallback: `[Reanimated] react-native-worklets
  library not found. Please install it as a dependency in your project.`
- `react-native-worklets` fallback:
  `:react-native-worklets:assertMinimalReactNativeVersionTask` failed —
  `[Worklets] Your installed version of React Native (0.87.0) is ...`
- `react-native-safe-area-context` fallback:
  `:react-native-safe-area-context:compileDebugKotlin` failed.

A `fail-baseline` status therefore does not rule out a `newDsl` problem. It
only means the fallback build could not prove one. `react-native-mmkv` is
another case outside these six: its flagged build fails on the `kotlin`
extension conflict, its fallback build fails with `Project with path
':react-native-nitro-modules' could not be found`.

### Two harness bugs found and fixed during this run

Both produced wrong statuses and both are fixed in `scripts/test-libs.sh`.
See the git log for the commits.

1. **`app.json` was not restored between packages.** `npx expo install` appends
   config plugins to `app.json`, but the cleanup step restored only
   `package.json` and `yarn.lock`. After `expo-secure-store` was tested and
   removed, its dangling plugin entry stayed, and all 150 following builds
   failed at `:expo-constants:createExpoConfig` with `Failed to resolve plugin
   for module "expo-secure-store"`. All 150 were recorded `fail-baseline`.
   Their rows and logs were removed and re-tested. `app.json` is now restored
   with the other two files.
2. **`android/app/.cxx` was not cleared between builds.** A build could fail on
   the previous package's codegen target. Three logs showed it, each naming the
   target of the package tested immediately before: `react_codegen_RNKC` from
   keyboard-controller, `react_codegen_rnpicker` from picker,
   `react_codegen_rnscreens` from screens. Re-tested with `.cxx` cleared, all
   three changed status:
   `@react-native-firebase/app` fail-newdsl to pass,
   `@react-native-masked-view/masked-view` fail-newdsl to pass,
   `react-native-gesture-handler` fail-baseline to fail-newdsl.
   The `gradle` function now clears `.cxx` before every build.

## Known limits

- Sequential. One Gradle build per library, about 1 to 3 minutes each.
- Both external steps have a deadline, via `gtimeout` from coreutils:
  `TIMEOUT_INSTALL` (default 900s) and `TIMEOUT_BUILD` (default 2400s). This is
  not optional hardening. `realm` hung inside `npx expo install` for 19 hours:
  its `yarn add` finished in 6 seconds, the expo CLI wrapper never exited, and
  no build was ever attempted. A stalled run is indistinguishable from a working
  one unless something enforces a deadline. Watch row count over time, not just
  whether the process is alive.
- `ensure_disk` prunes Gradle's transforms cache when free space drops below
  `MIN_FREE_GB` (default 12). Without it a long run fills the disk, and every
  build after that fails for a reason unrelated to the DSL while still being
  recorded as `fail-baseline`.
- `fail-baseline` results are not investigated. They may be config-plugin or
  peer-dependency problems unrelated to AGP.
- The AGP version comes from `@react-native/gradle-plugin` in `node_modules`
  (9.2.1 at the time of writing). Gradle is 9.4.1 from the wrapper.

## Environment

- Expo SDK 58 canary (`58.0.0-canary-20260902-26df09e`), React Native 0.87.0.
- Docs for this SDK: https://docs.expo.dev/versions/v58.0.0/
