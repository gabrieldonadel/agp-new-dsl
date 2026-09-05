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
| `upstream-prs.tsv` | The PRs filed, one per line. Source of truth; add a `note` for context. |
| `upstream-prs.md` | Generated tracker: pending / merged / closed, with live state. |
| `scripts/update-pr-status.py` | Refreshes `upstream-prs.md` from GitHub. `--check` to print only. |
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

1002 packages built against the AGP 9 defaults: the 1000 highest-usage
entries of `libs-android.txt` with `package.json` dependencies removed, plus 2
carried over from the original `libs.txt` run.

| Status | Count |
|---|---|
| `pass` | 364 |
| `fail-newdsl` | 281 |
| `fail-baseline` | 348 |
| `install-failed` | 8 |
| `timeout` | 1 |
| **total** | **1002** |

### What breaks under the new DSL (281)

Cause taken from the first `* What went wrong:` block of the flagged build,
before the fallback build runs.

| Cause | Count | Share |
|---|---|---|
| Kotlin plugin collides with AGP's built-in Kotlin | 269 | 96% |
| Removed DSL property (`libraryVariants`, `bootClasspath`) | 6 | 2% |
| Kotlin compile error | 4 | 1% |
| javac compile error | 1 | 0% |
| Other | 1 | 0% |

**One bug is almost all of it, and doubling the sample did not change that.**
It was 144 of 152 at 500 packages and 269 of 281 at 1000.
AGP 9 registers the `kotlin` extension itself, so a library that also applies
`kotlin-android` or `org.jetbrains.kotlin.android` unconditionally fails during
configuration. AGP reports it two ways, both the same problem:

```
Cannot add extension with name 'kotlin', as there is an extension already registered with that name.
The 'org.jetbrains.kotlin.android' plugin is no longer required for Kotlin support since AGP 9.0.
```

The rest are unrelated to the Kotlin plugin and each needs its own work:

- **Removed DSL property (`libraryVariants`, `bootClasspath`)**: `react-native-launch-arguments`, `react-native-onetrust-cmp`, `react-native-context-menu-view`, `react-native-create-thumbnail`, `react-native-worklets-core`, `@dariyd/react-native-document-scanner`
- **Kotlin compile error**: `@react-native-async-storage/async-storage`, `@apollohg/react-native-prose-editor`, `@bhojaniasgar/react-native-otp-input`, `@datalyr/react-native`
- **javac compile error**: `react-native-keyboard-controller`
- **Other**: `expo-updates` — `expo-updates` fails inside
  `expo-autolinking` on a null `KotlinJvmAndroidCompilation.getAndroidVariant()`.

The full per-package list is `results.csv`, one log each under `logs/`.

### 72 of the passes are vacuous

72 of the tested packages are Capacitor or Cordova plugins, and all
72 of them are recorded `pass`. They ship an `android/build.gradle`, so
`scan-libs.py` selects them, but React Native autolinking ignores them entirely:
their modules produce **no Gradle tasks** in the build. The app compiles because
the plugin was never part of it.

So `pass` is 364 nominally and **292 meaningfully**. Those
72 say nothing about AGP 9 either way; they could be as broken as anything
else and this harness would not see it. They cluster in the low-usage tail, so the
first 500 are unaffected.

A React Native harness cannot test them. Testing them needs a Capacitor host app,
which is a different project.

### `install-failed` (8) and `timeout` (1)

All genuine, and small enough to list: 4 crash `npm`/`node` with `SIGABRT`, 1
pins an incompatible Node engine, 2 depend on packages that are not published,
and 1 fails its own `react-native` link step. `realm` is the single `timeout`:
its install hung and was killed at the 900s deadline, so it has no verdict.

Four separate times a systemic failure was recorded as per-package verdicts
instead. See "Harness failures that produced fake results" below; the counts
above are after removing all of them.

### `fail-baseline` (348)

Fails with the flags on and with them off, so the harness cannot attribute it to
the DSL. Not investigated. This understates new-DSL breakage: a package whose
flagged build dies on the Kotlin collision but whose fallback build also fails,
for a missing peer dependency or its own version assert, lands here rather than
in `fail-newdsl`. `react-native-reanimated`, `react-native-worklets` and
`react-native-safe-area-context` are exactly that case.

