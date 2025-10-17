from enum import Enum

class Gender(Enum):
    MAN = 1
    WOMAN = 2
    NONE = 3

    @staticmethod
    def parse_gender(gender_value):
        if isinstance(gender_value, Gender): 
            return gender_value
        if isinstance(gender_value, int):  
            return Gender(gender_value)
        if isinstance(gender_value, str):
            try:
                return Gender[gender_value.upper()]
            except KeyError:
                raise ValueError("Valor de gênero inválido")
        raise ValueError("Valor de gênero inválido")
