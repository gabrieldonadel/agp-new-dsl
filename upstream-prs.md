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
| open | 163 |
| merged | 16 |
| closed | 2 |
| **total** | **181** |

181 pull requests covering 199 packages.

## Pending (163)

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
| `@phantom/react-native-webview` | 0.003 | 2 | 1 | https://github.com/phantom/react-native-webview/pull/57 |  | Re-filed on a unique branch. The first attempt shared a fork branch with another repository of the same name and showed unrelated commits; that PR was closed with an explanation. |
| `@powersync/op-sqlite`, `@powersync/react-native` | 0.003 | 2 | 1 | https://github.com/powersync-ja/powersync-js/pull/1091 | 2 |  |
| `react-native-nano-icons` | 0.003 | 2 | 1 | https://github.com/software-mansion-labs/react-native-nano-icons/pull/56 |  |  |
| `react-native-pulsar` | 0.003 | 2 | 1 | https://github.com/software-mansion/pulsar/pull/258 |  |  |
| `react-native-enriched`, `react-native-enriched-html` | 0.003 | 2 | 1 | https://github.com/software-mansion/react-native-enriched-html/pull/787 |  |  |
| `react-native-sound` | 0.003 | 2 | 1 | https://github.com/zmxv/react-native-sound/pull/899 |  |  |
| `@stream-io/react-native-webrtc` | 0.002 | 2 | 1 | https://github.com/GetStream/react-native-webrtc/pull/67 |  | Re-filed on a unique branch. The first attempt shared a fork branch with another repository of the same name and showed unrelated commits; that PR was closed with an explanation. |
| `@giphy/react-native-sdk` | 0.002 | 2 | 1 | https://github.com/Giphy/giphy-react-native-sdk/pull/229 |  |  |
| `@walletconnect/react-native-compat` | 0.002 | 2 | 1 | https://github.com/WalletConnect/walletconnect-monorepo/pull/7335 | 2 |  |
| `react-native-adapty` | 0.002 | 2 | 1 | https://github.com/adaptyteam/AdaptySDK-React-Native/pull/340 | 2 |  |
| `react-native-drop-shadow` | 0.002 | 2 | 1 | https://github.com/hoanglam10499/react-native-drop-shadow/pull/47 |  |  |
| `react-native-ble-manager` | 0.002 | 2 | 1 | https://github.com/innoveit/react-native-ble-manager/pull/1434 |  |  |
| `klaviyo-react-native-sdk` | 0.002 | 2 | 1 | https://github.com/klaviyo/klaviyo-react-native-sdk/pull/416 | 2 |  |
| `react-native-avoid-softinput` | 0.002 | 2 | 1 | https://github.com/mateusz1913/react-native-avoid-softinput/pull/293 |  |  |
| `@mixpanel/react-native-session-replay` | 0.002 | 2 | 1 | https://github.com/mixpanel/mixpanel-react-native-session-replay/pull/82 |  |  |
| `react-native-tiktok-business-sdk` | 0.002 | 2 | 1 | https://github.com/mtebele/react-native-tiktok-business-sdk/pull/41 |  | Re-filed on a unique branch. The first attempt shared a fork branch with another repository of the same name and showed unrelated commits; that PR was closed with an explanation. |
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
| `react-native-sherpa-onnx` | 0.001 | 3 | 1 | https://github.com/XDcobra/react-native-sherpa-onnx/pull/123 |  |  |
| `react-native-restart-newarch` | 0.001 | 3 | 1 | https://github.com/ahmedawaad1804/react-native-restart-newarch/pull/4 |  |  |
| `react-native-file-access` | 0.001 | 2 | 1 | https://github.com/alpha0010/react-native-file-access/pull/95 |  |  |
| `react-native-mmkv-storage` | 0.001 | 3 | 1 | https://github.com/ammarahm-ed/react-native-mmkv-storage/pull/393 | 1 |  |
| `react-native-appstack-sdk` | 0.001 | 2 | 1 | https://github.com/appstack-tech/react-native-appstack-sdk/pull/50 | 1 |  |
| `@react-native-community/image-editor` | 0.001 | 2 | 1 | https://github.com/callstack/react-native-image-editor/pull/208 |  |  |
| `react-native-snackbar` | 0.001 | 3 | 1 | https://github.com/cooperka/react-native-snackbar/pull/219 |  |  |
| `@siteed/audio-studio` | 0.001 | 2 | 4 | https://github.com/deeeed/audiolab/pull/489 | 1 |  |
| `react-native-turbo-image` | 0.001 | 3 | 1 | https://github.com/duguyihou/react-native-turbo-image/pull/445 |  |  |
| `@embrace-io/react-native` | 0.001 | 2 | 3 | https://github.com/embrace-io/embrace-react-native-sdk/pull/1033 |  |  |
| `react-native-exponea-sdk` | 0.001 | 2 | 1 | https://github.com/exponea/exponea-react-native-sdk/pull/144 |  |  |
| `@getcello/cello-react-native` | 0.001 | 2 | 1 | https://github.com/getcello/cello-react-native/pull/5 |  |  |
| `expo-pdf-text-extract` | 0.001 | 2 | 1 | https://github.com/gr8pathik/expo-pdf-text-extract/pull/2 |  |  |
| `react-native-photo-manipulator` | 0.001 | 3 | 1 | https://github.com/guhungry/react-native-photo-manipulator/pull/1022 |  |  |
| `@ht-sdks/sovran-react-native` | 0.001 | 2 | 3 | https://github.com/ht-sdks/events-sdk-react-native/pull/74 | 1 |  |
| `react-native-screenshot-aware` | 0.001 | 3 | 1 | https://github.com/huextrat/react-native-screenshot-aware/pull/613 |  |  |
| `@infinitered/react-native-mlkit-face-detection`, `@infinitered/react-native-mlkit-text-recognition` | 0.001 | 2 | 5 | https://github.com/infinitered/react-native-mlkit/pull/269 | 1 |  |
| `react-native-localization-settings` | 0.001 | 3 | 1 | https://github.com/jakex7/react-native-localization-settings/pull/37 |  |  |
| `react-native-system-navigation-bar` | 0.001 | 3 | 1 | https://github.com/kadiraydinli/react-native-system-navigation-bar/pull/83 |  |  |
| `@kesha-antonov/react-native-background-downloader` | 0.001 | 2 | 1 | https://github.com/kesha-antonov/react-native-background-downloader/pull/178 |  | Re-filed on a unique branch. The first attempt shared a fork branch with another repository of the same name and showed unrelated commits; that PR was closed with an explanation. |
| `@logicwind/react-native-exit-app` | 0.001 | 2 | 1 | https://github.com/logicwind/react-native-exit-app/pull/9 |  |  |
| `react-native-fast-opencv` | 0.001 | 2 | 1 | https://github.com/lukaszkurantdev/react-native-fast-opencv/pull/118 |  |  |
| `react-native-blurhash` | 0.001 | 2 | 1 | https://github.com/margelo/react-native-blurhash/pull/213 |  |  |
| `react-native-auto-skeleton` | 0.001 | 2 | 1 | https://github.com/pioner92/react-native-auto-skeleton/pull/21 |  |  |
| `@sbaiahmed1/react-native-biometrics` | 0.001 | 2 | 1 | https://github.com/sbaiahmed1/react-native-biometrics/pull/101 | 1 |  |
| `react-native-executorch` | 0.001 | 2 | 2 | https://github.com/software-mansion/react-native-executorch/pull/1412 | 1 |  |
| `react-native-camera-kit` | 0.001 | 2 | 1 | https://github.com/teslamotors/react-native-camera-kit/pull/810 |  |  |
| `react-native-crisp-chat-sdk` | 0.001 | 2 | 1 | https://github.com/walterholohan/react-native-crisp-chat-sdk/pull/212 |  |  |
| `@dalbodeule/expo-app-integrity` | 0 | 3 | 1 | https://github.com/20203153/expo-app-integrity/pull/1 |  |  |
| `@2060.io/react-native-eid-reader` | 0 | 3 | 1 | https://github.com/2060-io/react-native-eid-reader/pull/68 |  |  |
| `@alexzunik/react-native-money-input` | 0 | 3 | 1 | https://github.com/AleksandrNikolaevich/react-native-money-input/pull/8 |  |  |
| `@dongminyu/react-native-step-counter` | 0 | 3 | 1 | https://github.com/AndrewDongminYoo/react-native-step-counter/pull/66 | 2 |  |
| `@angelkrak/react-native-intent-launcher` | 0 | 3 | 1 | https://github.com/AngelKrak/react-native-intent-launcher/pull/1 |  |  |
| `@bitnet-infotech/react-native-wav-to-mp3` | 0 | 3 | 1 | https://github.com/BITNET-Infotech/react-native-wav-to-mp3/pull/3 |  |  |
| `@babylonjs/react-native` | 0 | 3 | 1 | https://github.com/BabylonJS/BabylonReactNative/pull/745 |  |  |
| `@b.taranenko/expo-color-thief` | 0 | 3 | 1 | https://github.com/BogdanTaranenko/expo-color-thief/pull/1 |  |  |
| `@bounceapp/react-native-paypal` | 0 | 3 | 1 | https://github.com/Bounceapp/react-native-paypal/pull/628 |  |  |
| `@carlossts/react-native-leaflet-platform` | 0 | 3 | 1 | https://github.com/CarlosSTS/react-native-leaflet-platform/pull/12 |  |  |
| `@chaitrabhairappa/react-native-rich-text-editor` | 0 | 3 | 1 | https://github.com/Chaitra9225/react-native-richtext-editor/pull/5 |  |  |
| `@appcitor/react-native-voice-to-text` | 0 | 3 | 1 | https://github.com/ChathuraLiyanapathirana/react-native-voice-to-text/pull/3 |  | Re-filed on a unique branch. The first attempt shared a fork branch with another repository of the same name and showed unrelated commits; that PR was closed with an explanation. |
| `@figuredev/react-native-local-server` | 0 | 3 | 1 | https://github.com/FigurePOS/react-native-local-server/pull/107 |  |  |
| `@fintecsystems/xs2a-react-native` | 0 | 3 | 1 | https://github.com/FinTecSystems/xs2a-react-native/pull/111 |  |  |
| `@gfean/react-native-bundle-drop` | 0 | 3 | 1 | https://github.com/GFean/react-native-bundle-drop/pull/35 |  |  |
| `@cohorly/react-native` | 0 | 3 | 1 | https://github.com/Gitarcitano/cohorly-js/pull/1 |  |  |
| `@grassper/react-native-icon-picker` | 0 | 3 | 1 | https://github.com/Grassper/react-native-icon-picker/pull/4 |  |  |
| `@angelcat/react-native-honeywell-barcode-scanner` | 0 | 3 | 1 | https://github.com/Ky0-Nguyen/react-native-honeywell-barcode-scanner/pull/1 |  |  |
| `@dbkable/react-native-speech-to-text` | 0 | 3 | 1 | https://github.com/adelbeke/react-native-speech-to-text/pull/16 |  |  |
| `@akbaraditamasp/expo-lock-task` | 0 | 3 | 1 | https://github.com/akbaraditamasp/expo-lock-task/pull/2 |  |  |
| `@alvie-tech/react-native-tiktok-business-sdk` | 0 | 3 | 1 | https://github.com/alvie-tech/react-native-tiktok-business-sdk/pull/9 |  | Re-filed on a unique branch. The first attempt shared a fork branch with another repository of the same name and showed unrelated commits; that PR was closed with an explanation. |
| `@ammarahmed/react-native-upload` | 0 | 3 | 1 | https://github.com/ammarahm-ed/react-native-upload/pull/1 |  |  |
| `@and2long/react-native-uvc-camera` | 0 | 3 | 1 | https://github.com/and2long/react-native-uvc-camera/pull/7 |  |  |
| `@anorak-games/react-native-background-downloader` | 0 | 3 | 1 | https://github.com/anorak-games/react-native-background-downloader/pull/3 |  | Re-filed on a unique branch. The first attempt shared a fork branch with another repository of the same name and showed unrelated commits; that PR was closed with an explanation. |
| `@appandflow/expo-camera-characteristics` | 0 | 3 | 1 | https://github.com/appandflow/expo-camera-characteristics/pull/5 |  |  |
| `@avasapp/react-native-app-intents` | 0 | 3 | 1 | https://github.com/avas-app/react-native-app-intents/pull/2 |  |  |
| `@aws/clickstream-react-native` | 0 | 3 | 1 | https://github.com/aws-solutions-library-samples/clickstream-analytics-on-aws-react-native-sdk/pull/23 |  |  |
| `@azizuysal/wallet-kit` | 0 | 3 | 1 | https://github.com/azizuysal/wallet-kit/pull/29 |  |  |
| `@dr.pogodin/react-native-audio` | 0 | 3 | 1 | https://github.com/birdofpreyru/react-native-audio/pull/44 |  |  |
| `@dr.pogodin/react-native-static-server` | 0 | 3 | 1 | https://github.com/birdofpreyru/react-native-static-server/pull/167 |  |  |
| `@dr.pogodin/react-native-webview` | 0 | 3 | 1 | https://github.com/birdofpreyru/react-native-webview/pull/23 |  | Re-filed on a unique branch. The first attempt shared a fork branch with another repository of the same name and showed unrelated commits; that PR was closed with an explanation. |
| `@bitdrift/react-native` | 0 | 3 | 1 | https://github.com/bitdriftlabs/capture-es/pull/293 | 1 |  |
| `@bnnx/react-native-label-printer` | 0 | 3 | 1 | https://github.com/bnnx/react-native-label-printer/pull/2 |  |  |
| `@breeztech/breez-sdk-liquid-react-native` | 0 | 3 | 2 | https://github.com/breez/breez-sdk-liquid/pull/1107 |  |  |
| `@breeztech/breez-sdk-spark-react-native` | 0 | 3 | 2 | https://github.com/breez/spark-sdk/pull/1097 |  |  |
| `@brighthustle/react-native-usage-stats-manager` | 0 | 3 | 1 | https://github.com/bright-hustle/react-native-usage-stats-manager/pull/3 |  |  |
| `@buildonspark/spark-sdk` | 0 | 3 | 1 | https://github.com/buildonspark/spark/pull/151 |  |  |
| `@callstack/repack` | 0 | 3 | 1 | https://github.com/callstack/repack/pull/1453 | 2 |  |
| `@callstack/timezone-hermes-fix` | 0 | 3 | 1 | https://github.com/callstack/timezone-hermes-fix/pull/8 |  |  |
| `@candlefinance/blur-view` | 0 | 3 | 1 | https://github.com/candlefinance/blur-view/pull/5 |  |  |
| `@candlefinance/faster-image` | 0 | 3 | 1 | https://github.com/candlefinance/faster-image/pull/92 |  |  |
| `@candlefinance/haptics` | 0 | 3 | 1 | https://github.com/candlefinance/haptics/pull/4 |  |  |
| `@candlefinance/page-control` | 0 | 3 | 1 | https://github.com/candlefinance/page-control/pull/2 |  |  |
| `@cleanuidev/react-native-scanner` | 0 | 3 | 1 | https://github.com/cleanui-dev/react-native-scanner/pull/7 |  |  |
| `@ecodevstack/react-native-mqtt-client` | 0 | 3 | 1 | https://github.com/cmcWebCode40/react-native-mqtt-client/pull/3 |  |  |
| `@coinbase/wallet-mobile-sdk` | 0 | 3 | 2 | https://github.com/coinbase/wallet-mobile-sdk/pull/12 |  |  |
| `@cometchat/chat-uikit-react-native` | 0 | 3 | 1 | https://github.com/cometchat/cometchat-uikit-react-native/pull/114 |  |  |
| `@guulabs/react-native-app-badge` | 0 | 3 | 1 | https://github.com/cristiangu/react-native-app-badge/pull/1 |  |  |
| `@dariyd/react-native-pdf-page-image` | 0 | 3 | 1 | https://github.com/dariyd/react-native-pdf-page-image/pull/2 |  |  |
| `@dariyd/react-native-text-recognition` | 0 | 3 | 1 | https://github.com/dariyd/react-native-text-recognition/pull/4 |  |  |
| `@dengage-tech/react-native-dengage` | 0 | 3 | 1 | https://github.com/dengage-tech/dengage-react-sdk/pull/15 |  |  |
| `@descope/react-native-sdk` | 0 | 3 | 1 | https://github.com/descope/descope-react-native/pull/186 | 3 |  |
| `@deuna/react-native-sdk` | 0 | 3 | 1 | https://github.com/deuna-developers/deuna-sdk-react-native/pull/1 |  |  |
| `@dev-amirzubair/react-native-voice` | 0 | 3 | 1 | https://github.com/dev-amirzubair/voice/pull/2 |  |  |
| `@didomi/react-native` | 0 | 3 | 1 | https://github.com/didomi/react-native/pull/188 |  |  |
| `@dpdpguard/react-native` | 0 | 3 | 1 | https://github.com/dpdp-guard-ai/dpdpguard-react-native-sdk/pull/3 |  |  |
| `@ebrimasamba/react-native-prompt` | 0 | 3 | 1 | https://github.com/ebrimasamba/react-native-prompt/pull/1 |  |  |
| `@ebrimasamba/react-native-sms-retriever` | 0 | 3 | 1 | https://github.com/ebrimasamba/react-native-sms-retriever/pull/3 |  |  |
| `@edritech93/react-native-datawedge-intents` | 0 | 3 | 1 | https://github.com/edritech93/react-native-datawedge-intents/pull/3 |  |  |
| `@entrig/react-native` | 0 | 3 | 1 | https://github.com/entrig/entrig-react-native/pull/1 |  |  |
| `@evervault/evervault-react-native`, `@evervault/react-native` | 0 | 3 | 2 | https://github.com/evervault/evervault-js/pull/1005 | 1 |  |
| `@fishjam-cloud/react-native-webrtc` | 0 | 3 | 1 | https://github.com/fishjam-cloud/fishjam-react-native-webrtc/pull/85 |  |  |
| `@fivecar/react-native-background-downloader` | 0 | 3 | 1 | https://github.com/fivecar/react-native-background-downloader/pull/3 |  | Re-filed on a unique branch. The first attempt shared a fork branch with another repository of the same name and showed unrelated commits; that PR was closed with an explanation. |
| `@grafana/faro-react-native` | 0 | 3 | 1 | https://github.com/grafana/faro-react-native-sdk/pull/191 | 1 |  |
| `@arkyutao/react-native-mqtt` | 0 | 3 | 1 | https://github.com/return764/react-native-mqtt/pull/2 |  |  |
| `@ascendtis/react-native-voice-to-text` | 0 | 3 | 1 | https://github.com/sufyan297/react-native-voice-to-text/pull/2 |  | Re-filed on a unique branch. The first attempt shared a fork branch with another repository of the same name and showed unrelated commits; that PR was closed with an explanation. |