### How far the upstream PRs go

269 packages now hit the Kotlin plugin collision, up from 144 at 500 packages.
The PRs were filed against the first 500, where every collision case that could
take a pull request has one:

| | Count |
|---|---|
| collisions in the first 500 | 144 |
| covered by a pull request from this harness | 126 |
| already fixed upstream, or another contributor's PR | 5 |
| cannot take a PR (no repo, 404, archived) | 8 |
| no unconditional apply left, or a `plugins {}` block | 5 |

The second 500 added **125 more collision cases** that have no PR yet. They are
all in the tail: the highest usage among them is 0.001, and most are 0. The same
one-line guard fixes every one, so it is mechanical work rather than 125
investigations.

105 pull requests cover the 126, because several repositories are monorepos where
one PR fixes many: `oblador/react-native-vector-icons` is 41 files across 13
packages, `THEOplayer/react-native-connectors` is 11 files, and
`infinitered/react-native-mlkit` is 5.

### Upstream fixes

The 144 collision cases are one bug with one fix: apply the Kotlin plugin only
when AGP is not already providing it. `react-native-screens` already does this,
which is why it passes.

**105 pull requests are filed, covering 126 packages across 105 repositories.**
The tracker is [`upstream-prs.md`](upstream-prs.md), grouped into pending, merged
and closed. Refresh it with `scripts/update-pr-status.py`; the PR list itself
lives in `upstream-prs.tsv`, where a `note` column records anything a maintainer
asked for.

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

### Harness failures that produced fake results

Four times a single systemic failure was written into `results.csv` as a long run
of per-package verdicts. Every one looked plausible from the outside, because
`fail-baseline` and `install-failed` are ordinary outcomes. All four rows below
were removed and re-tested, and each now has a guard.

| Cause | Rows poisoned | Guard |
|---|---|---|
| `npx expo install` appends a config plugin to `app.json`; the cleanup restored only `package.json` and `yarn.lock`, so the dangling plugin failed `:expo-constants:createExpoConfig` for every later package | 150 | `app.json` restored with the other two |
| `android/app/.cxx` persisted between packages, so a build could fail on the previous package's codegen target | 3 | `.cxx` cleared before every build |
| The network dropped mid-run; every remaining install failed `EHOSTUNREACH` and was recorded `install-failed` | 306 | `net_error` waits for the registry, retries once, aborts if still down |
| A failed install stripped the expo CLI from `node_modules`; every later package failed `expo: command not found` | 53 | `ensure_harness` checks and repairs before each package |

The shape is always the same: a long contiguous block of one verdict, with no
other outcome appearing after the first one. That is the signal to check for,
and it is worth checking whenever a run looks unusually uniform.

Two further failures stopped a run rather than corrupting it: Gradle's transforms
cache filled the disk, and `realm` hung inside `npx expo install` for 19 hours
because nothing enforced a deadline. `ensure_disk` and `gtimeout` cover both.

## Known limits

- Sequential. One Gradle build per library, about 1 to 3 minutes each.
- Both external steps have a deadline, via `gtimeout` from coreutils:
  `TIMEOUT_INSTALL` (default 900s) and `TIMEOUT_BUILD` (default 2400s). This is
  not optional hardening. `realm` hung inside `npx expo install` for 19 hours:
  its `yarn add` finished in 6 seconds, the expo CLI wrapper never exited, and
  no build was ever attempted. A stalled run is indistinguishable from a working
  one unless something enforces a deadline. Watch row count over time, not just
  whether the process is alive.
- A failed install can strip the expo CLI out of `node_modules`, after which every
  package fails with `expo: command not found` and is recorded `install-failed`.
  One package did that and took the next 53 with it. `ensure_harness` checks the
  CLI is present before each package, repairs with `yarn install`, and stops if it
  cannot.
- A dropped network is treated as a harness failure, not a result. `npx expo
  install` errors that look network-shaped (`EHOSTUNREACH` and friends) make the
  run wait for `registry.npmjs.org`, retry once, and abort if it is still down.
  Without that, one outage recorded 306 consecutive packages as `install-failed`,
  which reads exactly like 306 broken packages.
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
