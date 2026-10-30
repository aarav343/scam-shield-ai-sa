# Scam Shield AI

**Student:** Aarav Motwani  
**Course:** Artificial Intelligence: Real-World Applications and Implications  
**Assessment:** Summative Assessment (Individual), IBCP Year 1  
**Platform:** Google Dialogflow ES

## Project overview

Scam Shield AI is a conversational fraud-awareness assistant. I built it to help people respond more safely to suspicious payment requests, unknown links, fake job offers, impersonation calls, and similar scams.

The chatbot explains common warning signs and suggests practical next steps. It is **an awareness and guidance tool, not a fraud-verification service**. It cannot inspect URLs, confirm identities, determine for certain whether a message is genuine, contact a bank, or recover money. Users should never enter real OTPs, UPI PINs, passwords, CVVs, or full account details into the chatbot.

## Agent package

`ScamShieldAI_Agent.zip` is the Dialogflow ES agent import package.

## Problem and intended users

Fraud messages often create pressure to act quickly. A message may pretend to be from a bank, employer, courier, or support team, and ask someone to share a code, pay a fee, scan a QR code, or install an application.

The prototype is designed with these groups in mind:

- People using digital payments and UPI
- Students and job seekers
- Older adults and people who may be less familiar with digital fraud
- People who have already shared information or transferred money

These are intended user groups, not a claim that formal interviews or usability studies were carried out.

## How it works

Scam Shield AI uses Dialogflow ES intent matching, custom entities, and short-lived conversation contexts. It recognises common scam-related questions and replies with prepared safety advice. It does **not** use a generative large language model or perform live fraud detection.

The English agent contains:

- **21 intents:** 19 custom intents plus Default Welcome and Default Fallback
- **10 custom entities** for scam types, contact channels, requested actions, and related details
- **12 training phrases per custom intent** in the prepared import package
- A required follow-up parameter for the action requested by a suspicious sender
- Short-lived contexts for scam details and the safety quiz
- Quick replies and a reporting information card

The agent uses built-in responses and does not require a webhook or separate application database. This does not mean that the Dialogflow platform has no data-processing or logging behaviour.

The `ScamCheckIntent` first gives immediate precautionary advice. `ScamDetailsIntent` then asks what action the sender requested, without asking the user to paste sensitive information.

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

The two additional intents are **Default Welcome Intent** and **Default Fallback Intent**.

## Custom entities

| Entity | Example values |
| --- | --- |
| `@scam-type` | UPI fraud, phishing, job scam, investment scam, loan scam, impersonation |
| `@contact-channel` | WhatsApp, SMS, email, phone call, social media, website |
| `@requested-action` | share OTP, send money, open link, install app, scan QR, share PIN |
| `@credential-type` | OTP, UPI PIN, password, CVV, card number |
| `@payment-method` | UPI, QR code, bank transfer, card, wallet |
| `@impersonated-identity` | bank, employer, courier, support |
| `@urgency-cue` | immediately, today, within ten minutes, account will close |
| `@link-feature` | shortened link, misspelled domain, unknown website, unexpected attachment |
| `@job-fee` | registration fee, training fee, security deposit, equipment fee |
| `@loss-status` | money sent, credentials shared, app installed, no action taken |

These are representative examples. The imported entity definitions are the source for their complete entries and synonyms.

## Testing and results

I tested the agent in the **Dialogflow ES “Try it now” console**. I recorded **13 English scenario checks** that matched their intended intents and gave appropriate precautionary advice. A separate English greeting test matched Default Welcome Intent when English (`en`) was selected.

The scenarios included OTP requests, UPI collect requests, phishing links, fake job fees, remote-access requests, money already lost, scam-detail follow-up, quiz responses, and fallback behaviour.

A pass in these recorded tests means the expected intent matched and the response was appropriate **for that particular input**. It does not guarantee that the agent will understand every possible wording.

### Language limitation

**English is the tested working language of this prototype.** Hindi was selectable in the console, but most recorded Hindi scam requests did not match the intended intents: they reached fallback or an unrelated intent. I have therefore not presented the prototype as a working bilingual chatbot. Expanding Hindi training phrases, entities, and responses, then retesting them, would be a future improvement.

## Safety and privacy boundaries

- Never ask users to enter real OTPs, UPI PINs, passwords, CVVs, or complete account details.
- Do not claim that a link, caller, or payment request has been verified as genuine.
- Encourage users to contact organisations using independently found official contact details.
- If a user has already lost money or shared sensitive credentials, advise immediate contact with their bank or payment provider.
- For financial cyber fraud in India, direct users to the **1930** helpline and the [National Cybercrime Reporting Portal](https://cybercrime.gov.in/).
- Encourage users to preserve relevant evidence without sharing sensitive credentials in the chatbot.

Scam Shield AI does not transfer money, contact authorities, investigate complaints, or promise recovery of funds.

## Open and import the agent

1. Sign in to [Dialogflow ES](https://dialogflow.cloud.google.com/) with an account that has access to the relevant Google Cloud project.
2. To view the existing agent, open [ScamShieldAI](https://dialogflow.cloud.google.com/#/editAgent/scamshieldai-k9we/).
3. To inspect a separate copy, create or select a suitable Dialogflow ES agent and use its **Export and Import** settings to import `ScamShieldAI_Agent.zip`.
4. Choose English (`en`) and test the example scenarios in **Try it now**.

**Note:** Importing an agent may replace agent configuration in the chosen destination. Use a separate test agent if you do not want to overwrite existing work. The exported ZIP does not itself include console test history or all integration settings.

## Limitations and possible improvements

This is a course prototype rather than a production fraud-detection product. Its main limitations are predefined responses, incomplete Hindi intent matching, and a limited set of observed test scenarios. Future work could include broader testing with unfamiliar phrasing, improved multilingual support, clearer accessibility checks, and more scam scenarios. These improvements should be tested before making stronger reliability claims.

## References

- [Dialogflow ES: Agent settings](https://docs.cloud.google.com/dialogflow/es/docs/agents-settings)
- [Dialogflow ES: Actions and parameters](https://docs.cloud.google.com/dialogflow/es/docs/intents-actions-parameters)
- [Dialogflow ES: Web demo integration](https://docs.cloud.google.com/dialogflow/es/docs/integrations/web-demo)
- [NPCI: Fraud awareness](https://www.npci.org.in/fraud-awareness)
- [RBI: Safeguards for digital banking](https://rbikehtahai.rbi.org.in/safeguards-for-digital-banking.html)
- [National Cybercrime Reporting Portal](https://cybercrime.gov.in/)

**Project repository:** [aarav343/scam-shield-ai-sa](https://github.com/aarav343/scam-shield-ai-sa).
