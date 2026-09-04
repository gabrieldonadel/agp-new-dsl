# Upstream AGP 9 pull requests

Every pull request filed from this harness, with live state.
Regenerate with `scripts/update-pr-status.py`; the list of PRs itself lives
in `upstream-prs.tsv`.

The bug is one thing: a library that applies `kotlin-android` or
`org.jetbrains.kotlin.android` unconditionally collides with the `kotlin`
extension AGP 9 registers itself. Two guard shapes appear. Round 1 derived the
answer from the AGP major version and the `android.builtInKotlin` property.
Round 2 checks for the registered extension directly, which needs no version
table and covers AGP 10, where the opt-out is removed:

```groovy
if (project.extensions.findByName('kotlin') == null) {
    apply plugin: 'kotlin-android'
}
```

| State | Count |
|---|---|
| open | 91 |
| merged | 13 |
| closed | 2 |
| **total** | **106** |

106 pull requests covering 123 packages.

## Pending (91)

Waiting on maintainers. `Discussion` is the number of comments and review
comments, so a non-zero value is worth a look.

| Package(s) | Usage | Round | Files | PR | Discussion | Note |
|---|---|---|---|---|---|---|
| `@react-native-community/datetimepicker` | 0.288 | 1 | 1 | https://github.com/react-native-datetimepicker/datetimepicker/pull/1058 |  |  |
| `react-native-nitro-modules` | 0.115 | 1 | 1 | https://github.com/margelo/nitro/pull/1579 | 1 |  |
| `react-native-google-mobile-ads` | 0.039 | 1 | 1 | https://github.com/invertase/react-native-google-mobile-ads/pull/886 |  |  |
| `react-native-edge-to-edge` | 0.038 | 1 | 1 | https://github.com/zoontek/react-native-edge-to-edge/pull/108 |  |  |
| `@datadog/mobile-react-native` | 0.029 | 1 | 1 | https://github.com/DataDog/dd-sdk-reactnative/pull/1394 |  |  |
| `react-native-permissions` | 0.026 | 1 | 1 | https://github.com/zoontek/react-native-permissions/pull/987 |  |  |
| `@react-native-menu/menu` | 0.02 | 1 | 1 | https://github.com/react-native-menu/menu/pull/1226 |  |  |
| `react-native-video` | 0.018 | 1 | 1 | https://github.com/TheWidlarzGroup/react-native-video/pull/5082 |  |  |
| `@braze/react-native-sdk` | 0.017 | 1 | 1 | https://github.com/braze-inc/braze-react-native-sdk/pull/333 |  |  |
| `@maplibre/maplibre-react-native` | 0.017 | 1 | 1 | https://github.com/maplibre/maplibre-react-native/pull/1645 |  |  |
| `react-native-localize` | 0.017 | 1 | 1 | https://github.com/zoontek/react-native-localize/pull/343 |  |  |
| `@amplitude/analytics-react-native` | 0.016 | 1 | 1 | https://github.com/amplitude/Amplitude-TypeScript/pull/1966 |  |  |
| `@rudderstack/rudder-sdk-react-native` | 0.013 | 1 | 1 | https://github.com/rudderlabs/rudder-sdk-react-native/pull/696 | 5 | CodeRabbit asked for an AGP 10 guard (taken) and an android.newDsl check (declined, with reasoning in the thread). |
| `react-native-keychain` | 0.012 | 1 | 1 | https://github.com/oblador/react-native-keychain/pull/812 |  |  |
| `rive-react-native` | 0.012 | 1 | 1 | https://github.com/rive-app/rive-react-native/pull/446 |  |  |
| `@aws-amplify/react-native` | 0.011 | 1 | 1 | https://github.com/aws-amplify/amplify-js/pull/14933 | 1 |  |
| `@op-engineering/op-sqlite` | 0.01 | 1 | 1 | https://github.com/OP-Engineering/op-sqlite/pull/447 |  |  |
| `@invertase/react-native-apple-authentication` | 0.01 | 1 | 1 | https://github.com/invertase/react-native-apple-authentication/pull/390 |  |  |
| `@segment/analytics-react-native-plugin-advertising-id`, `@segment/sovran-react-native` | 0.009 | 2 | 3 | https://github.com/segmentio/analytics-react-native/pull/1325 |  |  |
| `react-native-document-scanner-plugin` | 0.008 | 2 | 1 | https://github.com/WebsiteBeaver/react-native-document-scanner-plugin/pull/183 |  |  |
| `customerio-reactnative` | 0.008 | 2 | 1 | https://github.com/customerio/customerio-reactnative/pull/652 |  |  |
| `react-native-teleport` | 0.008 | 2 | 1 | https://github.com/kirillzyusko/react-native-teleport/pull/191 | 1 |  |
| `react-native-bootsplash` | 0.008 | 2 | 1 | https://github.com/zoontek/react-native-bootsplash/pull/798 |  |  |
| `@posthog/react-native-plugin` | 0.007 | 2 | 2 | https://github.com/PostHog/posthog-js/pull/4789 | 1 | Maintainer asked for a changeset (added) and signed commits. Signing needs a key on the account; offered squash-merge via the UI or taking the change directly as alternatives. |
| `react-native-bottom-tabs` | 0.007 | 2 | 1 | https://github.com/callstack/react-native-bottom-tabs/pull/568 |  |  |
| `@react-native-vector-icons/ant-design`, `@react-native-vector-icons/entypo`, `@react-native-vector-icons/evil-icons`, `@react-native-vector-icons/feather`, `@react-native-vector-icons/fontawesome`, `@react-native-vector-icons/fontawesome5`, `@react-native-vector-icons/fontawesome6`, `@react-native-vector-icons/get-image`, `@react-native-vector-icons/ionicons`, `@react-native-vector-icons/lucide`, `@react-native-vector-icons/material-design-icons`, `@react-native-vector-icons/material-icons`, `@react-native-vector-icons/octicons` | 0.007 | 2 | 41 | https://github.com/oblador/react-native-vector-icons/pull/1928 |  |  |
| `react-native-image-colors` | 0.007 | 2 | 1 | https://github.com/osamaqarem/react-native-image-colors/pull/114 |  |  |
| `@react-native-documents/picker`, `@react-native-documents/viewer` | 0.007 | 2 | 2 | https://github.com/react-native-documents/document-picker/pull/1004 | 1 |  |
| `react-native-audio-api` | 0.007 | 2 | 2 | https://github.com/software-mansion/react-native-audio-api/pull/1271 |  |  |
| `react-native-ease` | 0.006 | 2 | 1 | https://github.com/appandflow/react-native-ease/pull/56 |  |  |
| `react-native-passkeys` | 0.006 | 2 | 1 | https://github.com/peterferguson/react-native-passkeys/pull/71 | 1 |  |
| `@10play/tentap-editor` | 0.005 | 2 | 1 | https://github.com/10play/10tap-editor/pull/350 |  |  |
| `react-native-shake` | 0.005 | 2 | 1 | https://github.com/Doko-Demo-Doa/react-native-shake/pull/160 |  |  |
| `@amplitude/experiment-react-native-client` | 0.005 | 2 | 1 | https://github.com/amplitude/experiment-react-native-client/pull/69 |  |  |
| `react-native-legal` | 0.005 | 2 | 1 | https://github.com/callstackincubator/react-native-legal/pull/182 |  |  |
| `react-native-html-to-pdf` | 0.005 | 2 | 1 | https://github.com/christopherdro/react-native-html-to-pdf/pull/338 |  |  |
| `stream-chat-expo` | 0.004 | 2 | 2 | https://github.com/GetStream/stream-chat-react-native/pull/3798 |  |  |
| `@iterable/react-native-sdk` | 0.004 | 2 | 1 | https://github.com/Iterable/react-native-sdk/pull/897 |  |  |
| `react-native-release-profiler` | 0.004 | 2 | 1 | https://github.com/margelo/react-native-release-profiler/pull/28 |  |  |
| `skyflow-react-native` | 0.004 | 2 | 1 | https://github.com/skyflowapi/skyflow-react-native/pull/159 |  |  |
| `@adyen/react-native` | 0.003 | 2 | 1 | https://github.com/Adyen/adyen-react-native/pull/1223 |  |  |
| `react-native-pdf-renderer` | 0.003 | 2 | 1 | https://github.com/douglasjunior/react-native-pdf-renderer/pull/70 |  |  |
| `react-native-passkey` | 0.003 | 2 | 1 | https://github.com/f-23/react-native-passkey/pull/116 |  |  |
| `@nandorojo/galeria` | 0.003 | 2 | 1 | https://github.com/nandorojo/galeria/pull/130 |  |  |
| `@phantom/react-native-juicebox-sdk` | 0.003 | 2 | 1 | https://github.com/phantom/react-native-juicebox-sdk/pull/31 | 1 |  |
| `@phantom/react-native-webview` | 0.003 | 2 | 1 | https://github.com/phantom/react-native-webview/pull/56 | 1 |  |
| `@powersync/op-sqlite`, `@powersync/react-native` | 0.003 | 2 | 1 | https://github.com/powersync-ja/powersync-js/pull/1091 | 2 |  |
| `react-native-nano-icons` | 0.003 | 2 | 1 | https://github.com/software-mansion-labs/react-native-nano-icons/pull/56 |  |  |
| `react-native-pulsar` | 0.003 | 2 | 1 | https://github.com/software-mansion/pulsar/pull/258 |  |  |
| `react-native-enriched`, `react-native-enriched-html` | 0.003 | 2 | 1 | https://github.com/software-mansion/react-native-enriched-html/pull/787 |  |  |
| `react-native-sound` | 0.003 | 2 | 1 | https://github.com/zmxv/react-native-sound/pull/899 |  |  |
| `@stream-io/react-native-webrtc` | 0.002 | 2 | 1 | https://github.com/GetStream/react-native-webrtc/pull/66 | 1 |  |
| `@giphy/react-native-sdk` | 0.002 | 2 | 1 | https://github.com/Giphy/giphy-react-native-sdk/pull/229 |  |  |
| `@walletconnect/react-native-compat` | 0.002 | 2 | 1 | https://github.com/WalletConnect/walletconnect-monorepo/pull/7335 | 2 |  |
| `react-native-adapty` | 0.002 | 2 | 1 | https://github.com/adaptyteam/AdaptySDK-React-Native/pull/340 | 2 |  |
| `react-native-drop-shadow` | 0.002 | 2 | 1 | https://github.com/hoanglam10499/react-native-drop-shadow/pull/47 |  |  |
| `react-native-ble-manager` | 0.002 | 2 | 1 | https://github.com/innoveit/react-native-ble-manager/pull/1434 |  |  |
| `klaviyo-react-native-sdk` | 0.002 | 2 | 1 | https://github.com/klaviyo/klaviyo-react-native-sdk/pull/416 | 2 |  |
| `react-native-avoid-softinput` | 0.002 | 2 | 1 | https://github.com/mateusz1913/react-native-avoid-softinput/pull/293 |  |  |
| `@mixpanel/react-native-session-replay` | 0.002 | 2 | 1 | https://github.com/mixpanel/mixpanel-react-native-session-replay/pull/82 |  |  |
| `react-native-tiktok-business-sdk` | 0.002 | 2 | 1 | https://github.com/mtebele/react-native-tiktok-business-sdk/pull/40 |  |  |
| `@pusher/pusher-websocket-react-native` | 0.002 | 2 | 1 | https://github.com/pusher/pusher-websocket-react-native/pull/219 |  |  |
| `@swmansion/react-native-bottom-sheet` | 0.002 | 2 | 1 | https://github.com/software-mansion-labs/react-native-bottom-sheet/pull/81 |  |  |
| `clevertap-react-native` | 0.001 | 2 | 1 | https://github.com/CleverTap/clevertap-react-native/pull/521 | 2 |  |
| `@domir/react-native-measure-text` | 0.001 | 2 | 1 | https://github.com/DomiR/react-native-measure-text/pull/5 |  |  |
| `react-native-advanced-input-mask` | 0.001 | 2 | 1 | https://github.com/IvanIhnatsiuk/react-native-advanced-input-mask/pull/156 | 1 |  |
| `@lottiefiles/dotlottie-react-native` | 0.001 | 2 | 1 | https://github.com/LottieFiles/dotlottie-react-native/pull/84 | 1 |  |
| `@rokt/react-native-sdk` | 0.001 | 2 | 1 | https://github.com/ROKT/rokt-sdk-react-native/pull/301 | 3 |  |
| `@simform_solutions/react-native-audio-waveform` | 0.001 | 2 | 1 | https://github.com/SimformSolutionsPvtLtd/react-native-audio-waveform/pull/215 |  |  |
| `@theoplayer/react-native-engage` | 0.001 | 2 | 11 | https://github.com/THEOplayer/react-native-connectors/pull/472 |  |  |
| `react-native-file-viewer-turbo` | 0.001 | 2 | 1 | https://github.com/Vadko/react-native-file-viewer-turbo/pull/44 |  |  |
| `react-native-file-access` | 0.001 | 2 | 1 | https://github.com/alpha0010/react-native-file-access/pull/95 |  |  |
| `react-native-appstack-sdk` | 0.001 | 2 | 1 | https://github.com/appstack-tech/react-native-appstack-sdk/pull/50 | 1 |  |
| `@react-native-community/image-editor` | 0.001 | 2 | 1 | https://github.com/callstack/react-native-image-editor/pull/208 |  |  |
| `@siteed/audio-studio` | 0.001 | 2 | 4 | https://github.com/deeeed/audiolab/pull/489 | 1 |  |
| `@embrace-io/react-native` | 0.001 | 2 | 3 | https://github.com/embrace-io/embrace-react-native-sdk/pull/1033 |  |  |
| `react-native-exponea-sdk` | 0.001 | 2 | 1 | https://github.com/exponea/exponea-react-native-sdk/pull/144 |  |  |
| `@getcello/cello-react-native` | 0.001 | 2 | 1 | https://github.com/getcello/cello-react-native/pull/5 |  |  |
| `expo-pdf-text-extract` | 0.001 | 2 | 1 | https://github.com/gr8pathik/expo-pdf-text-extract/pull/2 |  |  |
| `@ht-sdks/sovran-react-native` | 0.001 | 2 | 3 | https://github.com/ht-sdks/events-sdk-react-native/pull/74 | 1 |  |
| `@infinitered/react-native-mlkit-face-detection`, `@infinitered/react-native-mlkit-text-recognition` | 0.001 | 2 | 5 | https://github.com/infinitered/react-native-mlkit/pull/269 | 1 |  |
| `@kesha-antonov/react-native-background-downloader` | 0.001 | 2 | 1 | https://github.com/kesha-antonov/react-native-background-downloader/pull/177 |  |  |
| `@logicwind/react-native-exit-app` | 0.001 | 2 | 1 | https://github.com/logicwind/react-native-exit-app/pull/9 |  |  |
| `react-native-fast-opencv` | 0.001 | 2 | 1 | https://github.com/lukaszkurantdev/react-native-fast-opencv/pull/118 |  |  |
| `react-native-blurhash` | 0.001 | 2 | 1 | https://github.com/margelo/react-native-blurhash/pull/213 |  |  |
| `@mattermost/react-native-paste-input` | 0.001 | 2 | 1 | https://github.com/mattermost/react-native-paste-input/pull/57 | 1 |  |
| `react-native-auto-skeleton` | 0.001 | 2 | 1 | https://github.com/pioner92/react-native-auto-skeleton/pull/21 |  |  |
| `@sbaiahmed1/react-native-biometrics` | 0.001 | 2 | 1 | https://github.com/sbaiahmed1/react-native-biometrics/pull/101 | 1 |  |
| `react-native-executorch` | 0.001 | 2 | 2 | https://github.com/software-mansion/react-native-executorch/pull/1412 | 1 |  |
| `react-native-camera-kit` | 0.001 | 2 | 1 | https://github.com/teslamotors/react-native-camera-kit/pull/810 |  |  |
| `react-native-crisp-chat-sdk` | 0.001 | 2 | 1 | https://github.com/walterholohan/react-native-crisp-chat-sdk/pull/212 |  |  |

