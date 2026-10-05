# Scam Shield AI

**Student:** Aarav Motwani  
**Course:** Artificial Intelligence: Real-World Applications and Implications  
**Assessment:** Summative Assessment (Individual), IBCP Year 1  
**Platform:** Google Dialogflow ES

## Project overview

Scam Shield AI is a human-centered conversational fraud-awareness assistant for people who receive urgent payment requests, suspicious links, fake job offers, or impersonation calls. It offers clear warnings, safe next steps, and official reporting routes. It does not inspect URLs, verify identities, or certify a message as genuine. It never asks users to share a real OTP, UPI PIN, password, CVV, or full account details.

## User research and scope

Primary users are digital-payment users, students and job seekers, older adults, and people who may already have shared information or transferred money. Their pain points include urgency and pressure, confusing payment interfaces, fake authority cues, and uncertainty about what to save or report. The goal is to give a quick warning, a concise explanation, and a safe next action, then direct affected users to their bank and official reporting channels. The project does not move money, contact banks, or replace a professional investigation.

The assessment brief describes the intended assistant as bilingual. The current Dialogflow ES agent is configured in English; a second language, translated responses, and bilingual test evidence are not yet implemented. Do not describe the live prototype as bilingual until that work is completed and tested.

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

## Import and deployment

The agent exists in the user's Dialogflow ES account as `ScamShieldAI` (agent ID `scamshieldai-k9we`). The import ZIP was loaded and the console showed 21 intents and 10 custom entities. Do not import it again into the active agent unless a future change requires a restore.

The live console checks recorded in `test_cases.csv` passed for all ten scenarios, including remote-access, both quiz branches, slot/context follow-up, and fallback. The Integrations page displayed an IAM permission warning during this continuation, so Web Demo could not yet be enabled or verified.

**Live chatbot URL:** Not yet enabled (Dialogflow Web Demo requires permission).  
**GitHub URL:** https://github.com/aarav343/scam-shield-ai-sa (private; currently visible only to the account owner and invited collaborators).  
**Candidate registration number:** Not provided; add it if required by the brief.

## Review checklist

- Enable and verify the Web Demo after resolving Dialogflow permission; then record its actual URL here.
- Optionally run a second round with paraphrases and misspellings to evaluate robustness.
- Complete and test the second language described in the brief.
- If the teacher must review the repository, confirm whether public visibility is required or add the teacher as a collaborator after getting their GitHub username. Do not make it public without checking first.
- Add the candidate registration number only if required; it has not been provided.
- Review all advice and sources, then perform the final school upload yourself.

## Privacy and safety

The agent is intentionally advisory. It does not accept real credentials and does not claim to detect fraud with certainty. A user who has lost money is directed to contact their bank immediately and use India's official financial cyber fraud helpline **1930** or [cybercrime.gov.in](https://cybercrime.gov.in/). These routes should be rechecked before final submission.

## Sources

- [SA brief](https://docs.google.com/document/d/1S5Mo9vpwx0NfUdKMfST0aEMQzLXQEurs/edit)
- [Dialogflow ES agent settings and import](https://docs.cloud.google.com/dialogflow/es/docs/agents-settings)
- [Dialogflow ES actions and parameters](https://docs.cloud.google.com/dialogflow/es/docs/intents-actions-parameters)
- [NPCI fraud awareness](https://www.npci.org.in/fraud-awareness)
- [RBI digital banking safeguards](https://rbikehtahai.rbi.org.in/safeguards-for-digital-banking.html)
- [National Cybercrime Reporting Portal](https://cybercrime.gov.in/)
