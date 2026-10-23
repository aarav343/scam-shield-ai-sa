"""Build the Scam Shield AI Dialogflow ES agent import."""

from __future__ import annotations

import io
import json
import re
import uuid
import zipfile
from pathlib import Path


ROOT = Path(__file__).parent


def lines(value: str) -> list[str]:
    return [line.strip() for line in value.strip().splitlines() if line.strip()]


ENTITIES = {
    "scam-type": {
        "UPI fraud": ["UPI scam", "UPI fraud", "payment scam"],
        "phishing": ["phishing", "fake login", "phishing email"],
        "job scam": ["job scam", "fake job", "fake offer"],
        "investment scam": ["investment scam", "trading scam", "investment fraud"],
        "loan scam": ["loan scam", "fake loan", "loan app scam"],
        "impersonation": ["impersonation", "someone pretending", "fake support"],
    },
    "contact-channel": {
        "WhatsApp": ["WhatsApp", "WhatsApp chat"],
        "SMS": ["SMS", "text message"],
        "email": ["email", "mail"],
        "phone call": ["phone call", "call", "telephone call"],
        "social media": ["social media", "Instagram", "Facebook"],
        "website": ["website", "web page"],
    },
    "requested-action": {
        "share OTP": ["share my OTP", "share an OTP", "send an OTP", "give the OTP"],
        "send money": ["send money", "transfer money", "pay money"],
        "open link": ["open a link", "click a link", "open the link"],
        "install app": ["install an app", "download an app", "install a remote app"],
        "scan QR": ["scan a QR code", "scan QR", "scan their QR code"],
        "share PIN": ["share my PIN", "tell them my PIN", "give my UPI PIN"],
    },
    "credential-type": {
        "OTP": ["OTP", "one-time password", "one time code"],
        "UPI PIN": ["UPI PIN", "UPI-PIN"],
        "password": ["password", "login password"],
        "CVV": ["CVV", "card security code"],
        "card number": ["card number", "debit card number"],
    },
    "payment-method": {
        "UPI": ["UPI", "UPI collect request"],
        "QR code": ["QR code", "payment QR"],
        "bank transfer": ["bank transfer", "NEFT", "IMPS"],
        "card": ["card", "credit card", "debit card"],
        "wallet": ["wallet", "digital wallet"],
    },
    "impersonated-identity": {
        "bank": ["bank", "bank employee", "bank officer"],
        "government": ["government", "police", "tax department"],
        "employer": ["employer", "recruiter", "HR manager"],
        "courier": ["courier", "delivery company"],
        "support": ["support", "customer care", "technical support"],
    },
    "urgency-cue": {
        "immediately": ["immediately", "right now", "urgent"],
        "today": ["today", "before tonight"],
        "within ten minutes": ["within ten minutes", "in ten minutes", "within 10 minutes"],
        "account will close": ["account will close", "account will be blocked"],
    },
    "link-feature": {
        "shortened link": ["shortened link", "tiny URL", "bit.ly link"],
        "misspelled domain": ["misspelled domain", "wrong spelling in the URL"],
        "unknown website": ["unknown website", "unfamiliar website"],
        "unexpected attachment": ["unexpected attachment", "strange attachment"],
    },
    "job-fee": {
        "registration fee": ["registration fee", "application fee"],
        "training fee": ["training fee", "course fee"],
        "security deposit": ["security deposit", "refundable deposit"],
        "equipment fee": ["equipment fee", "laptop fee"],
    },
    "loss-status": {
        "money sent": ["money sent", "sent money", "paid them"],
        "credentials shared": ["credentials shared", "shared my OTP", "gave them my PIN"],
        "app installed": ["app installed", "installed the app", "gave remote access"],
        "no action taken": ["no action taken", "did not pay", "have not clicked"],
    },
}


