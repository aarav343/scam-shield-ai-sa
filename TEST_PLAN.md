# Dialogflow console test results

The live test pass was performed in the Dialogflow ES console for all cases in `test_cases.csv`: five required user scenarios, remote-access warning, slot/context follow-up, both quiz branches, and fallback. The actual matched intents and key extracted values are recorded there. All matched the intended intents and produced safety-aligned responses in this test pass.

A second English pass on 22 October 2026 tested a UPI refund PIN request, a misspelled suspicious SMS link, and an out-of-context quiz answer. All three matched safe responses; see `SECOND_PASS.md`.

## Hindi console observations

With Hindi selected, the greeting reached Welcome. The recorded scam requests reached fallback or the wrong intent; the observations are in `HINDI_CONSOLE_TESTS.md`. The separate Hindi package was not active during these checks.
