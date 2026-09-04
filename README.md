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

All 157 packages in `libs.txt` are tested. One row each in `results.csv`.

| Status | Count |
|---|---|
| `pass` | 85 |
| `fail-newdsl` | 34 |
| `fail-baseline` | 38 |
| `install-failed` | 0 |
| **total** | **157** |

### `fail-newdsl` (34)

Fails with `newDsl` + `builtInKotlin` on, builds with them off. Error lines are
from the flagged build only, taken from the first `* What went wrong:` block.

| Package | Version | First Gradle error |
|---|---|---|
| @react-native-async-storage/async-storage | 2.2.0 | `:react-native-async-storage_async-storage:compileDebugKotlin` failed. First compiler error: `StorageSupplier.kt:5:17 Unresolved reference 'room'.` |
| expo-updates | 58.0.0-canary-20260902-26df09e | Evaluating project `:expo`: Failed to apply plugin `expo-autolinking`. Root cause: `Cannot invoke BaseVariant.getSourceFolders(SourceKind) because the return value of KotlinJvmAndroidCompilation.getAndroidVariant() is null`. |
| react-native-webview | 13.16.1 | Evaluating project `:react-native-webview`: Failed to apply plugin `kotlin-android`. |
| @react-native-community/datetimepicker | 9.1.0 | Evaluating project `:react-native-community_datetimepicker`: Failed to apply plugin `org.jetbrains.kotlin.android`. |
| react-native-keyboard-controller | 1.22.4 | `:app:compileDebugJavaWithJavac` failed. First compiler error: `PackageList.java:61: error: cannot find symbol` — `class KeyboardControllerPackage`. |
| react-native-maps | 1.27.2 | Evaluating project `:react-native-maps`: Failed to apply plugin `kotlin-android`. |
| react-native-purchases | 10.8.1 | Evaluating project `:react-native-purchases`: Failed to apply plugin `kotlin-android`. |
| @react-native-google-signin/google-signin | 16.1.4 | Evaluating project `:react-native-google-signin_google-signin`: Failed to apply plugin `org.jetbrains.kotlin.android`. |
| react-native-nitro-modules | 0.37.1 | Evaluating project `:react-native-nitro-modules`: Failed to apply plugin `org.jetbrains.kotlin.android`. |
| lottie-react-native | 7.3.8 | Evaluating project `:lottie-react-native`: Failed to apply plugin `kotlin-android`. |
| react-native-pager-view | 8.0.2 | Evaluating project `:react-native-pager-view`: Failed to apply plugin `kotlin-android`. |
| react-native-purchases-ui | 10.8.1 | Evaluating project `:react-native-purchases-ui`: Failed to apply plugin `kotlin-android`. |
| react-native-google-mobile-ads | 16.5.0 | Evaluating project `:react-native-google-mobile-ads`: Failed to apply plugin `kotlin-android`. |
| react-native-edge-to-edge | 1.8.1 | Evaluating project `:react-native-edge-to-edge`: Failed to apply plugin `kotlin-android`. |
| @datadog/mobile-react-native | 3.6.0 | Evaluating project `:datadog_mobile-react-native`: Failed to apply plugin `kotlin-android`. |
| react-native-permissions | 5.6.1 | Evaluating project `:react-native-permissions`: Failed to apply plugin `kotlin-android`. |
| @react-native-menu/menu | 2.0.0 | Evaluating project `:react-native-menu_menu`: Failed to apply plugin `kotlin-android`. |
| react-native-video | 6.19.2 | Evaluating project `:react-native-video`: Failed to apply plugin `kotlin-android`. |
| @maplibre/maplibre-react-native | 11.3.8 | Evaluating project `:maplibre_maplibre-react-native`: Failed to apply plugin `kotlin-android`. |
| react-native-worklets-core | 1.6.3 | Configuring project `:react-native-worklets-core`: Could not get unknown property `libraryVariants` for object of type `LibraryExtensionImpl$AgpDecorated`. |
| @braze/react-native-sdk | 23.0.0 | Evaluating project `:braze_react-native-sdk`: Failed to apply plugin `kotlin-android`. |
| react-native-localize | 3.7.0 | Evaluating project `:react-native-localize`: Failed to apply plugin `kotlin-android`. |
| @amplitude/analytics-react-native | 1.8.0 | Evaluating project `:amplitude_analytics-react-native`: Failed to apply plugin `kotlin-android`. |
| posthog-react-native-session-replay | 1.6.0 | Evaluating project `:posthog-react-native-session-replay`: Failed to apply plugin `kotlin-android`. |
| @rudderstack/rudder-sdk-react-native | 3.2.0 | Evaluating project `:rudderstack_rudder-sdk-react-native`: Failed to apply plugin `kotlin-android`. |
| react-native-launch-arguments | 4.1.1 | Configuring project `:react-native-launch-arguments`: Could not get unknown property `libraryVariants` for object of type `LibraryExtensionImpl$AgpDecorated`. |
| rive-react-native | 9.8.5 | Evaluating project `:rive-react-native`: Failed to apply plugin `kotlin-android`. |
| react-native-keychain | 10.0.0 | Evaluating project `:react-native-keychain`: Failed to apply plugin `kotlin-android`. |
| @lodev09/react-native-true-sheet | 3.11.12 | Evaluating project `:lodev09_react-native-true-sheet`: Failed to apply plugin `kotlin-android`. |
| @aws-amplify/react-native | 1.3.3 | Evaluating project `:aws-amplify_react-native`: Failed to apply plugin `kotlin-android`. |
| react-native-enriched-markdown | 1.0.2 | Evaluating project `:react-native-enriched-markdown`: Failed to apply plugin `kotlin-android`. |
| @invertase/react-native-apple-authentication | 2.5.1 | Evaluating project `:invertase_react-native-apple-authentication`: Failed to apply plugin `kotlin-android`. |
| @op-engineering/op-sqlite | 18.1.4 | Evaluating project `:op-engineering_op-sqlite`: Failed to apply plugin `kotlin-android`. |
| react-native-gesture-handler | 3.1.0 | Evaluating project `:react-native-gesture-handler`: Failed to apply plugin `kotlin-android`. |

