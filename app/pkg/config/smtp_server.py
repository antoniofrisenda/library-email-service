import os
import smtplib
import mimetypes
from io import BytesIO
from email.message import EmailMessage


class SMTPServer:
    def __init__(self):
        self.host = str(os.getenv("SMTP_HOST"))
        self.port = int(os.getenv("SMTP_PORT", "2525"))
        self.username = str(os.getenv("SMTP_USERNAME"))
        self.password = str(os.getenv("SMTP_PASSWORD"))

        if not all([self.host, self.username, self.password]):
            raise ValueError("SMTP_HOST, SMTP_USERNAME and SMTP_PASSWORD are required")

    def send_email_msg(self, to: str, subject: str, body: str,
                       file_name: str | None = None,
                       file_bytes: BytesIO | None = None
                    ):

        msg = EmailMessage()
        msg["To"] = to
        msg["From"] = "Email Service <noreply@vidyasoft.com>"
        msg["Subject"] = subject
        msg.set_content(body)

        if file_name and file_bytes:
            file_type, _ = mimetypes.guess_type(file_name)
            if not file_type:
                file_type = "application/octet-stream"
            try:
                maintype, subtype = file_type.split("/", 1)
            except ValueError:
                maintype, subtype = "application", "octet-stream"

            msg.add_attachment(
                file_bytes.getvalue(),
                maintype=maintype,
                subtype=subtype,
                filename=file_name
            )

            with smtplib.SMTP(self.host, self.port, timeout=5) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
