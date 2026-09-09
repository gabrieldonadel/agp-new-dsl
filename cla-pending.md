# Pull requests waiting on a CLA

**None. All 13 pull requests that ever showed a CLA signal are now clear.**

| PR | CLA state |
|---|---|
| stripe/stripe-react-native#2602 | success |
| stripe/stripe-terminal-react-native#1134 | success |
| stripe/stripe-identity-react-native#276 | success |
| Expensify/react-native-wallet#88 | success |
| adobe/aepsdk-react-native#591 | success |
| google-pay/react-native-make-payment#111 | success, merged |
| googlemaps/react-native-navigation-sdk#644 | success |
| livekit/client-sdk-react-native#454 | success |
| livekit/client-sdk-react-native-expo-plugin#25 | success |
| BabylonJS/BabylonReactNative#745 | success, merged |
| klarna/react-native-klarna-inapp-sdk#388 | check no longer reported |
| rudderlabs/rudder-sdk-react-native#696 | check no longer reported |
| bitdriftlabs/capture-es#293 | all contributors signed |

## How each one was cleared

Signing is only half of it. Three different bots needed three different nudges,
and none of them re-evaluated on their own.

| Bot | What retriggers it |
|---|---|
| `cla-assistant` (Stripe, Klarna, LiveKit) | An empty commit. A `recheck` comment did **nothing** — the status sat unchanged for four days. |
| `adobe-cla-bot` | Close and reopen the pull request, which is what its own check summary instructs. |
| Expensify's GitHub Action | An empty commit. Close and reopen did not fire it. |
| `google-cla` | Re-ran on its own once the signature matched the commit author email. |

The general lesson: after signing, a `synchronize` event is the most reliable
retrigger. `git commit --allow-empty` and push.

Signing itself is a legal act and was always left to the account owner; only the
retriggers were automated here.
