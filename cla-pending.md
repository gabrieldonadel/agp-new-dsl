# Pull requests waiting on a CLA

Found by scanning the CLA status checks, check runs and bot comments on every
open pull request in `upstream-prs.md`. Regenerate the scan with the same query
if more arrive; 13 PRs carry a CLA signal and 2 of those are already satisfied.

Each signature is one click and covers that organisation, not just the one PR,
so the Google and Stripe entries collapse into fewer actions than rows.

## Sign these (11)

Ordered by usage, highest first.

### cla-assistant.io — sign in with GitHub, one click each

| Package usage | PR | Sign |
|---|---|---|
| 0.053 | [stripe/stripe-react-native#2602](https://github.com/stripe/stripe-react-native/pull/2602) | https://cla-assistant.io/stripe/stripe-react-native?pullRequest=2602 |
| 0.015 | [livekit/client-sdk-react-native#454](https://github.com/livekit/client-sdk-react-native/pull/454) | https://cla-assistant.io/livekit/client-sdk-react-native?pullRequest=454 |
| 0.004 | [stripe/stripe-terminal-react-native#1134](https://github.com/stripe/stripe-terminal-react-native/pull/1134) | https://cla-assistant.io/stripe/stripe-terminal-react-native?pullRequest=1134 |
| 0.001 | [stripe/stripe-identity-react-native#276](https://github.com/stripe/stripe-identity-react-native/pull/276) | https://cla-assistant.io/stripe/stripe-identity-react-native?pullRequest=276 |
| 0.001 | [klarna/react-native-klarna-inapp-sdk#388](https://github.com/klarna/react-native-klarna-inapp-sdk/pull/388) | https://cla-assistant.io/klarna/react-native-klarna-inapp-sdk?pullRequest=388 |

The three Stripe repositories use separate cla-assistant records, so each needs
its own click.

### Google — one signature covers both

| Package usage | PR |
|---|---|
| 0.002 | [google-pay/react-native-make-payment#111](https://github.com/google-pay/react-native-make-payment/pull/111) |
| 0.001 | [googlemaps/react-native-navigation-sdk#644](https://github.com/googlemaps/react-native-navigation-sdk/pull/644) |

Sign once at https://cla.developers.google.com/about, then comment
`@googlebot I signed it!` on each PR to re-run the check.

### Adobe

| Package usage | PR | Sign |
|---|---|---|
| 0.003 | [adobe/aepsdk-react-native#591](https://github.com/adobe/aepsdk-react-native/pull/591) | https://opensource.adobe.com/cla.html |

### RudderStack — their own CLA service

| Package usage | PR | Sign |
|---|---|---|
| 0.013 | [rudderlabs/rudder-sdk-react-native#696](https://github.com/rudderlabs/rudder-sdk-react-native/pull/696) | https://contributor.rudderlabs.com/cla?org=rudderlabs&repo=rudder-sdk-react-native&prNumber=696&username=gabrieldonadel |

### Signed by posting a comment

| Package usage | PR | What to post |
|---|---|---|
| 0 | [bitdriftlabs/capture-es#293](https://github.com/bitdriftlabs/capture-es/pull/293) | The exact sentence their bot asks for, per [CLA.md](https://github.com/bitdriftlabs/capture-es/blob/main/CLA.md) |

## Needs a re-run, not a signature (1)

| PR | State |
|---|---|
| [Expensify/react-native-wallet#88](https://github.com/Expensify/react-native-wallet/pull/88) | The signing comment is already posted, but the `CLA / CLA` check still reports failure. Re-run the job or push an empty commit to retrigger it. |

## Already satisfied (2)

No action needed; listed so they are not rechecked.

- [livekit/client-sdk-react-native-expo-plugin#25](https://github.com/livekit/client-sdk-react-native-expo-plugin/pull/25) — `license/cla` success
- [BabylonJS/BabylonReactNative#745](https://github.com/BabylonJS/BabylonReactNative/pull/745) — all CLA requirements met

## Note

Signing a CLA is a legal act and is not something this harness does on anyone's
behalf, which is why every row above is a link for a person to click rather than
something already actioned.
