# Hindi console checks — 22 October 2026

These tests were run in the Dialogflow ES **Try it now** console for `ScamShieldAI` (`scamshieldai-k9we`) with Hindi selected. They describe the **current live agent before the prepared bilingual ZIP was imported**.

| Hindi input | Matched intent | Observed response | Assessment |
| --- | --- | --- | --- |
| नमस्ते | Default Welcome Intent | आपका दिन शुभ हो! | Greeting reached Welcome; generic reply |
| बैंक वाला मेरा ओटीपी मांग रहा है | Default Fallback Intent | माफ़ करें, क्या आप अपनी बात फिर से कह सकते हैं? | OTP warning failed |
| मुझे पैसे लेने के लिए यूपीआई पिन डालने को कह रहे हैं | Default Fallback Intent | माफ़ करें, मुझे समझ नहीं आया\| | UPI PIN warning failed |
| मुझे एसएमएस में संदिग्ध लिंक मिला है | Default Welcome Intent | नमस्कार! | Suspicious-link request misrouted |
| सुरक्षा क्विज़ शुरू करो | Default Fallback Intent | माफ़ करें, क्या कहा आपने? | Quiz start failed |
| मैंने ठग को पैसे भेज दिए | Default Fallback Intent | एक बार फिर से कह सकते हैं? | Money-loss guidance failed |

These results describe the live agent before the separate Hindi package was active.
