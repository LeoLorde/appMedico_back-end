import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()  # lê variáveis do .env

class Email:
    @staticmethod
    def parse(email: str) -> str:
        """Remove espaços e padroniza o domínio em minúsculo."""
        if not isinstance(email, str):
            raise TypeError("Email precisa ser uma string")
        email = email.strip()
        local, sep, domain = email.partition("@")
        return f"{local}@{domain.lower()}" if sep else email

    @staticmethod
    def is_valid(email: str) -> bool:
        """Validação simplificada de email."""
        email = Email.parse(email)

        if "@" not in email or email.count("@") != 1:
            return False

        local, domain = email.split("@")
        if not local or not domain:
            return False
        if "." not in domain:
            return False
        if domain.endswith("."):
            return False
        dominio_principal, *resto = domain.split(".")
        if not dominio_principal or any(not parte for parte in resto):
            return False

        return True

    @staticmethod
    def send_email(to_email: str, subject: str, body: str):
        """Envia um e-mail usando SMTP."""
        EMAIL_USER = os.getenv("EMAIL_USER")
        EMAIL_PASS = os.getenv("EMAIL_PASS")

        if not EMAIL_USER or not EMAIL_PASS:
            raise ValueError("Defina EMAIL_USER e EMAIL_PASS no .env")

        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
