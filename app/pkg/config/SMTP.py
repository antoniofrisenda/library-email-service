import os
import smtplib
import mimetypes
from io import BytesIO
from email.message import EmailMessage


def send_email_msg(to: str, subject: str, body: str, file_name: str | None  = None, file_bytes: BytesIO | None = None):
    msg = EmailMessage()
    msg["To"] = to
    msg["From"] = "Email Service <noreply@vidyasoft.com>"
    msg["Subject"] = subject
    msg.set_content(body)
    
    if file_name and file_bytes:
        file_data = file_bytes.getvalue()
        
        mime_type, _ = mimetypes.guess_type(file_name)
        if mime_type is None:
            mime_type = "application/octet-stream"
        maintype, subtype = mime_type.split("/", 1)
        
        msg.add_attachment(
            file_data,
            maintype=maintype,
            subtype=subtype,
            filename=file_name
        )
                    
    with smtplib.SMTP(str(os.getenv("SMTP_HOST")), int(os.getenv("SMTP_PORT", "2525")), timeout=5) as server:
        server.starttls()
        server.login(str(os.getenv("SMTP_USERNAME")),
                     str(os.getenv("SMTP_PASSWORD")))
        server.send_message(msg)
