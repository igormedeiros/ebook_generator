import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Optional

from .config import get_config

def send_epub_email(epub_path: str, title: str, recipient_email: Optional[str] = None) -> bool:
    """
    Sends the generated EPUB file via email using SMTP configuration.

    Args:
        epub_path: Path to the .epub file.
        title: Title of the ebook (for subject/body formatting).
        recipient_email: Optional override for recipient email. If None, uses env var.

    Returns:
        bool: True if sent successfully, False otherwise.
    """
    # Load email config
    email_config = get_config("email_notification")
    if not email_config.get("enabled", False):
        print("Email notification is disabled in config.")
        return False

    # Load SMTP credentials from environment
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    sender_email = os.getenv("EMAIL_SENDER")

    # Determine recipient
    to_email = recipient_email or os.getenv("EMAIL_RECIPIENT")

    if not all([smtp_server, smtp_port, smtp_username, smtp_password, sender_email, to_email]):
        print("Missing SMTP environment variables. Please check .env file.")
        return False

    if not os.path.exists(epub_path):
        print(f"EPUB file not found at: {epub_path}")
        return False

    try:
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email

        # Format subject and body
        subject_tmpl = email_config.get("subject", "Ebook Generated: {title}")
        body_tmpl = email_config.get("body", "Please find attached the ebook '{title}'.")

        msg['Subject'] = subject_tmpl.format(title=title)
        body = body_tmpl.format(title=title)

        msg.attach(MIMEText(body, 'plain'))

        # Attach the EPUB file
        file_path = Path(epub_path)
        with open(file_path, "rb") as f:
            part = MIMEApplication(
                f.read(),
                Name=file_path.name
            )

        # After the file is closed
        part['Content-Disposition'] = f'attachment; filename="{file_path.name}"'
        msg.attach(part)

        # Connect and send
        print(f"Connecting to SMTP server {smtp_server}:{smtp_port}...")
        with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        print(f"Email sent successfully to {to_email}")
        return True

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False