INTENTS = [
    {
        "name": "ScamCheckIntent",
        "action": "scam.check",
        "response": "I cannot verify a message as safe from a description alone. Do not click links, pay, or share codes. Tell me what the sender asked you to do, without pasting any OTP, PIN, password, or full account details.",
        "phrases": lines("""
            Can you check if this message is a scam?
            I received a suspicious message
            Is this offer genuine or fraud?
            I think someone is trying to trick me
            Can you help me identify a scam?
            A WhatsApp message looks suspicious
            I got an SMS that may be fake
            How do I check whether a message is safe?
            I received a suspicious email today
            This phone call felt like a scam
            Can you review a possible phishing message?
            I am unsure if an online request is legitimate
        """),
        "params": ["contact-channel", "scam-type", "urgency-cue"],
        "output_context": "scam-details-followup",
        "quick": ["Asked for an OTP", "They asked for money", "How do I report it?"],
    },
    {
        "name": "ScamDetailsIntent",
        "action": "scam.details",
        "response": "That request is a warning sign. Pause contact and independently check the organisation through its official app or website. Do not share a PIN, OTP, password, or CVV. If you already lost money, contact your bank and report financial cyber fraud immediately.",
        "phrases": lines("""
            They asked me to share my OTP
            They want me to send money
            I was told to open a link
            They asked me to install an app
            The person wants me to scan a QR code
            They asked me to share my PIN
            The message says to transfer money
            They want me to click a link
            They told me to download an app
            They asked for an OTP
            They want me to give my UPI PIN
            They are asking me to pay money
        """),
        "params": ["requested-action"],
        "required": ["requested-action"],
        "input_context": "scam-details-followup",
        "quick": ["I already paid", "How do I report it?"],
    },
    {
        "name": "OTPIntent",
        "action": "scam.otp",
        "response": "Never share an OTP, UPI PIN, password, or CVV with another person, even if they claim to be from your bank. Stop the conversation and contact your bank using a number from its official app or card.",
        "phrases": lines("""
            Should I share my OTP with someone?
            A caller asked for my one-time password
            My bank says it needs my OTP
            They want my UPI PIN to fix the issue
            Is it safe to send a password in chat?
            Someone asked for my CVV
            A support agent requested my one time code
            Can I tell a recruiter my OTP?
            A message asks for my card number
            Do banks ever ask for a PIN on calls?
            I was told to give the OTP immediately
            They need my login password to verify me
        """),
        "params": ["credential-type", "impersonated-identity", "urgency-cue"],
        "quick": ["I shared it already", "How do I report it?"],
    },
    {
        "name": "UPICollectIntent",
        "action": "scam.upi_collect",
        "response": "Be careful with unexpected UPI collect requests. Entering your UPI PIN authorises a payment; it is not needed to receive money. Decline the request and verify the sender through an official channel.",
        "phrases": lines("""
            They sent me a UPI collect request
            Do I need a UPI PIN to receive a refund?
            A stranger says approve a payment request to get money
            Can I receive money by entering my UPI PIN?
            Someone sent a collect request on my payment app
            They say the UPI request is for verification
            Is an unexpected request for money safe?
            My refund requires accepting a UPI collect request
            A caller wants me to authorise a UPI request
            A payment app asks me to approve a stranger's request
            I was told to enter a PIN for cashback
            Is this UPI collect message a scam?
        """),
        "params": ["payment-method", "credential-type"],
        "quick": ["I approved it", "Report fraud"],
    },
    {
        "name": "QRCodeIntent",
        "action": "scam.qr",
        "response": "Do not scan an unknown QR code or enter your UPI PIN to receive a refund or prize. Scanning and approving with a PIN can make a payment. Verify through the official app instead.",
        "phrases": lines("""
            They sent a QR code for my refund
            Should I scan this QR to receive money?
            A stranger says scan a QR code for cashback
            I got a payment QR from an unknown person
            The seller asked me to scan their QR code
            Can a QR code help me get a prize?
            Someone wants me to scan QR for verification
            Is it safe to pay using an unfamiliar QR code?
            I was told to enter UPI PIN after scanning
            I received a QR code in WhatsApp
            How can I check a payment QR?
            They say I must scan QR to get my deposit back
        """),
        "params": ["payment-method", "contact-channel"],
        "quick": ["I scanned it", "More safety tips"],
    },
    {
        "name": "PhishingLinkIntent",
        "action": "scam.phishing",
        "response": "Do not open an unexpected link or attachment. A shortened URL, misspelled domain, or urgent login demand is a warning sign. Visit the organisation's official website by typing the address yourself.",
        "phrases": lines("""
            I received a shortened link in SMS
            Is a bit.ly link from my bank safe?
            This email has an unexpected attachment
            A message asks me to open a link
            The website has a misspelled domain
            I got a login link from an unknown website
            They say click a link to avoid account closure
            Can a phishing email steal my password?
            Should I download a file from this message?
            The URL spelling looks wrong
            A courier SMS links to a payment page
            A stranger sent me a link to verify my identity
        """),
        "params": ["link-feature", "contact-channel", "urgency-cue"],
        "quick": ["I clicked it", "Report fraud"],
    },
    {
        "name": "FakeJobIntent",
        "action": "scam.job",
        "response": "A job offer asking for an upfront registration, training, or equipment fee is a warning sign. Do not pay or share sensitive documents. Verify the employer on its official website and contact the published HR number independently.",
        "phrases": lines("""
            A job offer asks for a registration fee
            The recruiter wants a training fee
            I must pay a security deposit for an interview
            A company asks for an equipment fee first
            Is this work from home offer genuine?
            I got a job on WhatsApp but need to pay
            A recruiter asks for money before hiring me
            They promised a high salary without an interview
            Is a paid application for a job a scam?
            The employer says pay today to keep the role
            A fake job offer asks for my bank details
            Should I transfer money for a new job?
        """),
        "params": ["job-fee", "contact-channel", "urgency-cue"],
        "quick": ["I paid already", "How to verify them?"],
    },
    {
        "name": "ImpersonationIntent",
        "action": "scam.impersonation",
        "response": "A name, logo, or caller ID does not prove identity. End the conversation and contact the bank, government office, employer, courier, or support team through an independently found official channel. Do not share credentials or pay a 'verification' fee.",
        "phrases": lines("""
            Someone claiming to be my bank called me
            A government officer asked me to pay
            The police called and demanded money
            A courier says my package is held
            Technical support wants remote access
            The caller claims to be customer care
            Is this bank employee real?
            A recruiter says they are from a famous company
            This account uses a government logo
            Someone says they represent the tax department
            The delivery company wants my OTP
            A support person told me to act immediately
        """),
        "params": ["impersonated-identity", "contact-channel", "urgency-cue"],
        "quick": ["Asked for an OTP", "I already paid"],
    },
    {
        "name": "InvestmentIntent",
        "action": "scam.investment",
        "response": "Guaranteed high returns and pressure to invest quickly are warning signs. Do not send money based on a chat group or influencer claim. Independently verify the provider and its regulator details before any decision.",
        "phrases": lines("""
            This investment promises guaranteed returns
            A trading group says I can double my money
            Someone offered a risk-free crypto investment
            I was invited to a stock tip WhatsApp group
            An influencer says this scheme cannot lose
            They want me to invest immediately
            Is this online investment offer trustworthy?
            A stranger showed me fake profit screenshots
            They promised fixed daily returns
            A trading app asks for a deposit today
            I got an investment scam message
            Should I join this secret profit group?
        """),
        "params": ["scam-type", "contact-channel", "urgency-cue"],
        "quick": ["I invested already", "Report fraud"],
    },
    {
        "name": "LoanAppIntent",
        "action": "scam.loan",
        "response": "Be cautious with loan apps that demand an advance fee, unnecessary phone permissions, or payment outside the official app. Verify the lender independently and do not share an OTP or install unknown software.",
        "phrases": lines("""
            A loan app wants an advance fee
            Is this instant loan offer safe?
            The lender wants access to my contacts
            A fake loan app says pay first
            I was offered a loan on WhatsApp
            The loan company asks for my OTP
            The app wants full phone permissions
            They say I must transfer money to unlock a loan
            Is a no-document loan genuine?
            The lender is threatening me by phone
            This loan offer looks like a scam
            How do I check a digital lender?
        """),
        "params": ["scam-type", "contact-channel", "credential-type"],
        "quick": ["I shared details", "Report fraud"],
    },
    {
        "name": "RemoteAccessIntent",
        "action": "scam.remote_access",
        "response": "Do not install a remote-control app for an unsolicited caller. It may let them view your screen or operate your device. If you already installed one, disconnect the device, remove the app, contact your bank through official channels, and change passwords from a trusted device.",
        "phrases": lines("""
            Support asked me to install an app
            They want to control my phone remotely
            Is it safe to share my screen with a caller?
            Someone asked me to download AnyDesk
            A bank agent wants remote access
            I installed a remote app for a refund
            They asked me to turn on screen sharing
            A stranger wants to help by controlling my laptop
            The caller told me to download an app
            I gave technical support access to my device
            Should I allow a remote connection?
            An unknown person can see my screen
        """),
        "params": ["requested-action", "impersonated-identity", "loss-status"],
        "quick": ["I installed it", "Report fraud"],
    },
    {
        "name": "AccountCompromisedIntent",
        "action": "scam.compromised",
        "response": "Act quickly: contact your bank or payment provider using its official app, website, or card number. Block affected access, change passwords from a trusted device, and review transactions. For financial cyber fraud in India, call 1930 or use cybercrime.gov.in.",
        "phrases": lines("""
            I shared my OTP already
            I gave them my UPI PIN
            I clicked the link and entered my password
            I sent money to a scammer
            My bank account may be compromised
            I installed the app they suggested
            There is an unauthorised transaction
            I paid them and now they disappeared
            Someone has access to my wallet
            My card details were stolen
            I may have given remote access
            I think my account was hacked
        """),
        "params": ["loss-status", "credential-type", "payment-method"],
        "quick": ["Report fraud", "Preserve evidence"],
    },
    {
        "name": "ReportFraudIntent",
        "action": "scam.report",
        "response": "If money was lost in India, contact your bank immediately and call the national financial cyber fraud helpline 1930. You can also report at https://cybercrime.gov.in/. Use official sites only. Keep transaction IDs and screenshots, but do not share an OTP, PIN, or password here.",
        "phrases": lines("""
            How do I report online fraud?
            I need to report a scam
            Where can I complain about a phishing attempt?
            I paid a scammer; who should I call?
            What is the cyber fraud helpline?
            How do I report a fake job offer?
            Can I file a complaint about UPI fraud?
            I lost money; what should I do first?
            Where is the official cybercrime portal?
            Help me report an unauthorised payment
            How do I inform my bank about fraud?
            I want to make a cybercrime complaint
        """),
        "params": ["scam-type", "payment-method", "loss-status"],
        "quick": ["Preserve evidence", "Secure my account"],
        "card": True,
    },
    {
        "name": "PreserveEvidenceIntent",
        "action": "scam.evidence",
        "response": "Save screenshots of the message, sender details, links, transaction IDs, dates, and times. Do not delete the chat before reporting. Do not paste private credentials into this chatbot. Share evidence only through your bank's or the cybercrime portal's official reporting route.",
        "phrases": lines("""
            What evidence should I save?
            Should I delete the scam message?
            How can I document a suspicious call?
            Do I need screenshots of the WhatsApp chat?
            Which transaction details matter for a report?
            Should I keep the SMS from the scammer?
            What information does a fraud complaint need?
            Can I save the email headers?
            How do I keep proof of a fake website?
            I have a payment reference number
            Should I forward the scam message to others?
            What should I do with the phishing link?
        """),
        "params": ["contact-channel", "link-feature"],
        "quick": ["Report fraud", "Secure my account"],
    },
    {
        "name": "SafePaymentTipsIntent",
        "action": "scam.tips",
        "response": "Before paying, verify the recipient independently, check the amount in your payment app, and avoid links from strangers. Never enter a UPI PIN to receive money and never share OTPs, PINs, passwords, or CVV. If pressured, stop and contact your bank through its official channel.",
        "phrases": lines("""
            Give me safe payment tips
            How can I avoid UPI scams?
            What should I check before a bank transfer?
            How can I protect my digital wallet?
            Give me advice for paying online
            How do I check a QR payment?
            What are warning signs of payment fraud?
            How do I stay safe with a credit card?
            Tell me how to avoid phishing
            What should I never share with callers?
            Can you give me a digital safety checklist?
            How do I make safer online payments?
        """),
        "params": ["payment-method", "scam-type"],
        "quick": ["Take a safety quiz", "Report fraud"],
    },
    {
        "name": "QuizStartIntent",
        "action": "quiz.start",
        "response": "Quick quiz: a caller claims to be your bank and asks for your OTP to stop fraud. Should you share it? Reply yes or no.",
        "phrases": lines("""
            Start a safety quiz
            Quiz me about scams
            I want a fraud awareness question
            Test my knowledge about OTPs
            Can we do a quick safety quiz?
            Give me a practice question
            I want to learn through a quiz
            Ask me a scam prevention question
            Let's play a fraud safety quiz
            How well do I know scam warning signs?
            Start the awareness quiz
            Give me a digital safety challenge
        """),
        "output_context": "quiz-otp-answer",
        "quick": ["Yes", "No"],
    },
    {
        "name": "QuizSafeAnswerIntent",
        "action": "quiz.correct",
        "response": "Correct. Never share an OTP with a caller, even if they claim to be from your bank. For help, end the call and use the bank's official contact details.",
        "phrases": lines("""
            No
            Never
            I should not share it
            Do not give them the OTP
            No, that is unsafe
            I would hang up
            No way
            I must keep it private
            I would contact my bank instead
            No, the bank does not need my OTP
            That sounds suspicious so no
            I will not tell the caller
        """),
        "input_context": "quiz-otp-answer",
        "quick": ["Another tip", "Report fraud"],
    },
    {
        "name": "QuizUnsafeAnswerIntent",
        "action": "quiz.incorrect",
        "response": "The safe answer is no. A caller asking for your OTP is a warning sign. Never share it; end the call and contact your bank through an official number.",
        "phrases": lines("""
            Yes
            Sure
            I would share it
            I can give the code
            Yes, if they sound official
            Maybe I should tell the bank
            I would send the OTP
            Yes, to stop the fraud
            I think it is okay
            I would read the code aloud
            Yes, if the caller knows my name
            I can tell them the PIN too
        """),
        "input_context": "quiz-otp-answer",
        "quick": ["Another tip", "Report fraud"],
    },
    {
        "name": "GoodbyeIntent",
        "action": "input.goodbye",
        "response": "Stay safe. If you have lost money or shared credentials, contact your bank promptly and report financial cyber fraud through official channels.",
        "phrases": lines("""
            Goodbye
            Bye
            Thanks, bye
            I am done for now
            End chat
            See you later
            That is all, thanks
            I have no more questions
            Thank you for the help
            I need to go
            Talk later
            Stop the conversation
        """),
    },
]