29 of the 34 flagged builds end in the same cause line:
`Cannot add extension with name 'kotlin', as there is an extension already
registered with that name.` Those 29 are exactly the rows above that report
`Failed to apply plugin 'kotlin-android'` or
`Failed to apply plugin 'org.jetbrains.kotlin.android'`. This confirms the
expectation recorded earlier: a library that applies `kotlin-android` or
`org.jetbrains.kotlin.android` unconditionally cannot build under `newDsl`.

The other five fail differently. `react-native-worklets-core` and
`react-native-launch-arguments` fail on `libraryVariants`. `expo-updates`
fails on a null `getAndroidVariant()`. `@react-native-async-storage/async-storage`
and `react-native-keyboard-controller` fail at compile time.

`results.csv` records an empty version for
`posthog-react-native-session-replay`. The `node -p require(...)` version
probe in `test-libs.sh` cannot resolve that package's `package.json`. The
version above, 1.6.0, is read from the `yarn add` output in its log.

### Upstream fixes

The 29 `Failed to apply plugin` cases are one bug with one fix: apply the
Kotlin plugin only when AGP is not already providing it. `react-native-screens`
already does this, which is why it passes.

Patches are filed for every affected library that still needed one and accepts
pull requests. See "Not filed" below for the rest.
State as of 2026-09-03: **4 merged, 18 open**.

