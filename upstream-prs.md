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
| open | 263 |
| merged | 22 |
| closed | 2 |
| **total** | **287** |

287 pull requests covering 311 packages.

## Pending (263)

Waiting on maintainers. `Discussion` is the number of comments and review
comments, so a non-zero value is worth a look.

| Package(s) | Usage | Round | Files | PR | Discussion | Note |
|---|---|---|---|---|---|---|
| `@react-native-community/datetimepicker` | 0.288 | 1 | 1 | https://github.com/react-native-datetimepicker/datetimepicker/pull/1058 |  |  |
| `react-native-nitro-modules` | 0.115 | 1 | 1 | https://github.com/margelo/nitro/pull/1579 | 1 |  |
| `react-native-mmkv` | 0.097 | 4 | 1 | https://github.com/margelo/react-native-mmkv/pull/1090 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@stripe/stripe-react-native` | 0.053 | 4 | 1 | https://github.com/stripe/stripe-react-native/pull/2602 | 2 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-google-mobile-ads` | 0.039 | 1 | 1 | https://github.com/invertase/react-native-google-mobile-ads/pull/886 |  |  |
| `react-native-edge-to-edge` | 0.038 | 1 | 1 | https://github.com/zoontek/react-native-edge-to-edge/pull/108 |  |  |
| `react-native-vision-camera`, `react-native-vision-camera-barcode-scanner`, `react-native-vision-camera-resizer`, `react-native-vision-camera-worklets` | 0.036 | 4 | 5 | https://github.com/margelo/react-native-vision-camera/pull/4181 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-appsflyer` | 0.034 | 4 | 1 | https://github.com/AppsFlyerSDK/appsflyer-react-native-plugin/pull/704 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `expo-iap`, `react-native-iap` | 0.031 | 4 | 2 | https://github.com/hyodotdev/openiap/pull/438 | 2 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@datadog/mobile-react-native` | 0.029 | 1 | 1 | https://github.com/DataDog/dd-sdk-reactnative/pull/1394 |  |  |
| `react-native-permissions` | 0.026 | 1 | 1 | https://github.com/zoontek/react-native-permissions/pull/987 |  |  |
| `react-native-health-connect` | 0.021 | 4 | 1 | https://github.com/matinzd/react-native-health-connect/pull/273 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@react-native-menu/menu` | 0.02 | 1 | 1 | https://github.com/react-native-menu/menu/pull/1226 |  |  |
| `react-native-unistyles` | 0.019 | 4 | 1 | https://github.com/jpudysz/react-native-unistyles/pull/1246 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-video` | 0.018 | 1 | 1 | https://github.com/TheWidlarzGroup/react-native-video/pull/5082 |  |  |
| `react-native-compressor` | 0.018 | 4 | 1 | https://github.com/numandev1/react-native-compressor/pull/419 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@braze/react-native-sdk` | 0.017 | 1 | 1 | https://github.com/braze-inc/braze-react-native-sdk/pull/333 |  |  |
| `react-native-localize` | 0.017 | 1 | 1 | https://github.com/zoontek/react-native-localize/pull/343 |  |  |
| `@amplitude/analytics-react-native` | 0.016 | 1 | 1 | https://github.com/amplitude/Amplitude-TypeScript/pull/1966 |  |  |
| `@braze/expo-plugin` | 0.016 | 4 | 1 | https://github.com/braze-inc/braze-expo-plugin/pull/50 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@livekit/react-native` | 0.015 | 4 | 1 | https://github.com/livekit/client-sdk-react-native/pull/454 | 2 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@rudderstack/rudder-sdk-react-native` | 0.013 | 1 | 1 | https://github.com/rudderlabs/rudder-sdk-react-native/pull/696 | 5 | CodeRabbit asked for an AGP 10 guard (taken) and an android.newDsl check (declined, with reasoning in the thread). |
| `@livekit/react-native-expo-plugin` | 0.012 | 4 | 1 | https://github.com/livekit/client-sdk-react-native-expo-plugin/pull/25 | 2 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-keychain` | 0.012 | 1 | 1 | https://github.com/oblador/react-native-keychain/pull/812 |  |  |
| `rive-react-native` | 0.012 | 1 | 1 | https://github.com/rive-app/rive-react-native/pull/446 |  |  |
| `@aws-amplify/react-native` | 0.011 | 1 | 1 | https://github.com/aws-amplify/amplify-js/pull/14933 | 1 |  |
| `react-native-auth0` | 0.01 | 4 | 1 | https://github.com/auth0/react-native-auth0/pull/1654 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@invertase/react-native-apple-authentication` | 0.01 | 1 | 1 | https://github.com/invertase/react-native-apple-authentication/pull/390 |  |  |
| `react-native-quick-crypto` | 0.01 | 4 | 1 | https://github.com/margelo/react-native-quick-crypto/pull/1075 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-nitro-image`, `react-native-nitro-web-image` | 0.01 | 4 | 2 | https://github.com/mrousavy/react-native-nitro-image/pull/178 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@segment/analytics-react-native-plugin-advertising-id`, `@segment/sovran-react-native` | 0.009 | 2 | 3 | https://github.com/segmentio/analytics-react-native/pull/1325 |  |  |
| `react-native-document-scanner-plugin` | 0.008 | 2 | 1 | https://github.com/WebsiteBeaver/react-native-document-scanner-plugin/pull/183 |  |  |
| `customerio-reactnative` | 0.008 | 2 | 1 | https://github.com/customerio/customerio-reactnative/pull/652 |  |  |
| `react-native-teleport` | 0.008 | 2 | 1 | https://github.com/kirillzyusko/react-native-teleport/pull/191 | 1 |  |
| `react-native-bootsplash` | 0.008 | 2 | 1 | https://github.com/zoontek/react-native-bootsplash/pull/798 |  |  |
| `react-native-bottom-tabs` | 0.007 | 2 | 1 | https://github.com/callstack/react-native-bottom-tabs/pull/568 |  |  |
| `@react-native-vector-icons/ant-design`, `@react-native-vector-icons/entypo`, `@react-native-vector-icons/evil-icons`, `@react-native-vector-icons/feather`, `@react-native-vector-icons/fontawesome`, `@react-native-vector-icons/fontawesome5`, `@react-native-vector-icons/fontawesome6`, `@react-native-vector-icons/get-image`, `@react-native-vector-icons/ionicons`, `@react-native-vector-icons/lucide`, `@react-native-vector-icons/material-design-icons`, `@react-native-vector-icons/material-icons`, `@react-native-vector-icons/octicons` | 0.007 | 2 | 41 | https://github.com/oblador/react-native-vector-icons/pull/1928 |  |  |
| `react-native-image-colors` | 0.007 | 2 | 1 | https://github.com/osamaqarem/react-native-image-colors/pull/114 |  |  |
| `@react-native-documents/picker`, `@react-native-documents/viewer` | 0.007 | 2 | 2 | https://github.com/react-native-documents/document-picker/pull/1004 | 1 |  |
| `react-native-audio-api` | 0.007 | 2 | 2 | https://github.com/software-mansion/react-native-audio-api/pull/1271 |  |  |
| `react-native-ease` | 0.006 | 2 | 1 | https://github.com/appandflow/react-native-ease/pull/56 |  |  |
| `react-native-passkeys` | 0.006 | 2 | 1 | https://github.com/peterferguson/react-native-passkeys/pull/71 | 1 |  |
| `@10play/tentap-editor` | 0.005 | 2 | 1 | https://github.com/10play/10tap-editor/pull/350 |  |  |
| `react-native-shake` | 0.005 | 2 | 1 | https://github.com/Doko-Demo-Doa/react-native-shake/pull/160 |  |  |
| `@nozbe/watermelondb` | 0.005 | 4 | 1 | https://github.com/Nozbe/WatermelonDB/pull/1974 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@amplitude/experiment-react-native-client` | 0.005 | 2 | 1 | https://github.com/amplitude/experiment-react-native-client/pull/69 |  |  |
| `react-native-legal` | 0.005 | 2 | 1 | https://github.com/callstackincubator/react-native-legal/pull/182 |  |  |
| `react-native-html-to-pdf` | 0.005 | 2 | 1 | https://github.com/christopherdro/react-native-html-to-pdf/pull/338 |  |  |
| `react-native-radar` | 0.005 | 4 | 1 | https://github.com/radarlabs/react-native-radar/pull/451 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `stream-chat-expo` | 0.004 | 2 | 2 | https://github.com/GetStream/stream-chat-react-native/pull/3798 |  |  |
| `@iterable/react-native-sdk` | 0.004 | 2 | 1 | https://github.com/Iterable/react-native-sdk/pull/897 |  |  |
| `react-native-release-profiler` | 0.004 | 2 | 1 | https://github.com/margelo/react-native-release-profiler/pull/28 |  |  |
| `@rive-app/react-native` | 0.004 | 4 | 2 | https://github.com/rive-app/rive-nitro-react-native/pull/377 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `skyflow-react-native` | 0.004 | 2 | 1 | https://github.com/skyflowapi/skyflow-react-native/pull/159 |  |  |
| `@stripe/stripe-terminal-react-native` | 0.004 | 4 | 1 | https://github.com/stripe/stripe-terminal-react-native/pull/1134 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@adyen/react-native` | 0.003 | 2 | 1 | https://github.com/Adyen/adyen-react-native/pull/1223 |  |  |
| `@adobe/react-native-aepmessaging` | 0.003 | 4 | 1 | https://github.com/adobe/aepsdk-react-native/pull/591 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-pdf-renderer` | 0.003 | 2 | 1 | https://github.com/douglasjunior/react-native-pdf-renderer/pull/70 |  |  |
| `react-native-passkey` | 0.003 | 2 | 1 | https://github.com/f-23/react-native-passkey/pull/116 |  |  |
| `expo-app-integrity` | 0.003 | 4 | 1 | https://github.com/jeffDevelops/expo-app-integrity/pull/14 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-vision-camera-face-detector` | 0.003 | 4 | 1 | https://github.com/luicfrr/react-native-vision-camera-face-detector/pull/246 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-fast-tflite` | 0.003 | 4 | 1 | https://github.com/margelo/react-native-fast-tflite/pull/203 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@nandorojo/galeria` | 0.003 | 2 | 1 | https://github.com/nandorojo/galeria/pull/130 |  |  |
| `@phantom/react-native-juicebox-sdk` | 0.003 | 2 | 1 | https://github.com/phantom/react-native-juicebox-sdk/pull/31 | 1 |  |
| `@phantom/react-native-webview` | 0.003 | 2 | 1 | https://github.com/phantom/react-native-webview/pull/57 | 2 | Re-filed on a unique branch. The first attempt shared a fork branch with another repository of the same name and showed unrelated commits; that PR was closed with an explanation. |
| `@powersync/op-sqlite`, `@powersync/react-native` | 0.003 | 2 | 1 | https://github.com/powersync-ja/powersync-js/pull/1091 | 2 |  |
| `react-native-nitro-google-signin` | 0.003 | 4 | 1 | https://github.com/react-native-nitro-google-sign-in/google-signin/pull/62 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-nano-icons` | 0.003 | 2 | 1 | https://github.com/software-mansion-labs/react-native-nano-icons/pull/56 |  |  |
| `react-native-enriched`, `react-native-enriched-html` | 0.003 | 2 | 1 | https://github.com/software-mansion/react-native-enriched-html/pull/787 |  |  |
| `react-native-sound` | 0.003 | 2 | 1 | https://github.com/zmxv/react-native-sound/pull/899 |  |  |
| `@stream-io/react-native-webrtc` | 0.002 | 2 | 1 | https://github.com/GetStream/react-native-webrtc/pull/67 | 1 | Re-filed on a unique branch. The first attempt shared a fork branch with another repository of the same name and showed unrelated commits; that PR was closed with an explanation. |
| `@stream-io/react-native-callingx`, `@stream-io/video-react-native-sdk` | 0.002 | 4 | 4 | https://github.com/GetStream/stream-video-js/pull/2417 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@giphy/react-native-sdk` | 0.002 | 2 | 1 | https://github.com/Giphy/giphy-react-native-sdk/pull/229 |  |  |
| `@walletconnect/react-native-compat` | 0.002 | 2 | 1 | https://github.com/WalletConnect/walletconnect-monorepo/pull/7335 | 2 |  |
| `react-native-adapty` | 0.002 | 2 | 1 | https://github.com/adaptyteam/AdaptySDK-React-Native/pull/340 | 2 |  |
| `@react-native-seoul/kakao-login` | 0.002 | 4 | 1 | https://github.com/crossplatformkorea/react-native-kakao-login/pull/443 | 2 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-wallet-manager` | 0.002 | 4 | 1 | https://github.com/dev-family/react-native-wallet-manager/pull/46 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@google/react-native-make-payment` | 0.002 | 4 | 1 | https://github.com/google-pay/react-native-make-payment/pull/111 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-drop-shadow` | 0.002 | 2 | 1 | https://github.com/hoanglam10499/react-native-drop-shadow/pull/47 |  |  |
| `react-native-ble-manager` | 0.002 | 2 | 1 | https://github.com/innoveit/react-native-ble-manager/pull/1434 |  |  |
| `klaviyo-react-native-sdk` | 0.002 | 2 | 1 | https://github.com/klaviyo/klaviyo-react-native-sdk/pull/416 | 2 |  |
| `react-native-nitro-fetch` | 0.002 | 4 | 3 | https://github.com/margelo/react-native-nitro-fetch/pull/230 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-avoid-softinput` | 0.002 | 2 | 1 | https://github.com/mateusz1913/react-native-avoid-softinput/pull/293 |  |  |
| `@mixpanel/react-native-session-replay` | 0.002 | 2 | 1 | https://github.com/mixpanel/mixpanel-react-native-session-replay/pull/82 |  |  |
| `react-native-tiktok-business-sdk` | 0.002 | 2 | 1 | https://github.com/mtebele/react-native-tiktok-business-sdk/pull/41 |  | Re-filed on a unique branch. The first attempt shared a fork branch with another repository of the same name and showed unrelated commits; that PR was closed with an explanation. |
| `@react-native-kakao/core` | 0.002 | 4 | 6 | https://github.com/mym0404/react-native-kakao/pull/78 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@pusher/pusher-websocket-react-native` | 0.002 | 2 | 1 | https://github.com/pusher/pusher-websocket-react-native/pull/219 |  |  |
| `@swmansion/react-native-bottom-sheet` | 0.002 | 2 | 1 | https://github.com/software-mansion-labs/react-native-bottom-sheet/pull/81 |  |  |
| `react-native-watch-connectivity` | 0.002 | 4 | 1 | https://github.com/watch-connectivity/react-native-watch-connectivity/pull/136 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-capture-protection` | 0.002 | 4 | 1 | https://github.com/wn-na/react-native-capture-protection/pull/134 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `clevertap-react-native` | 0.001 | 2 | 1 | https://github.com/CleverTap/clevertap-react-native/pull/521 | 2 |  |
| `react-native-performance-limiter` | 0.001 | 4 | 1 | https://github.com/DataDog/react-native-performance-limiter/pull/64 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@domir/react-native-measure-text` | 0.001 | 2 | 1 | https://github.com/DomiR/react-native-measure-text/pull/5 |  |  |
| `react-native-advanced-input-mask` | 0.001 | 2 | 1 | https://github.com/IvanIhnatsiuk/react-native-advanced-input-mask/pull/156 | 1 |  |
| `react-native-clusterer` | 0.001 | 4 | 1 | https://github.com/JiriHoffmann/react-native-clusterer/pull/70 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-nitro-markdown` | 0.001 | 4 | 1 | https://github.com/JoaoPauloCMarra/react-native-nitro-markdown/pull/76 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@lottiefiles/dotlottie-react-native` | 0.001 | 2 | 1 | https://github.com/LottieFiles/dotlottie-react-native/pull/84 | 1 |  |
| `@rokt/react-native-sdk` | 0.001 | 2 | 1 | https://github.com/ROKT/rokt-sdk-react-native/pull/301 | 3 |  |
| `react-native-android-location-enabler` | 0.001 | 4 | 1 | https://github.com/Richou/react-native-android-location-enabler/pull/111 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@simform_solutions/react-native-audio-waveform` | 0.001 | 2 | 1 | https://github.com/SimformSolutionsPvtLtd/react-native-audio-waveform/pull/215 |  |  |
| `@theoplayer/react-native-engage` | 0.001 | 2 | 11 | https://github.com/THEOplayer/react-native-connectors/pull/472 |  |  |
| `react-native-file-viewer-turbo` | 0.001 | 2 | 1 | https://github.com/Vadko/react-native-file-viewer-turbo/pull/44 |  |  |
| `react-native-background-upload` | 0.001 | 4 | 1 | https://github.com/Vydia/react-native-background-upload/pull/366 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-sherpa-onnx` | 0.001 | 3 | 1 | https://github.com/XDcobra/react-native-sherpa-onnx/pull/123 |  |  |
| `react-native-restart-newarch` | 0.001 | 3 | 1 | https://github.com/ahmedawaad1804/react-native-restart-newarch/pull/4 |  |  |
| `react-native-file-access` | 0.001 | 2 | 1 | https://github.com/alpha0010/react-native-file-access/pull/95 |  |  |
| `react-native-mmkv-storage` | 0.001 | 3 | 1 | https://github.com/ammarahm-ed/react-native-mmkv-storage/pull/393 | 1 |  |
| `react-native-appstack-sdk` | 0.001 | 2 | 1 | https://github.com/appstack-tech/react-native-appstack-sdk/pull/50 | 1 |  |
| `@bam.tech/react-native-app-security` | 0.001 | 4 | 1 | https://github.com/bamlab/react-native-app-security/pull/43 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@react-native-community/image-editor` | 0.001 | 2 | 1 | https://github.com/callstack/react-native-image-editor/pull/208 |  |  |
| `react-native-snackbar` | 0.001 | 3 | 1 | https://github.com/cooperka/react-native-snackbar/pull/219 |  |  |
| `@react-native-seoul/naver-login` | 0.001 | 4 | 1 | https://github.com/crossplatformkorea/react-native-naver-login/pull/255 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@siteed/audio-studio` | 0.001 | 2 | 4 | https://github.com/deeeed/audiolab/pull/489 | 1 |  |
| `@didit-protocol/sdk-react-native` | 0.001 | 4 | 1 | https://github.com/didit-protocol/sdk-react-native/pull/47 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-turbo-image` | 0.001 | 3 | 1 | https://github.com/duguyihou/react-native-turbo-image/pull/445 |  |  |
| `@embrace-io/react-native` | 0.001 | 2 | 3 | https://github.com/embrace-io/embrace-react-native-sdk/pull/1033 |  |  |
| `react-native-exponea-sdk` | 0.001 | 2 | 1 | https://github.com/exponea/exponea-react-native-sdk/pull/144 |  |  |
| `react-native-fast-squircle` | 0.001 | 4 | 1 | https://github.com/fbeccaceci/react-native-fast-squircle/pull/30 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@getcello/cello-react-native` | 0.001 | 2 | 1 | https://github.com/getcello/cello-react-native/pull/5 |  |  |
| `@googlemaps/react-native-navigation-sdk` | 0.001 | 4 | 1 | https://github.com/googlemaps/react-native-navigation-sdk/pull/644 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `expo-pdf-text-extract` | 0.001 | 2 | 1 | https://github.com/gr8pathik/expo-pdf-text-extract/pull/2 |  |  |
| `react-native-photo-manipulator` | 0.001 | 3 | 1 | https://github.com/guhungry/react-native-photo-manipulator/pull/1022 |  |  |
| `@ht-sdks/sovran-react-native` | 0.001 | 2 | 3 | https://github.com/ht-sdks/events-sdk-react-native/pull/74 | 1 |  |
| `react-native-nitro-sound` | 0.001 | 4 | 1 | https://github.com/hyochan/react-native-nitro-sound/pull/846 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@infinitered/react-native-mlkit-face-detection`, `@infinitered/react-native-mlkit-text-recognition` | 0.001 | 2 | 5 | https://github.com/infinitered/react-native-mlkit/pull/269 | 1 |  |
| `react-native-localization-settings` | 0.001 | 3 | 1 | https://github.com/jakex7/react-native-localization-settings/pull/37 |  |  |
| `react-native-system-navigation-bar` | 0.001 | 3 | 1 | https://github.com/kadiraydinli/react-native-system-navigation-bar/pull/83 |  |  |
| `react-native-klarna-inapp-sdk` | 0.001 | 4 | 4 | https://github.com/klarna/react-native-klarna-inapp-sdk/pull/388 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-nitro-cookies` | 0.001 | 4 | 1 | https://github.com/l2hyunwoo/react-native-nitro-cookies/pull/19 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-zendesk-messaging` | 0.001 | 4 | 1 | https://github.com/leegeunhyeok/react-native-zendesk-messaging/pull/98 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@logicwind/react-native-exit-app` | 0.001 | 2 | 1 | https://github.com/logicwind/react-native-exit-app/pull/9 |  |  |
| `react-native-fast-opencv` | 0.001 | 2 | 1 | https://github.com/lukaszkurantdev/react-native-fast-opencv/pull/118 |  |  |
| `react-native-sensitive-info` | 0.001 | 4 | 1 | https://github.com/mCodex/react-native-sensitive-info/pull/696 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-mparticle` | 0.001 | 4 | 1 | https://github.com/mParticle/react-native-mparticle/pull/384 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-blurhash` | 0.001 | 2 | 1 | https://github.com/margelo/react-native-blurhash/pull/213 |  |  |
| `vision-camera-resize-plugin` | 0.001 | 4 | 1 | https://github.com/mrousavy/vision-camera-resize-plugin/pull/98 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@mj-studio/react-native-naver-map` | 0.001 | 4 | 1 | https://github.com/mym0404/react-native-naver-map/pull/196 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `expo-dynamic-app-icon` | 0.001 | 4 | 1 | https://github.com/outsung/expo-dynamic-app-icon/pull/36 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-auto-skeleton` | 0.001 | 2 | 1 | https://github.com/pioner92/react-native-auto-skeleton/pull/21 |  |  |
| `@sbaiahmed1/react-native-biometrics` | 0.001 | 2 | 1 | https://github.com/sbaiahmed1/react-native-biometrics/pull/101 | 1 |  |
| `react-native-executorch` | 0.001 | 2 | 2 | https://github.com/software-mansion/react-native-executorch/pull/1412 | 1 |  |
| `react-native-pdf-thumbnail` | 0.001 | 4 | 1 | https://github.com/songsterq/react-native-pdf-thumbnail/pull/95 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@stripe/stripe-identity-react-native` | 0.001 | 4 | 1 | https://github.com/stripe/stripe-identity-react-native/pull/276 | 2 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `freerasp-react-native` | 0.001 | 4 | 1 | https://github.com/talsec/Free-RASP-ReactNative/pull/160 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-camera-kit` | 0.001 | 2 | 1 | https://github.com/teslamotors/react-native-camera-kit/pull/810 |  |  |
| `@ua/react-native-airship` | 0.001 | 4 | 1 | https://github.com/urbanairship/react-native-airship/pull/761 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `react-native-crisp-chat-sdk` | 0.001 | 2 | 1 | https://github.com/walterholohan/react-native-crisp-chat-sdk/pull/212 |  |  |
| `@xmartlabs/react-native-line` | 0.001 | 4 | 1 | https://github.com/xmartlabs/react-native-line/pull/225 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@dalbodeule/expo-app-integrity` | 0 | 3 | 1 | https://github.com/20203153/expo-app-integrity/pull/1 |  |  |
| `@2060.io/react-native-eid-reader` | 0 | 3 | 1 | https://github.com/2060-io/react-native-eid-reader/pull/68 |  |  |
| `@atomiqlab/react-native-mapbox-navigation` | 0 | 4 | 1 | https://github.com/ATOMIQTECH/react-native-mapbox-navigation/pull/21 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@alexzunik/react-native-money-input` | 0 | 3 | 1 | https://github.com/AleksandrNikolaevich/react-native-money-input/pull/8 |  |  |
| `@angelkrak/react-native-intent-launcher` | 0 | 3 | 1 | https://github.com/AngelKrak/react-native-intent-launcher/pull/1 |  |  |
| `@bitnet-infotech/react-native-razorpay-nitro` | 0 | 4 | 1 | https://github.com/BITNET-Infotech/react-native-razorpay-nitro/pull/1 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@bitnet-infotech/react-native-wav-to-mp3` | 0 | 3 | 1 | https://github.com/BITNET-Infotech/react-native-wav-to-mp3/pull/3 |  |  |
| `@babylonjs/react-native` | 0 | 3 | 1 | https://github.com/BabylonJS/BabylonReactNative/pull/745 |  |  |
| `@beatsphere/expo-apple-music-kit` | 0 | 4 | 1 | https://github.com/Beatsphere/expo-apple-music-kit/pull/1 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@b.taranenko/expo-color-thief` | 0 | 3 | 1 | https://github.com/BogdanTaranenko/expo-color-thief/pull/1 |  |  |
| `@bounceapp/react-native-paypal` | 0 | 3 | 1 | https://github.com/Bounceapp/react-native-paypal/pull/628 |  |  |
| `@bryandev/expo-mapbox-navigation` | 0 | 4 | 1 | https://github.com/BryanQuezada1910/expo-mapbox-navigation/pull/1 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@carlossts/react-native-leaflet-platform` | 0 | 3 | 1 | https://github.com/CarlosSTS/react-native-leaflet-platform/pull/12 |  |  |
| `@chaitrabhairappa/react-native-rich-text-editor` | 0 | 3 | 1 | https://github.com/Chaitra9225/react-native-richtext-editor/pull/5 |  |  |
| `@appcitor/react-native-voice-to-text` | 0 | 3 | 1 | https://github.com/ChathuraLiyanapathirana/react-native-voice-to-text/pull/3 |  | Re-filed on a unique branch. The first attempt shared a fork branch with another repository of the same name and showed unrelated commits; that PR was closed with an explanation. |
| `@doko/react-native-pdf-editor` | 0 | 4 | 1 | https://github.com/Doko-Demo-Doa/react-native-pdf-editor/pull/5 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@fressh/react-native-terminal` | 0 | 4 | 1 | https://github.com/EthanShoeDev/fressh/pull/17 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@expensify/react-native-wallet` | 0 | 4 | 1 | https://github.com/Expensify/react-native-wallet/pull/88 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@figuredev/react-native-local-server` | 0 | 3 | 1 | https://github.com/FigurePOS/react-native-local-server/pull/107 |  |  |
| `@fintecsystems/xs2a-react-native` | 0 | 3 | 1 | https://github.com/FinTecSystems/xs2a-react-native/pull/111 |  |  |
| `@gfean/react-native-bundle-drop` | 0 | 3 | 1 | https://github.com/GFean/react-native-bundle-drop/pull/35 |  |  |
| `@cohorly/react-native` | 0 | 3 | 1 | https://github.com/Gitarcitano/cohorly-js/pull/1 |  |  |
| `@grassper/react-native-icon-picker` | 0 | 3 | 1 | https://github.com/Grassper/react-native-icon-picker/pull/4 |  |  |
| `@baronha/react-native-multiple-image-picker` | 0 | 4 | 1 | https://github.com/NitrogenZLab/react-native-multiple-image-picker/pull/265 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@baronha/ting` | 0 | 4 | 1 | https://github.com/NitrogenZLab/ting/pull/44 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@gmessier/nitro-speech` | 0 | 4 | 1 | https://github.com/NotGeorgeMessier/nitro-speech/pull/16 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@dbkable/react-native-speech-to-text` | 0 | 3 | 1 | https://github.com/adelbeke/react-native-speech-to-text/pull/16 |  |  |
| `@ajitpatel28/react-native-truecaller` | 0 | 4 | 1 | https://github.com/ajitpatel28/react-native-truecaller/pull/8 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@akbaraditamasp/expo-lock-task` | 0 | 3 | 1 | https://github.com/akbaraditamasp/expo-lock-task/pull/2 |  |  |
| `@alvie-tech/react-native-tiktok-business-sdk` | 0 | 3 | 1 | https://github.com/alvie-tech/react-native-tiktok-business-sdk/pull/9 |  | Re-filed on a unique branch. The first attempt shared a fork branch with another repository of the same name and showed unrelated commits; that PR was closed with an explanation. |
| `@ammarahmed/react-native-upload` | 0 | 3 | 1 | https://github.com/ammarahm-ed/react-native-upload/pull/1 |  |  |
| `@ammarahmed/react-native-workers` | 0 | 4 | 3 | https://github.com/ammarahm-ed/react-native-workers/pull/2 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@and2long/react-native-uvc-camera` | 0 | 3 | 1 | https://github.com/and2long/react-native-uvc-camera/pull/7 |  |  |
| `@anorak-games/react-native-background-downloader` | 0 | 3 | 1 | https://github.com/anorak-games/react-native-background-downloader/pull/3 |  | Re-filed on a unique branch. The first attempt shared a fork branch with another repository of the same name and showed unrelated commits; that PR was closed with an explanation. |
| `@appandflow/expo-camera-characteristics` | 0 | 3 | 1 | https://github.com/appandflow/expo-camera-characteristics/pull/5 |  |  |
| `@appcues/expo-config` | 0 | 4 | 1 | https://github.com/appcues/appcues-expo-module/pull/21 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@appcues/react-native` | 0 | 4 | 1 | https://github.com/appcues/appcues-react-native-module/pull/234 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@apphud/react-native-apphud-sdk` | 0 | 4 | 1 | https://github.com/apphud/ApphudSDK-React-Native/pull/101 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@attarchi/react-native-lottie-splash-screen` | 0 | 4 | 1 | https://github.com/attarchi/react-native-lottie-splash-screen/pull/7 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@avasapp/react-native-app-intents` | 0 | 3 | 1 | https://github.com/avas-app/react-native-app-intents/pull/2 |  |  |
| `@aws/clickstream-react-native` | 0 | 3 | 1 | https://github.com/aws-solutions-library-samples/clickstream-analytics-on-aws-react-native-sdk/pull/23 |  |  |
| `@axeptio/react-native-sdk` | 0 | 4 | 1 | https://github.com/axeptio/react-native-sdk/pull/97 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@azizuysal/wallet-kit` | 0 | 3 | 1 | https://github.com/azizuysal/wallet-kit/pull/29 |  |  |
| `@baeckerherz/expo-mapbox-navigation` | 0 | 4 | 1 | https://github.com/baeckerherz/expo-mapbox-navigation/pull/1 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@bam.tech/react-native-ssl-pinning` | 0 | 4 | 1 | https://github.com/bamlab/react-native-ssl-pinning/pull/8 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@bernagl/react-native-date` | 0 | 4 | 1 | https://github.com/bbernag/react-native-date/pull/8 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@bear-block/vision-camera-ocr` | 0 | 4 | 1 | https://github.com/bear-block/vision-camera-ocr/pull/12 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@dr.pogodin/react-native-audio` | 0 | 3 | 1 | https://github.com/birdofpreyru/react-native-audio/pull/44 |  |  |
| `@dr.pogodin/react-native-static-server` | 0 | 3 | 1 | https://github.com/birdofpreyru/react-native-static-server/pull/167 |  |  |
| `@dr.pogodin/react-native-webview` | 0 | 3 | 1 | https://github.com/birdofpreyru/react-native-webview/pull/23 |  | Re-filed on a unique branch. The first attempt shared a fork branch with another repository of the same name and showed unrelated commits; that PR was closed with an explanation. |
| `@bitdrift/react-native` | 0 | 3 | 1 | https://github.com/bitdriftlabs/capture-es/pull/293 | 1 |  |
| `@blazejkustra/react-native-alert` | 0 | 4 | 1 | https://github.com/blazejkustra/react-native-alert/pull/8 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@bnnx/react-native-label-printer` | 0 | 3 | 1 | https://github.com/bnnx/react-native-label-printer/pull/2 |  |  |
| `@borndotcom/react-native-godot` | 0 | 4 | 1 | https://github.com/borndotcom/react-native-godot/pull/34 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@breeztech/breez-sdk-liquid-react-native` | 0 | 3 | 2 | https://github.com/breez/breez-sdk-liquid/pull/1107 |  |  |
| `@breeztech/breez-sdk-spark-react-native` | 0 | 3 | 2 | https://github.com/breez/spark-sdk/pull/1097 |  |  |
| `@brighthustle/react-native-usage-stats-manager` | 0 | 3 | 1 | https://github.com/bright-hustle/react-native-usage-stats-manager/pull/3 |  |  |
| `@bufgix/react-native-secure-window` | 0 | 4 | 1 | https://github.com/bufgix/react-native-secure-window/pull/3 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@buildonspark/spark-sdk` | 0 | 3 | 1 | https://github.com/buildonspark/spark/pull/151 |  |  |
| `@busanid/react-native-voip` | 0 | 4 | 1 | https://github.com/busanid/react-native-voip/pull/1 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@cafebazaar/react-native-poolakey` | 0 | 4 | 1 | https://github.com/cafebazaar/react-native-poolakey/pull/32 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@callstack/repack` | 0 | 3 | 1 | https://github.com/callstack/repack/pull/1453 | 2 |  |
| `@callstack/timezone-hermes-fix` | 0 | 3 | 1 | https://github.com/callstack/timezone-hermes-fix/pull/8 |  |  |
| `@candlefinance/blur-view` | 0 | 3 | 1 | https://github.com/candlefinance/blur-view/pull/5 |  |  |
| `@candlefinance/faster-image` | 0 | 3 | 1 | https://github.com/candlefinance/faster-image/pull/92 |  |  |
| `@candlefinance/haptics` | 0 | 3 | 1 | https://github.com/candlefinance/haptics/pull/4 |  |  |
| `@candlefinance/page-control` | 0 | 3 | 1 | https://github.com/candlefinance/page-control/pull/2 |  |  |
| `@castleio/react-native-castle` | 0 | 4 | 1 | https://github.com/castle/castle-react-native/pull/182 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@cleanuidev/react-native-scanner` | 0 | 3 | 1 | https://github.com/cleanui-dev/react-native-scanner/pull/7 |  |  |
| `@ecodevstack/react-native-mqtt-client` | 0 | 3 | 1 | https://github.com/cmcWebCode40/react-native-mqtt-client/pull/3 |  |  |
| `@coinbase/wallet-mobile-sdk` | 0 | 3 | 2 | https://github.com/coinbase/wallet-mobile-sdk/pull/12 |  |  |
| `@colloque/react-native-zendesk-messaging` | 0 | 4 | 1 | https://github.com/colloquet/react-native-zendesk-messaging/pull/1 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@cometchat/chat-uikit-react-native` | 0 | 3 | 1 | https://github.com/cometchat/cometchat-uikit-react-native/pull/114 |  |  |
| `@computools/react-native-dynamic-app-icon` | 0 | 4 | 1 | https://github.com/computools/react-native-dynamic-app-icon/pull/3 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@cjblack/expo-audio-stream` | 0 | 4 | 1 | https://github.com/connorblack/expo-audio-stream/pull/1 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@craftstudiodev/expo-tiktok-business` | 0 | 4 | 1 | https://github.com/craftstudiodev/expo-tiktok-business/pull/1 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@criipto/verify-expo` | 0 | 4 | 1 | https://github.com/criipto/criipto-verify-expo/pull/41 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. Re-pushed to preserve the file's CRLF line endings. |
| `@guulabs/react-native-app-badge` | 0 | 3 | 1 | https://github.com/cristiangu/react-native-app-badge/pull/1 |  |  |
| `@dariyd/react-native-image-description` | 0 | 4 | 1 | https://github.com/dariyd/react-native-image-description/pull/1 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@dariyd/react-native-pdf-page-image` | 0 | 3 | 1 | https://github.com/dariyd/react-native-pdf-page-image/pull/2 |  |  |
| `@dariyd/react-native-text-recognition` | 0 | 3 | 1 | https://github.com/dariyd/react-native-text-recognition/pull/4 |  |  |
| `@dasimems/react-native-svga` | 0 | 4 | 1 | https://github.com/dasimems/react-native-svga/pull/2 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@dawidzawada/bonjour-zeroconf` | 0 | 4 | 1 | https://github.com/dawidzawada/bonjour-zeroconf/pull/1 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@everuribe/expo-audio-studio` | 0 | 4 | 4 | https://github.com/deeeed/audiolab/pull/490 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@dengage-tech/react-native-dengage` | 0 | 3 | 1 | https://github.com/dengage-tech/dengage-react-sdk/pull/15 |  |  |
| `@descope/react-native-sdk` | 0 | 3 | 1 | https://github.com/descope/descope-react-native/pull/186 | 3 |  |
| `@deuna/react-native-sdk` | 0 | 3 | 1 | https://github.com/deuna-developers/deuna-sdk-react-native/pull/1 |  |  |
| `@dev-amirzubair/react-native-voice` | 0 | 3 | 1 | https://github.com/dev-amirzubair/voice/pull/2 |  |  |
| `@didomi/react-native` | 0 | 3 | 1 | https://github.com/didomi/react-native/pull/188 |  |  |
| `@dodopayments/react-native-checkout` | 0 | 4 | 2 | https://github.com/dodopayments/dodopayments-mobile-sdk/pull/25 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@dolami-inc/react-native-expo-unity` | 0 | 4 | 1 | https://github.com/dolami-inc/react-native-expo-unity/pull/8 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@doorstepai/dropoff-sdk` | 0 | 4 | 1 | https://github.com/doorstep-ai/DoorstepAIDropoffReactNativeSDK/pull/1 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@dpdpguard/react-native` | 0 | 3 | 1 | https://github.com/dpdp-guard-ai/dpdpguard-react-native-sdk/pull/3 |  |  |
| `@dub/react-native` | 0 | 4 | 1 | https://github.com/dubinc/dub-react-native/pull/5 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@ebrimasamba/react-native-prompt` | 0 | 3 | 1 | https://github.com/ebrimasamba/react-native-prompt/pull/1 |  |  |
| `@ebrimasamba/react-native-sms-retriever` | 0 | 3 | 1 | https://github.com/ebrimasamba/react-native-sms-retriever/pull/3 |  |  |
| `@edkimmel/expo-audio-stream` | 0 | 4 | 1 | https://github.com/edkimmel/expo-audio-stream/pull/4 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@edritech93/react-native-datawedge-intents` | 0 | 3 | 1 | https://github.com/edritech93/react-native-datawedge-intents/pull/3 |  |  |
| `@eitjuh/expo-apple-intelligence` | 0 | 4 | 1 | https://github.com/eitjuh/expo-apple-intelligence/pull/1 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@entrig/react-native` | 0 | 3 | 1 | https://github.com/entrig/entrig-react-native/pull/1 |  |  |
| `@evervault/evervault-react-native`, `@evervault/react-native` | 0 | 3 | 2 | https://github.com/evervault/evervault-js/pull/1005 | 1 |  |
| `@extole/react-native-sdk` | 0 | 4 | 1 | https://github.com/extole/react-native-sdk/pull/5 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@filipfrlic/expo-google-signin` | 0 | 4 | 1 | https://github.com/filipfrlic/expo-google-signin/pull/1 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@fishjam-cloud/react-native-webrtc` | 0 | 3 | 1 | https://github.com/fishjam-cloud/fishjam-react-native-webrtc/pull/85 |  |  |
| `@fivecar/react-native-background-downloader` | 0 | 3 | 1 | https://github.com/fivecar/react-native-background-downloader/pull/3 |  | Re-filed on a unique branch. The first attempt shared a fork branch with another repository of the same name and showed unrelated commits; that PR was closed with an explanation. |
| `@foursquare/movement-sdk-react-native` | 0 | 4 | 1 | https://github.com/foursquare/movement-sdk-react-native/pull/21 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@frontegg/react-native` | 0 | 4 | 1 | https://github.com/frontegg/frontegg-react-native/pull/131 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@gabriel-sisjr/react-native-background-location` | 0 | 4 | 1 | https://github.com/gabriel-sisjr/react-native-background-location/pull/50 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@gmisoftware/react-native-pay` | 0 | 4 | 1 | https://github.com/gmi-software/react-native-pay/pull/5 | 1 | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@grafana/faro-react-native` | 0 | 3 | 1 | https://github.com/grafana/faro-react-native-sdk/pull/191 | 1 |  |
| `@grupalia/react-native-photo-picker` | 0 | 4 | 1 | https://github.com/grupalia/react-native-photo-picker/pull/1 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@bittingz/expo-native-fonts` | 0 | 4 | 1 | https://github.com/mike-stewart-dev/expo-native-fonts/pull/9 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |
| `@arkyutao/react-native-mqtt` | 0 | 3 | 1 | https://github.com/return764/react-native-mqtt/pull/2 |  |  |
| `@ascendtis/react-native-voice-to-text` | 0 | 3 | 1 | https://github.com/sufyan297/react-native-voice-to-text/pull/2 |  | Re-filed on a unique branch. The first attempt shared a fork branch with another repository of the same name and showed unrelated commits; that PR was closed with an explanation. |
| `@badatgil/expo-mapbox-navigation` | 0 | 4 | 1 | https://github.com/uju777/expo-mapbox-navigation/pull/44 |  | Hidden collision: the flagged build died on the Kotlin collision but the harness filed it fail-baseline because the fallback build also failed for an unrelated reason. |