WELCOME = {
    "name": "Default Welcome Intent",
    "action": "input.welcome",
    "response": "Welcome to ScamShield AI. I can help you spot warning signs, learn safer actions, and find official reporting options. Please do not share OTPs, PINs, passwords, CVV, or full account details here. What happened?",
    "phrases": lines("""
        Hi
        Hello
        Hey ScamShield
        Good morning
        Good evening
        I need help with a scam
        Can you help me stay safe online?
        Start
        Help me check a message
        I need fraud safety advice
        What can you do?
        I need digital safety support
    """),
    "quick": ["Check a message", "Safe payment tips", "Report fraud"],
    "event": "WELCOME",
}


FALLBACK = {
    "name": "Default Fallback Intent",
    "action": "input.unknown",
    "response": "I may have misunderstood. Please describe the warning sign without sharing sensitive details, or choose: check a message, payment safety tips, or report fraud. If money was lost, contact your bank and call 1930 promptly.",
    "phrases": [],
    "fallback": True,
    "quick": ["Check a message", "Safe payment tips", "Report fraud"],
}


def annotate(text: str, parameter_types: list[str]) -> list[dict]:
    matches = []
    for entity in parameter_types:
        for canonical, synonyms in ENTITIES[entity].items():
            for synonym in synonyms:
                for match in re.finditer(r"(?<!\w)" + re.escape(synonym) + r"(?!\w)", text, re.I):
                    matches.append((match.start(), match.end(), entity, canonical))
    matches.sort(key=lambda item: (item[0], -(item[1] - item[0])))
    chosen = []
    for match in matches:
        if not any(match[0] < old[1] and old[0] < match[1] for old in chosen):
            chosen.append(match)
    chosen.sort()
    parts = []
    cursor = 0
    for start, end, entity, _ in chosen:
        if start > cursor:
            parts.append({"text": text[cursor:start], "userDefined": False})
        parts.append({"text": text[start:end], "alias": entity.replace("-", "_"), "meta": "@" + entity, "userDefined": False})
        cursor = end
    if cursor < len(text):
        parts.append({"text": text[cursor:], "userDefined": False})
    return parts or [{"text": text, "userDefined": False}]


