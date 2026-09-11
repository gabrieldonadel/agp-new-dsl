# Did the merged fixes actually work?

Merged, released and fixed are three different things. This checks all three for
every merged pull request, by **building** each published package rather than
reading its gradle file.

Re-run with `RESULTS=verify-released.csv LIBS=<list> scripts/test-libs.sh`.

## Latest run: 2026-09-11, all 64 shipped packages

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