## Merged (16)

| Package(s) | Usage | Round | Files | PR | Merged | Note |
|---|---|---|---|---|---|---|
| `react-native-purchases` | 0.136 | 1 | 1 | https://github.com/RevenueCat/react-native-purchases/pull/1934 | 2026-09-03 | Maintainer asked for the extension check instead of the version table; switched, then merged. Round 2 follows their shape. |
| `@react-native-google-signin/google-signin` | 0.132 | 1 | 1 | https://github.com/react-native-google-signin/google-signin/pull/1524 | 2026-09-03 |  |
| `@maplibre/maplibre-react-native` | 0.017 | 1 | 1 | https://github.com/maplibre/maplibre-react-native/pull/1645 | 2026-09-05 |  |
| `@lodev09/react-native-true-sheet` | 0.012 | 1 | 1 | https://github.com/lodev09/react-native-true-sheet/pull/819 | 2026-09-02 |  |
| `react-native-enriched-markdown` | 0.011 | 1 | 1 | https://github.com/software-mansion/enriched-markdown/pull/744 | 2026-09-03 |  |
| `@preeternal/react-native-cookie-manager` | 0.009 | 2 | 1 | https://github.com/Preeternal/react-native-cookie-manager/pull/5 | 2026-09-04 |  |
| `@posthog/react-native-plugin` | 0.007 | 2 | 2 | https://github.com/PostHog/posthog-js/pull/4789 | 2026-09-05 | Maintainer asked for a changeset (added) and signed commits (done; both commits verify). Awaiting review approval. |
| `react-native-volume-manager` | 0.007 | 2 | 1 | https://github.com/hirbod/react-native-volume-manager/pull/63 | 2026-09-04 |  |
| `react-native-navigation-mode` | 0.003 | 2 | 1 | https://github.com/JairajJangle/react-native-navigation-mode/pull/28 | 2026-09-04 |  |
| `react-native-video-trim` | 0.003 | 2 | 1 | https://github.com/maitrungduc1410/react-native-video-trim/pull/141 | 2026-09-04 |  |
| `@dr.pogodin/react-native-fs` | 0.002 | 2 | 1 | https://github.com/birdofpreyru/react-native-fs/pull/161 | 2026-09-04 |  |
| `@clerk/expo-google-signin`, `@clerk/expo-passkeys` | 0.002 | 2 | 3 | https://github.com/clerk/javascript/pull/9662 | 2026-09-04 |  |
| `react-native-fast-rsa` | 0.002 | 2 | 1 | https://github.com/jerson/react-native-fast-rsa/pull/101 | 2026-09-04 |  |
| `@sbaiahmed1/react-native-blur` | 0.002 | 2 | 1 | https://github.com/sbaiahmed1/react-native-blur/pull/165 | 2026-09-04 |  |
| `react-native-cloud-storage` | 0.001 | 2 | 1 | https://github.com/kuatsu/react-native-cloud-storage/pull/85 | 2026-09-04 |  |
| `@mattermost/react-native-paste-input` | 0.001 | 2 | 1 | https://github.com/mattermost/react-native-paste-input/pull/57 | 2026-09-05 |  |

## Closed without merging (2)

Check each one: so far every closure has been a maintainer taking the change
through their own process rather than rejecting it.

| Package(s) | Usage | Round | Files | PR | Discussion | Note |
|---|---|---|---|---|---|---|
| `@atomicfi/transact-react-native` | 0.004 | 2 | 1 | https://github.com/atomicfi/atomic-transact-react-native/pull/197 | 1 | Closed on company policy: external PRs go through their internal workflow. Maintainer confirmed they are applying the change. |
| `@clerk/expo-google-signin`, `@clerk/expo-passkeys` | 0.002 | 2 | 2 | https://github.com/clerk/javascript/pull/9660 | 4 | Closed in favour of clerk/javascript#9662, which merged with the same guard and credits us as co-author. Clerk is fixed. |

