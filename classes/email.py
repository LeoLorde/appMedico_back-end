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