def make_intent(spec: dict) -> tuple[dict, list[dict]]:
    name = spec["name"]
    messages = [{"type": 0, "lang": "en", "condition": "", "speech": [spec["response"]]}]
    if spec.get("quick"):
        messages.append({"type": 2, "lang": "en", "title": "Quick actions", "replies": spec["quick"]})
    if spec.get("card"):
        messages.append({"type": 1, "lang": "en", "title": "Official cybercrime reporting", "subtitle": "Report financial cyber fraud through India's official portal.", "buttons": [{"text": "Open cybercrime.gov.in", "postback": "https://cybercrime.gov.in/"}]})
    parameters = []
    for index, entity in enumerate(spec.get("params", [])):
        required = entity in spec.get("required", [])
        parameters.append({
            "id": str(uuid.uuid5(uuid.NAMESPACE_DNS, f"scamshield-{name}-{entity}")),
            "required": required,
            "dataType": "@" + entity,
            "name": entity.replace("-", "_"),
            "value": "$" + entity.replace("-", "_"),
            "promptMessages": ([{"lang": "en", "value": "What did they ask you to do? For example, send money, share an OTP, open a link, or install an app. Do not enter any actual code or PIN."}] if required else []),
            "noMatchPromptMessages": [],
            "noInputPromptMessages": [],
            "outputDialogContexts": [],
            "isList": False,
        })
    data = {
        "id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "scamshield-intent-" + name)),
        "name": name,
        "auto": True,
        "contexts": ([spec["input_context"]] if spec.get("input_context") else []),
        "responses": [{
            "resetContexts": False,
            "action": spec["action"],
            "affectedContexts": ([{"name": spec["output_context"], "parameters": {}, "lifespan": 3}] if spec.get("output_context") else []),
            "parameters": parameters,
            "messages": messages,
            "defaultResponsePlatforms": {},
            "speech": [],
        }],
        "priority": 500000,
        "webhookUsed": False,
        "webhookForSlotFilling": False,
        "fallbackIntent": bool(spec.get("fallback")),
        "events": ([{"name": spec["event"]}] if spec.get("event") else []),
        "conditionalResponses": [],
        "condition": "",
        "conditionalFollowupEvents": [],
    }
    examples = [
        {"id": str(uuid.uuid5(uuid.NAMESPACE_DNS, f"scamshield-{name}-phrase-{index}")),
         "data": annotate(phrase, spec.get("params", [])),
         "isTemplate": False, "count": 0, "updated": 0}
        for index, phrase in enumerate(spec["phrases"])
    ]
    return data, examples


