# Live English second pass — 22 October 2026

| Input | Matched intent | Observed response | Result |
| --- | --- | --- | --- |
| A stranger says I must enter my UPI PIN to get a refund | UPICollectIntent | Warned that PIN authorises payment and is not needed to receive money. | Pass |
| I recived a suspicous link by SMS | PhishingLinkIntent | Advised not to open the link and to type the official address independently. | Pass |
| Yes (without starting the quiz) | Default Fallback Intent | Asked for a warning sign without secrets and offered safe options. | Pass |

These tests were run in the Dialogflow ES console for agent `scamshieldai-k9we` with English selected.
