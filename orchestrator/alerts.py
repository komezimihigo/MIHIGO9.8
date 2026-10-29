from __future__ import annotations

import os
import re
import smtplib
from email.message import EmailMessage
from typing import Iterable, Optional


def redact_secrets(text: str) -> str:
    patterns = [
        (r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*[^\s\r\n]+", r"\\1=[REDACTED]"),
        (r"(?i)(Authorization:\s*Bearer\s+)[A-Za-z0-9._-]+", r"\\1[REDACTED]"),
    ]
    sanitized = text
    for pattern, replacement in patterns:
        sanitized = re.sub(pattern, replacement, sanitized)
    return sanitized


class AlertEmail:
    def __init__(self, smtp_host: str, smtp_port: int = 587, username: Optional[str] = None, password: Optional[str] = None, sender: Optional[str] = None, recipient: Optional[str] = None, tls: bool = True) -> None:
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.sender = sender
        self.recipient = recipient
        self.tls = tls

    def send(self, subject: str, body: str) -> bool:
        if not self.smtp_host or not self.recipient:
            return False
        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = self.sender or self.username or "no-reply@example.com"
        message["To"] = self.recipient
        message.set_content(redact_secrets(body))
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10) as smtp:
                if self.tls:
                    smtp.starttls()
                if self.username and self.password:
                    smtp.login(self.username, self.password)
                smtp.send_message(message)
            return True
        except Exception:
            return False