## Merged (13)

| Package(s) | Usage | Round | Files | PR | Merged | Note |
|---|---|---|---|---|---|---|
| `react-native-purchases` | 0.136 | 1 | 1 | https://github.com/RevenueCat/react-native-purchases/pull/1934 | 2026-09-03 | Maintainer asked for the extension check instead of the version table; switched, then merged. Round 2 follows their shape. |
| `@react-native-google-signin/google-signin` | 0.132 | 1 | 1 | https://github.com/react-native-google-signin/google-signin/pull/1524 | 2026-09-03 |  |
| `@lodev09/react-native-true-sheet` | 0.012 | 1 | 1 | https://github.com/lodev09/react-native-true-sheet/pull/819 | 2026-09-02 |  |
| `react-native-enriched-markdown` | 0.011 | 1 | 1 | https://github.com/software-mansion/enriched-markdown/pull/744 | 2026-09-03 |  |
| `@preeternal/react-native-cookie-manager` | 0.009 | 2 | 1 | https://github.com/Preeternal/react-native-cookie-manager/pull/5 | 2026-09-04 |  |
| `react-native-volume-manager` | 0.007 | 2 | 1 | https://github.com/hirbod/react-native-volume-manager/pull/63 | 2026-09-04 |  |
| `react-native-navigation-mode` | 0.003 | 2 | 1 | https://github.com/JairajJangle/react-native-navigation-mode/pull/28 | 2026-09-04 |  |
| `react-native-video-trim` | 0.003 | 2 | 1 | https://github.com/maitrungduc1410/react-native-video-trim/pull/141 | 2026-09-04 |  |
| `@dr.pogodin/react-native-fs` | 0.002 | 2 | 1 | https://github.com/birdofpreyru/react-native-fs/pull/161 | 2026-09-04 |  |
| `@clerk/expo-google-signin`, `@clerk/expo-passkeys` | 0.002 | 2 | 3 | https://github.com/clerk/javascript/pull/9662 | 2026-09-04 |  |
| `react-native-fast-rsa` | 0.002 | 2 | 1 | https://github.com/jerson/react-native-fast-rsa/pull/101 | 2026-09-04 |  |
| `@sbaiahmed1/react-native-blur` | 0.002 | 2 | 1 | https://github.com/sbaiahmed1/react-native-blur/pull/165 | 2026-09-04 |  |
| `react-native-cloud-storage` | 0.001 | 2 | 1 | https://github.com/kuatsu/react-native-cloud-storage/pull/85 | 2026-09-04 |  |

## Closed without merging (2)

Check each one: so far every closure has been a maintainer taking the change
through their own process rather than rejecting it.

| Package(s) | Usage | Round | Files | PR | Discussion | Note |
|---|---|---|---|---|---|---|
| `@atomicfi/transact-react-native` | 0.004 | 2 | 1 | https://github.com/atomicfi/atomic-transact-react-native/pull/197 | 1 | Closed on company policy: external PRs go through their internal workflow. Maintainer confirmed they are applying the change. |
| `@clerk/expo-google-signin`, `@clerk/expo-passkeys` | 0.002 | 2 | 2 | https://github.com/clerk/javascript/pull/9660 | 4 | Closed in favour of clerk/javascript#9662, which merged with the same guard and credits us as co-author. Clerk is fixed. |

