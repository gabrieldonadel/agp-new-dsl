# Did the merged fixes actually work?

Merged, released and fixed are three different things. This checks all three for
every merged pull request, by **building** each published package rather than
reading its gradle file.

Re-run with `RESULTS=verify-released.csv LIBS=<list> scripts/test-libs.sh`.

## Latest run: 2026-11-23, 74 newly shipped packages

139 pull requests are merged. 74 more packages have the fix on npm since the
last run, including two whose PR was closed because the maintainer landed the
change themselves (`@castleio/react-native-castle`, `@cohorly/react-native`).
All 74 were built. Combined with the 64 from September that is 138.

| Result | This run | All runs |
|---|---|---|
| **pass** | **32** | **73** |
| fail-newdsl | 20 | 27 |
| fail-baseline | 22 | 38 |
| **total built** | **74** | **138** |

**No library that shipped the guard inline still hits the collision itself.**
What the 42 failures are instead:

| Cause | Count | Packages |
|---|---|---|
| Kotlin sources only on `java.srcDirs` | 8 | `@bitdrift/react-native`, `@callstack/repack`, `@giphy/react-native-sdk`, `@rokt/react-native-sdk`, `react-native-auto-skeleton`, `react-native-edge-to-edge`, `react-native-localize`, `react-native-permissions` |
| Collision re-added by `expo-modules-core` | 5 | `@nandorojo/galeria`, `react-native-image-colors`, `@livekit/react-native-expo-plugin`, `@badatgil/expo-mapbox-navigation`, `@bryandev/expo-mapbox-navigation` |
| `kotlinOptions()` not found | 5 | `@avasapp/react-native-app-intents`, `@carlossts/react-native-leaflet-platform`, `@didomi/react-native`, `react-native-audio-api`, `@castleio/react-native-castle` |
| Other Kotlin compile errors | 5 | `react-native-video-trim`, `stream-chat-expo`, `@ammarahmed/react-native-workers`, `@fintecsystems/xs2a-react-native` (Kotlin metadata version), `@amplitude/analytics-react-native` (its async-storage dependency) |
| Guard present (inside an `isKotlinPluginMissing()` helper), collides anyway; not yet diagnosed | 1 | `react-native-bootsplash` |
| Removed DSL property `unitTestVariants` | 1 | `@datadog/mobile-react-native` |
| javac compile error | 1 | `react-native-mmkv-storage` |
| Missing sibling project (peer not installed) | 10 | mostly Nitro modules without `react-native-nitro-modules` |
| Dependency resolution | 3 | `@expensify/react-native-wallet`, `react-native-capture-protection`, `react-native-klarna-inapp-sdk` |
| `createExpoConfig` | 2 | `@cohorly/react-native`, `@stripe/stripe-terminal-react-native` |
| Manifest merger (`minSdkVersion`) | 1 | `@ua/react-native-airship` |

### Two findings worth acting on

**`java.srcDirs` is the next wave.** Built-in Kotlin compiles `kotlin.srcDirs`
and the default `src/main/java`, not extra folders added to `java.srcDirs`.
Libraries that keep `src/newarch` / `src/oldarch` there get past configuration
now, then fail with `Unresolved reference` on their own module classes. The fix
is to mirror the same folders into `kotlin.srcDirs`, which is what the rudder
and rive maintainers asked for on their PRs. It is mechanical, like the guard.

**`expo-modules-core` re-applies the plugin.** Packages on the legacy Expo
module template call `applyKotlinExpoModulesCorePlugin()` from
`expo-modules-core/android/ExpoModulesCorePlugin.gradle`, which runs
`apply plugin: 'kotlin-android'` inside a `try/catch`. The catch does not stop
the AGP 9 failure (`Failed to apply plugin 'com.android.internal.library'`:
"The 'org.jetbrains.kotlin.android' plugin is no longer required"), so these
packages fail even with our guard in their own file. Still unguarded on
`expo/expo` main as of 2026-11-23. 33 packages in the main run fail with this
signature; one guard there fixes them without touching the libraries.

### The run itself

The first attempt filled the disk at package 36 and recorded the next 39 as
`install-failed`: the same long uniform block described in the README. Those
rows were discarded and re-run. `ensure_disk` now stops the run when pruning
cannot get back above `MIN_HARD_GB` (default 5), and it runs before each install
as well as before each build.

## Previous run: 2026-09-11, all 64 shipped packages

79 pull requests are merged. 64 of the packages they cover have the fix
published on npm; 32 are merged but unreleased.

| Result | Count |
|---|---|
| **pass** | **41** |
| fail-baseline | 16 |
| fail-newdsl | 7 |
| **total built** | **64** |

**41 of 64 build clean under AGP 9.** Four of the eight packages added in this
run passed. The other four never reached an AGP 9 code path at all:

| Package | Stopped at |
|---|---|
| `@stream-io/react-native-callingx` | missing sibling `:react-native-firebase_app` |
| `@stream-io/video-react-native-sdk` | missing sibling `:stream-io_react-native-webrtc` |
| `react-native-vision-camera-face-detector` | missing sibling `:react-native-nitro-modules` |
| `@appcues/expo-config` | config plugin needs `ios.bundleIdentifier` in app config |

The first three declare those siblings as `peerDependencies`. The harness installs
only the package under test, so the peer is absent and Gradle fails before it
configures anything. This is a harness gap, not a library or AGP 9 defect. The
fourth is an Expo config plugin whose iOS branch throws during
`:expo-constants:createExpoConfig`, so the Android build never starts.

`@azizuysal/wallet-kit` records an empty version because
`require('<pkg>/package.json')` is blocked by the package's `exports` map. The
build itself is real: `:azizuysal_wallet-kit:compileDebugKotlin` ran and the
build succeeded.

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
