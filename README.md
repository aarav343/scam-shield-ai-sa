# Scam Shield AI

**Student:** Aarav Motwani  
**Course:** Artificial Intelligence: Real-World Applications and Implications  
**Assessment:** Summative Assessment (Individual), IBCP Year 1  
**Platform:** Google Dialogflow ES

## Project overview

Scam Shield AI is a human-centered conversational fraud-awareness assistant for people who receive urgent payment requests, suspicious links, fake job offers, or impersonation calls. It offers clear warnings, safe next steps, and official reporting routes. It does not inspect URLs, verify identities, or certify a message as genuine. It never asks users to share a real OTP, UPI PIN, password, CVV, or full account details.

## User research and scope

Primary users are digital-payment users, students and job seekers, older adults, and people who may already have shared information or transferred money. Their pain points include urgency and pressure, confusing payment interfaces, fake authority cues, and uncertainty about what to save or report. The goal is to give a quick warning, a concise explanation, and a safe next action, then direct affected users to their bank and official reporting channels. The project does not move money, contact banks, or replace a professional investigation.

English is the working language in the recorded Dialogflow ES console tests. Hindi is available in the language selector. In the recorded Hindi console tests, scam requests reached the fallback or an unrelated intent; the separate Hindi package was not active during those tests. Results are in `HINDI_CONSOLE_TESTS.md`.

## Architecture

The import contains **21 intents** (including default welcome and fallback), **10 custom entities**, 12 example phrases per custom intent, a required follow-up slot for the requested action, short-lived contexts for scam details and the quiz, quick replies, and a reporting card. Responses are built into the agent; no webhook or external user data store is required. The `ScamCheckIntent` gives immediate precautionary advice before `ScamDetailsIntent` asks what action the sender requested.

## Intent catalogue

| Intent | Training phrases | Custom entity parameters |
| --- | ---: | --- |
| ScamCheckIntent | 12 | contact-channel, scam-type, urgency-cue |
| ScamDetailsIntent | 12 | requested-action |
| OTPIntent | 12 | credential-type, impersonated-identity, urgency-cue |
| UPICollectIntent | 12 | payment-method, credential-type |
| QRCodeIntent | 12 | payment-method, contact-channel |
| PhishingLinkIntent | 12 | link-feature, contact-channel, urgency-cue |
| FakeJobIntent | 12 | job-fee, contact-channel, urgency-cue |
| ImpersonationIntent | 12 | impersonated-identity, contact-channel, urgency-cue |
| InvestmentIntent | 12 | scam-type, contact-channel, urgency-cue |
| LoanAppIntent | 12 | scam-type, contact-channel, credential-type |
| RemoteAccessIntent | 12 | requested-action, impersonated-identity, loss-status |
| AccountCompromisedIntent | 12 | loss-status, credential-type, payment-method |
| ReportFraudIntent | 12 | scam-type, payment-method, loss-status |
| PreserveEvidenceIntent | 12 | contact-channel, link-feature |
| SafePaymentTipsIntent | 12 | payment-method, scam-type |
| QuizStartIntent | 12 | None |
| QuizSafeAnswerIntent | 12 | None |
| QuizUnsafeAnswerIntent | 12 | None |
| GoodbyeIntent | 12 | None |

## Entity catalogue

| Entity | Example canonical values |
| --- | --- |
| @scam-type | UPI fraud, phishing, job scam, investment scam, loan scam, impersonation |
| @contact-channel | WhatsApp, SMS, email, phone call, social media, website |
| @requested-action | share OTP, send money, open link, install app, scan QR, share PIN |
| @credential-type | OTP, UPI PIN, password, CVV, card number |
| @payment-method | UPI, QR code, bank transfer, card, wallet |
| @impersonated-identity | bank, government, employer, courier, support |
| @urgency-cue | immediately, today, within ten minutes, account will close |
| @link-feature | shortened link, misspelled domain, unknown website, unexpected attachment |
| @job-fee | registration fee, training fee, security deposit, equipment fee |
| @loss-status | money sent, credentials shared, app installed, no action taken |

## Dialogflow console results

The agent is `ScamShieldAI` (`scamshieldai-k9we`). Its English configuration contains 21 intents and 10 custom entities. The ten scenarios in `test_cases.csv` and three additional English inputs in `SECOND_PASS.md` passed in the Dialogflow ES console. The English greeting `hi` also matched Default Welcome Intent when `en` was selected. The Hindi results in `HINDI_CONSOLE_TESTS.md` describe the live agent before the separate Hindi package was imported.

The chatbot is demonstrated through the Dialogflow ES console. The former Web Demo URL returns 404 and is omitted from this repository's project links.

**GitHub repository:** https://github.com/aarav343/scam-shield-ai-sa (private).

## Privacy and safety

The agent is intentionally advisory. It does not accept real credentials and does not claim to detect fraud with certainty. A user who has lost money is directed to contact their bank immediately and use India's official financial cyber fraud helpline **1930** or [cybercrime.gov.in](https://cybercrime.gov.in/). These routes were checked against the official cybercrime, NPCI, and RBI sources on 22 October 2026.

## Sources

- [SA brief](https://docs.google.com/document/d/1S5Mo9vpwx0NfUdKMfST0aEMQzLXQEurs/edit)
- [Dialogflow ES agent settings and import](https://docs.cloud.google.com/dialogflow/es/docs/agents-settings)
- [Dialogflow ES actions and parameters](https://docs.cloud.google.com/dialogflow/es/docs/intents-actions-parameters)
- [Dialogflow Web Demo limitations](https://docs.cloud.google.com/dialogflow/es/docs/integrations/web-demo)
- [NPCI fraud awareness](https://www.npci.org.in/fraud-awareness)
- [RBI digital banking safeguards](https://rbikehtahai.rbi.org.in/safeguards-for-digital-banking.html)
- [National Cybercrime Reporting Portal](https://cybercrime.gov.in/)
