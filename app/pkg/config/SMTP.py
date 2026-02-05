import os
import smtplib
from email.message import EmailMessage


def send_email_msg(to: str, subject: str, body: str):
    msg = EmailMessage()
    msg["To"] = to
    msg["From"] = "Email Service <noreply@vidyasoft.com>"
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(str(os.getenv("SMTP_HOST")), int(os.getenv("SMTP_PORT", "2525")), timeout=5) as server:
        server.starttls()
        server.login(str(os.getenv("SMTP_USERNAME")),
                     str(os.getenv("SMTP_PASSWORD")))
        server.send_message(msg)
