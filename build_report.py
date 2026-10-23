"""Create the Scam Shield AI summative assessment report."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).parent
OUTPUT = ROOT / "ScamShieldAI_Report.pdf"
STUDENT_NAME = "Aarav Motwani"
CRS_NAME = "Artificial Intelligence"
COURSE_NAME = "Artificial Intelligence: Real-World Applications and Implications"
INK = colors.HexColor("#142B34")
TEAL = colors.HexColor("#007D76")
PAPER = colors.HexColor("#F5F7F4")
PALE = colors.HexColor("#E6F2EF")
MUTED = colors.HexColor("#52636A")


def styles():
    base = getSampleStyleSheet()
    base.add(ParagraphStyle(name="EyebrowCustom", fontName="Helvetica-Bold", fontSize=8, leading=11, textColor=TEAL, spaceAfter=9))
    base.add(ParagraphStyle(name="TitleCustom", fontName="Helvetica-Bold", fontSize=27, leading=32, textColor=INK, spaceAfter=11))
    base.add(ParagraphStyle(name="DeckCustom", fontName="Helvetica", fontSize=11, leading=16, textColor=MUTED, spaceAfter=20))
    base.add(ParagraphStyle(name="SectionCustom", fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=INK, spaceBefore=14, spaceAfter=8))
    base.add(ParagraphStyle(name="BodyCustom", fontName="Helvetica", fontSize=9, leading=14, textColor=INK, spaceAfter=8))
    base.add(ParagraphStyle(name="SmallCustom", fontName="Helvetica", fontSize=7.6, leading=11, textColor=INK, spaceAfter=4))
    base.add(ParagraphStyle(name="TableHeadCustom", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=colors.white))
    base.add(ParagraphStyle(name="TableCellCustom", fontName="Helvetica", fontSize=7.5, leading=10.2, textColor=INK))
    base.add(ParagraphStyle(name="CalloutCustom", fontName="Helvetica-Bold", fontSize=9, leading=14, textColor=INK))
    return base


S = styles()


def p(text: str, style="BodyCustom"):
    return Paragraph(text, S[style])


def section(title: str):
    return p(title, "SectionCustom")


def table(rows, widths):
    formatted = []
    for index, row in enumerate(rows):
        kind = "TableHeadCustom" if index == 0 else "TableCellCustom"
        formatted.append([p(str(cell), kind) for cell in row])
    result = Table(formatted, colWidths=widths, repeatRows=1, hAlign="LEFT")
    result.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TEAL),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PAPER]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.HexColor("#D8E2DE")),
    ]))
    return result


def footer(canvas, doc):
    canvas.saveState()
    width, _ = doc.pagesize
    canvas.setStrokeColor(colors.HexColor("#D8E2DE"))
    canvas.line(44, 38, width - 44, 38)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(44, 26, "SCAMSHIELD AI  /  AARAV MOTWANI")
    canvas.drawRightString(width - 44, 26, str(doc.page))
    canvas.restoreState()


def build():
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=(595.3, 841.9), rightMargin=44, leftMargin=44,
        topMargin=50, bottomMargin=56, title="ScamShield AI - SA final submission",
        author="Aarav Motwani",
    )
    flow = [
        p("IBCP YEAR 1  /  ARTIFICIAL INTELLIGENCE  /  SUMMATIVE ASSESSMENT", "EyebrowCustom"),
        p("Scam Shield AI", "TitleCustom"),
        p("A Dialogflow ES fraud-awareness assistant with implementation and console results", "DeckCustom"),
        HRFlowable(width="100%", thickness=1, color=TEAL),
        Spacer(1, 18),
        table([
            ["STUDENT", "PLATFORM", "DELIVERABLE"],
            [STUDENT_NAME, "Google Dialogflow ES", "Agent, tests and project documentation"],
        ], [150, 165, 192]),
        Spacer(1, 10),
        table([
            ["CRS NAME", "COURSE NAME"],
            [CRS_NAME, COURSE_NAME],
        ], [210, 297]),
        section("01  The problem"),
        p("People who get payment requests, fake job offers, impersonation calls or unfamiliar links may react quickly without checking who is contacting them. Scam Shield AI gives advice and a safe path to official help. Scam Shield AI does not say that a message or sender is genuine."),
        section("02  Audience and design goals"),
        p("The main users are people who use payments, students, job seekers, older adults and anyone who may have already shared information or sent money. The response design focuses on a warning, an explanation and a safe next step. The response does not ask users to share OTPs, UPI PINs, passwords, CVVs or full account details."),
        section("03  Solution architecture"),
        p("The agent package contains <b>21 intents</b>, including welcome and fallback. It contains <b>10 custom entities</b> and <b>240 example training phrases</b>. Each custom intent contains 12 example phrases. A required requested-action parameter shows slot filling. Short-lived contexts help with scam-detail follow-up and an OTP-safety quiz. Quick replies guide users to clear steps. The agent works without a webhook or a personal data store."),
        table([
            ["USER NEED", "INTENT GROUP", "SAFETY OUTCOME"],
            ["Check a message", "ScamCheck, ScamDetails", "Pause action; describe the request without sharing secrets"],
            ["Understand a scam pattern", "OTP, UPI, QR, phishing, job, investment, loan, impersonation, remote access", "Recognise warning signs and verify independently"],
            ["Recover and report", "AccountCompromised, ReportFraud, PreserveEvidence", "Contact bank quickly; use reporting routes"],
            ["Learn and navigate", "SafePaymentTips, quiz, welcome, fallback, goodbye", "Practice a safe response and recover from unclear input"],
        ], [126, 158, 223]),
        PageBreak(),
        p("DESIGN DETAIL", "EyebrowCustom"),
        section("04  Language understanding"),
        p("Custom entities identify the scam type, contact channel, requested action, credential type, payment method, claimed identity, urgency cue, suspicious-link feature, job fee and whether harm has already happened. Synonyms include variations like one-time password, UPI collect request, and registration fee. The agent stays safe even if a phrase is misclassified."),
        table([
            ["ENTITY", "EXAMPLE VALUES", "WHY IT MATTERS"],
            ["@scam-type", "UPI fraud, phishing, job scam", "Routes to relevant advice"],
            ["@requested-action", "share OTP, send money, open link", "Supports required follow-up slot"],
            ["@credential-type", "OTP, UPI PIN, password", "Highlights secrets never to disclose"],
            ["@payment-method", "UPI, QR code, card", "Explains payment-specific risk"],
            ["@contact-channel", "WhatsApp, SMS, call", "Captures where contact happened"],
            ["@impersonated-identity", "bank, employer, support", "Identifies authority claims"],
            ["@urgency-cue", "immediately, account will close", "Recognises pressure tactics"],
            ["@link-feature", "shortened link, misspelled domain", "Recognises suspicious links"],
            ["@job-fee", "registration fee, deposit", "Flags upfront-payment requests"],
            ["@loss-status", "money sent, app installed", "Prioritises urgent recovery"],
        ], [125, 177, 205]),
        section("05  Example conversation"),
        table([
            ["STEP", "USER / AGENT"],
            ["1. User", "Can you check if this message is a scam?"],
            ["2. Agent", "I cannot verify that a message is safe from a description alone. Do not click links, pay or share codes. What did they ask you to do?"],
            ["3. User", "They want me to share my OTP."],
            ["4. Agent", "That is a warning sign. Do not share the OTP. Contact the organisation using its app or website, not the sender's link or number."],
        ], [92, 415]),
        section("06  Safety boundaries"),
        p("The bot gives advice. It does not detect fraud automatically. It is not a bank representative. It never asks for secrets. It never says a transaction is safe. If money has been lost it tells the user to contact their bank. It also directs them to India's cyber-fraud helpline 1930 and cybercrime.gov.in. Advice follows NPCI and RBI fraud-awareness guidance."),
        PageBreak(),
        p("DIALOGFLOW CONSOLE EVIDENCE", "EyebrowCustom"),
        section("07  Test protocol"),
        p("A live Dialogflow ES console pass covered ten cases: five scam-scenario intents, remote access, a slot/context follow-up, both quiz branches, and fallback. Three further English inputs passed on 22 October 2026."),
    ]
    rows = [["SCENARIO", "EXPECTED MATCH", "OBSERVED RESULT"]]
    rows.extend([
        ["UPI collect request", "UPICollectIntent", "Matched; UPI extracted; safe warning returned"],
        ["OTP impersonation", "OTPIntent", "Matched; OTP extracted; advised not to share it"],
        ["Fake job fee", "FakeJobIntent", "Matched; warned about registration fees"],
        ["Phishing link", "PhishingLinkIntent", "Matched; warned against shortened SMS link"],
        ["Remote access", "RemoteAccessIntent", "Matched; warned against remote-control app"],
        ["Money already lost", "AccountCompromisedIntent", "Matched; bank, 1930 and portal guidance returned"],
        ["Scam detail follow-up", "ScamCheckIntent -> ScamDetailsIntent", "Matched; requested action captured; safe advice returned"],
        ["Quiz safe answer", "QuizStartIntent -> QuizSafeAnswerIntent", "Matched; confirmed OTPs must not be shared"],
        ["Quiz unsafe answer", "QuizStartIntent -> QuizUnsafeAnswerIntent", "Matched; corrected unsafe answer"],
        ["Fallback", "Default Fallback Intent", "Matched; safe options and 1930 guidance returned"],
    ])
    flow.extend([
        table(rows, [100, 124, 283]),
        section("08  Recorded implementation"),
        p("The Dialogflow ES console agent is ScamShieldAI (agent ID scamshieldai-k9we), with 21 intents and 10 custom entities. Ten English scenarios and three additional English inputs passed in the console. The chatbot is demonstrated through the Dialogflow ES console."),
        section("09  Sources"),
        p("SA brief: CRS AI Y1C1 Artificial Intelligence - Real-World Applications and Implications (Summative Assessment).", "SmallCustom"),
        p("Google Cloud Dialogflow ES documentation: agent import/export and intent parameters.", "SmallCustom"),
        p("Google Cloud Dialogflow Web Demo documentation: default-language limitation.", "SmallCustom"),
        p("National Payments Corporation of India: fraud awareness. Reserve Bank of India: digital banking safeguards.", "SmallCustom"),
        p("National Cybercrime Reporting Portal: cybercrime.gov.in and financial cyber-fraud helpline 1930.", "SmallCustom"),
    ])
    doc.build(flow, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    build()
