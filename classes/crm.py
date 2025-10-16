class CRM:
    @staticmethod
    def parse(crm: str) -> str:
        """Remove espaços e padroniza o CRM em maiúsculo."""
        if not isinstance(crm, str):
            raise TypeError("CRM precisa ser uma string")
        return crm.strip().upper().replace(" ", "")

    @staticmethod
    def is_valid(crm: str) -> bool:
        """Validação simplificada de CRM."""
        crm = CRM.parse(crm)

        if len(crm) < 6:
            return False

        numeros = ""
        letras = ""
        for c in crm:
            if c.isdigit():
                if letras:
                    return False
                numeros += c
            elif c.isalpha():
                letras += c
            elif c in "-/":
                continue 
            else:
                return False 
        if len(numeros) < 4 or len(letras) != 2:
            return False

        return True