## Merged (22)

| Package(s) | Usage | Round | Files | PR | Merged | Note |
|---|---|---|---|---|---|---|
| `react-native-purchases` | 0.136 | 1 | 1 | https://github.com/RevenueCat/react-native-purchases/pull/1934 | 2026-09-03 | Maintainer asked for the extension check instead of the version table; switched, then merged. Round 2 follows their shape. |
| `@react-native-google-signin/google-signin` | 0.132 | 1 | 1 | https://github.com/react-native-google-signin/google-signin/pull/1524 | 2026-09-03 |  |
| `@maplibre/maplibre-react-native` | 0.017 | 1 | 1 | https://github.com/maplibre/maplibre-react-native/pull/1645 | 2026-09-05 |  |
| `@lodev09/react-native-true-sheet` | 0.012 | 1 | 1 | https://github.com/lodev09/react-native-true-sheet/pull/819 | 2026-09-02 |  |
| `react-native-enriched-markdown` | 0.011 | 1 | 1 | https://github.com/software-mansion/enriched-markdown/pull/744 | 2026-09-03 |  |
| `@op-engineering/op-sqlite` | 0.01 | 1 | 1 | https://github.com/OP-Engineering/op-sqlite/pull/447 | 2026-09-05 |  |
| `@preeternal/react-native-cookie-manager` | 0.009 | 2 | 1 | https://github.com/Preeternal/react-native-cookie-manager/pull/5 | 2026-09-04 |  |
| `@posthog/react-native-plugin` | 0.007 | 2 | 2 | https://github.com/PostHog/posthog-js/pull/4789 | 2026-09-05 | Maintainer asked for a changeset (added) and signed commits (done; both commits verify). Awaiting review approval. |
| `react-native-volume-manager` | 0.007 | 2 | 1 | https://github.com/hirbod/react-native-volume-manager/pull/63 | 2026-09-04 |  |
| `react-native-navigation-mode` | 0.003 | 2 | 1 | https://github.com/JairajJangle/react-native-navigation-mode/pull/28 | 2026-09-04 |  |
| `react-native-video-trim` | 0.003 | 2 | 1 | https://github.com/maitrungduc1410/react-native-video-trim/pull/141 | 2026-09-04 |  |
| `react-native-pulsar` | 0.003 | 2 | 1 | https://github.com/software-mansion/pulsar/pull/258 | 2026-09-05 |  |
| `@dr.pogodin/react-native-fs` | 0.002 | 2 | 1 | https://github.com/birdofpreyru/react-native-fs/pull/161 | 2026-09-04 |  |
| `@clerk/expo-google-signin`, `@clerk/expo-passkeys` | 0.002 | 2 | 3 | https://github.com/clerk/javascript/pull/9662 | 2026-09-04 |  |
| `react-native-fast-rsa` | 0.002 | 2 | 1 | https://github.com/jerson/react-native-fast-rsa/pull/101 | 2026-09-04 |  |
| `@sbaiahmed1/react-native-blur` | 0.002 | 2 | 1 | https://github.com/sbaiahmed1/react-native-blur/pull/165 | 2026-09-04 |  |
| `react-native-screenshot-aware` | 0.001 | 3 | 1 | https://github.com/huextrat/react-native-screenshot-aware/pull/613 | 2026-09-05 |  |
| `@kesha-antonov/react-native-background-downloader` | 0.001 | 2 | 1 | https://github.com/kesha-antonov/react-native-background-downloader/pull/178 | 2026-09-05 | Re-filed on a unique branch. The first attempt shared a fork branch with another repository of the same name and showed unrelated commits; that PR was closed with an explanation. |
| `react-native-cloud-storage` | 0.001 | 2 | 1 | https://github.com/kuatsu/react-native-cloud-storage/pull/85 | 2026-09-04 |  |
| `@mattermost/react-native-paste-input` | 0.001 | 2 | 1 | https://github.com/mattermost/react-native-paste-input/pull/57 | 2026-09-05 |  |
| `@dongminyu/react-native-step-counter` | 0 | 3 | 1 | https://github.com/AndrewDongminYoo/react-native-step-counter/pull/66 | 2026-09-05 |  |
| `@angelcat/react-native-honeywell-barcode-scanner` | 0 | 3 | 1 | https://github.com/Ky0-Nguyen/react-native-honeywell-barcode-scanner/pull/1 | 2026-09-05 |  |

## Closed without merging (2)

Check each one: so far every closure has been a maintainer taking the change
through their own process rather than rejecting it.

| Package(s) | Usage | Round | Files | PR | Discussion | Note |
|---|---|---|---|---|---|---|
| `@atomicfi/transact-react-native` | 0.004 | 2 | 1 | https://github.com/atomicfi/atomic-transact-react-native/pull/197 | 1 | Closed on company policy: external PRs go through their internal workflow. Maintainer confirmed they are applying the change. |
| `@clerk/expo-google-signin`, `@clerk/expo-passkeys` | 0.002 | 2 | 2 | https://github.com/clerk/javascript/pull/9660 | 4 | Closed in favour of clerk/javascript#9662, which merged with the same guard and credits us as co-author. Clerk is fixed. |