def validate() -> None:
    names = [item["name"] for item in INTENTS]
    assert len(names) >= 15 and len(names) == len(set(names))
    assert len(ENTITIES) >= 10
    assert all(len(item["phrases"]) >= 12 for item in INTENTS)
    assert all(len(set(item["phrases"])) == len(item["phrases"]) for item in INTENTS)
    used = {param for item in INTENTS for param in item.get("params", [])}
    assert set(ENTITIES) <= used, set(ENTITIES) - used
    assert any(item.get("required") for item in INTENTS)


def build_zip() -> None:
    agent = {
        "description": "ScamShield AI: cautious fraud awareness and reporting guidance for India.",
        "language": "en",
        "shortDescription": "Fraud safety assistant for UPI, phishing, job scams and reporting",
        "defaultTimezone": "Asia/Kolkata",
        "isPrivate": True,
        "customClassifierMode": "use.after",
        "mlMinConfidence": 0.3,
        "supportedLanguages": [],
        "onePlatformApiVersion": "v2",
        "webhook": {"url": "", "username": "", "headers": {}, "available": False, "useForDomains": False},
    }
    archive = ROOT / "ScamShieldAI_Agent.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as package:
        package.writestr("agent.json", json.dumps(agent, indent=2))
        package.writestr("package.json", json.dumps({"version": "1.0.0"}, indent=2))
        for entity, values in ENTITIES.items():
            entity_data = {"id": str(uuid.uuid5(uuid.NAMESPACE_DNS, "scamshield-entity-" + entity)),
                           "name": entity, "isOverridable": True, "isEnum": False,
                           "isRegexp": False, "automatedExpansion": False,
                           "allowFuzzyExtraction": False}
            entries = [{"value": canonical, "synonyms": list(dict.fromkeys([canonical, *synonyms]))}
                       for canonical, synonyms in values.items()]
            package.writestr(f"entities/{entity}.json", json.dumps(entity_data, indent=2))
            package.writestr(f"entities/{entity}_entries_en.json", json.dumps(entries, indent=2))
        for spec in [WELCOME, *INTENTS, FALLBACK]:
            intent, examples = make_intent(spec)
            name = spec["name"]
            package.writestr(f"intents/{name}.json", json.dumps(intent, indent=2))
            if examples:
                package.writestr(f"intents/{name}_usersays_en.json", json.dumps(examples, indent=2))



def main() -> None:
    validate()
    build_zip()
    print(f"Built {len(INTENTS) + 2} intents, {len(ENTITIES)} entities, and {sum(len(item['phrases']) for item in INTENTS) + len(WELCOME['phrases'])} training phrases.")


if __name__ == "__main__":
    main()
