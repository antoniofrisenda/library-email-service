import smtplib
import mimetypes
from io import BytesIO
from app.pkg.util import get_env
from email.message import EmailMessage

class SMTPServer:
    def __init__(self) -> None:
        self.host = str(get_env("SMTP_HOST"))
        self.port = int(get_env("SMTP_PORT"))
        self.username = str(get_env("SMTP_USERNAME"))
        self.password = str(get_env("SMTP_PASSWORD"))

        if not all([self.host, self.username, self.password]):
            raise ValueError("Missing credentials are required")

    def send_email_msg(self, to: str, subject: str, body: str, file_name: str | None = None, file_bytes: BytesIO | None = None) -> None:
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