| Package | Usage | PR | Status |
|---|---|---|---|
| @react-native-community/datetimepicker | 0.288 | [react-native-datetimepicker/datetimepicker#1058](https://github.com/react-native-datetimepicker/datetimepicker/pull/1058) | open |
| react-native-purchases | 0.136 | [RevenueCat/react-native-purchases#1934](https://github.com/RevenueCat/react-native-purchases/pull/1934) | merged 2026-09-03 |
| @react-native-google-signin/google-signin | 0.132 | [react-native-google-signin/google-signin#1524](https://github.com/react-native-google-signin/google-signin/pull/1524) | merged 2026-09-03 |
| react-native-nitro-modules | 0.115 | [margelo/nitro#1579](https://github.com/margelo/nitro/pull/1579) | open |
| react-native-google-mobile-ads | 0.039 | [invertase/react-native-google-mobile-ads#886](https://github.com/invertase/react-native-google-mobile-ads/pull/886) | open |
| react-native-edge-to-edge | 0.038 | [zoontek/react-native-edge-to-edge#108](https://github.com/zoontek/react-native-edge-to-edge/pull/108) | open |
| @datadog/mobile-react-native | 0.029 | [DataDog/dd-sdk-reactnative#1394](https://github.com/DataDog/dd-sdk-reactnative/pull/1394) | open |
| react-native-permissions | 0.026 | [zoontek/react-native-permissions#987](https://github.com/zoontek/react-native-permissions/pull/987) | open |
| @react-native-menu/menu | 0.02 | [react-native-menu/menu#1226](https://github.com/react-native-menu/menu/pull/1226) | open |
| react-native-video | 0.018 | [TheWidlarzGroup/react-native-video#5082](https://github.com/TheWidlarzGroup/react-native-video/pull/5082) | open |
| react-native-localize | 0.017 | [zoontek/react-native-localize#343](https://github.com/zoontek/react-native-localize/pull/343) | open |
| @maplibre/maplibre-react-native | 0.017 | [maplibre/maplibre-react-native#1645](https://github.com/maplibre/maplibre-react-native/pull/1645) | open |
| @braze/react-native-sdk | 0.017 | [braze-inc/braze-react-native-sdk#333](https://github.com/braze-inc/braze-react-native-sdk/pull/333) | open |
| @amplitude/analytics-react-native | 0.016 | [amplitude/Amplitude-TypeScript#1966](https://github.com/amplitude/Amplitude-TypeScript/pull/1966) | open |
| @rudderstack/rudder-sdk-react-native | 0.013 | [rudderlabs/rudder-sdk-react-native#696](https://github.com/rudderlabs/rudder-sdk-react-native/pull/696) | open |
| rive-react-native | 0.012 | [rive-app/rive-react-native#446](https://github.com/rive-app/rive-react-native/pull/446) | open |
| react-native-keychain | 0.012 | [oblador/react-native-keychain#812](https://github.com/oblador/react-native-keychain/pull/812) | open |
| @lodev09/react-native-true-sheet | 0.012 | [lodev09/react-native-true-sheet#819](https://github.com/lodev09/react-native-true-sheet/pull/819) | merged 2026-09-02 |
| @aws-amplify/react-native | 0.011 | [aws-amplify/amplify-js#14933](https://github.com/aws-amplify/amplify-js/pull/14933) | open |
| react-native-enriched-markdown | 0.011 | [software-mansion/enriched-markdown#744](https://github.com/software-mansion/enriched-markdown/pull/744) | merged 2026-09-03 |
| @invertase/react-native-apple-authentication | 0.01 | [invertase/react-native-apple-authentication#390](https://github.com/invertase/react-native-apple-authentication/pull/390) | open |
| @op-engineering/op-sqlite | 0.01 | [OP-Engineering/op-sqlite#447](https://github.com/OP-Engineering/op-sqlite/pull/447) | open |

`react-native-purchases-ui` is fixed by the same PR as `react-native-purchases`.

Two variants of the guard are in use. Most PRs derive the answer from the AGP
major version and the `android.builtInKotlin` property. The RevenueCat PR checks
for the registered extension directly, at maintainer request:

```groovy
if (project.extensions.findByName('kotlin') == null) {
    apply plugin: 'kotlin-android'
}
```

The second form is simpler and needs no version table. It also covers AGP 10,
where the `android.builtInKotlin` opt-out is removed. Both forms were verified
in this harness against AGP 9.2.1: `:app:assembleDebug` succeeds with both
flags on and with both flags off.

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

### `fail-baseline` (38)

Fails both ways. Not a DSL result. Not investigated.

@braze/expo-plugin, @clerk/expo, @config-plugins/react-native-branch,
@intercom/intercom-react-native, @livekit/react-native,
@livekit/react-native-expo-plugin, @react-native-cookies/cookies,
@react-native-firebase/analytics, @react-native-firebase/app-check,
@react-native-firebase/auth, @react-native-firebase/crashlytics,
@react-native-firebase/firestore, @react-native-firebase/messaging,
@react-native-firebase/perf, @react-native-firebase/remote-config,
@react-native-firebase/storage, @rnmapbox/maps, @stripe/stripe-react-native,
expo-iap, expo-widgets, react-native-android-widget, react-native-appsflyer,
react-native-auth0, react-native-branch, react-native-compressor,
react-native-date-picker, react-native-fbsdk-next,
react-native-health-connect, react-native-iap, react-native-mmkv,
react-native-nitro-image, react-native-plaid-link-sdk,
react-native-quick-crypto, react-native-reanimated,
react-native-safe-area-context, react-native-unistyles,
react-native-vision-camera, react-native-worklets

### `install-failed` (0)

None.

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
