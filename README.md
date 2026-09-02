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
| `lib-table.csv` | Raw input. `Package,Usage`. 108k rows, 3 malformed. Do not edit. |
| `scripts/filter-libs.sh` | Cleans the CSV into `libs.txt`. |
| `libs.txt` | Packages to test, one per line. 157 entries. |
| `libs-skipped.txt` | Cache of packages the filter rejected. Delete a line to re-check it. |
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

| Package | Version | Status | Note |
|---|---|---|---|
| react-native-svg | 15.15.4 | pass | |
| @react-native-async-storage/async-storage | 2.2.0 | fail-newdsl | Kotlin compile: unresolved reference `room`. |

Expected but not yet confirmed: every library that applies
`org.jetbrains.kotlin.android` or `kotlin-android` unconditionally will report
`fail-newdsl`. Known cases in `node_modules` at the time of writing:
gesture-handler, safe-area-context, reanimated, worklets. `react-native-screens`
guards it behind `shouldEnableAgpFallback()`.

## Known limits

- Sequential. One Gradle build per library, about 1 to 3 minutes each.
- No per-build timeout. macOS has no `timeout`. Wrap the `gradle` function in
  `gtimeout` from coreutils if a build hangs.
- `fail-baseline` results are not investigated. They may be config-plugin or
  peer-dependency problems unrelated to AGP.
- The AGP version comes from `@react-native/gradle-plugin` in `node_modules`
  (9.2.1 at the time of writing). Gradle is 9.4.1 from the wrapper.

## Environment

- Expo SDK 58 canary (`58.0.0-canary-20260902-26df09e`), React Native 0.87.0.
- Docs for this SDK: https://docs.expo.dev/versions/v58.0.0/
