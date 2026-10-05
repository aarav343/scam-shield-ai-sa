# Test plan and optimization log

The live test pass was performed in the Dialogflow ES console for all cases in `test_cases.csv`: five required user scenarios, remote-access warning, slot/context follow-up, both quiz branches, and fallback. The actual matched intents and key extracted values are recorded there. All matched the intended intents and produced safety-aligned responses in this test pass.

For a second pass, try natural paraphrases, misspellings, and unexpected input. Confirm that the agent never asks for a real OTP or PIN, that reports direct users to official channels, and that quiz answers are interpreted only while quiz context is active.
