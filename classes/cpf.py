import re

class CPF():
    @staticmethod
    def parse_cpf(cpf: str) -> str:
        """Remove caracteres não numéricos e retorna somente os 11 dígitos."""
        return re.sub(r'\D', '', cpf)

    @staticmethod
    def validator(cpf: str) -> bool:
        """Valida um CPF (com ou sem máscara)."""
        cpf = CPF.parse_cpf(cpf)

        if len(cpf) != 11:
            return False

        if cpf == cpf[0] * 11:
            return False

        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        primeiro_dv = (soma * 10) % 11
        if primeiro_dv == 10:
            primeiro_dv = 0

        if primeiro_dv != int(cpf[9]):
            return False

        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        segundo_dv = (soma * 10) % 11
        if segundo_dv == 10:
            segundo_dv = 0

        if segundo_dv != int(cpf[10]):
            return False

        return True
