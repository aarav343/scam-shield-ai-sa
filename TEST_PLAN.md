# Test plan and optimization log

The live English test pass in Dialogflow ES covered all ten cases in `test_cases.csv`: the five required scenarios, remote access, slot/context follow-up, both quiz branches, and fallback. The CSV records actual matched intents and key extracted values. All ten produced safety-aligned responses in this pass.

## Second pass — 22 October 2026

| Input | Matched intent | Observed response | Result |
| --- | --- | --- | --- |
| A stranger says I must enter my UPI PIN to get a refund | UPICollectIntent | Warned that a PIN authorises payment and is not needed to receive money. | Pass |
| I recived a suspicous link by SMS | PhishingLinkIntent | Advised against opening the link and suggested typing the official address independently. | Pass |
| Yes (without starting the quiz) | Default Fallback Intent | Asked for a warning sign without secrets and offered safe options. | Pass |

## Hindi verification still required

The bilingual ZIP is prepared locally, but Hindi training phrases and responses have not been imported and verified in the live agent. After import, test a greeting, an OTP warning, a UPI collect request, scam-detail follow-up, quiz branches, and fallback in Hindi. Record matched intent, extracted parameters, response, and result. Do not describe the live agent as bilingual until these checks pass.

## Web Demo verification still required

Dialogflow returned a URL/body name-mismatch error when Web Demo was enabled on 22 October 2026; the setting reverted to ENABLE when reopened. The displayed demo URL produced a certificate-name error in Chrome. Resolve the integration error and verify the URL before presenting it as working.
