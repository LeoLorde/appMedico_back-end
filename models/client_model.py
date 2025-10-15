from database import db
from .user_model import User
from enum import Enum
from sqlalchemy import Enum as sqlenum
import os

class Gender(Enum):
    MAN = 1
    WOMAN = 2

from cryptography.fernet import Fernet

crm_key = os.getenv("CRM_KEY")

class Client(User):
    cpf = db.Column(db.String(128), nullable=False)
    dataDeNascimento = db.Column(db.DateTime, nullable=False)
    gender = db.Column(sqlenum(Gender), nullable=False)
    _key = crm_key

    def set_cpf(self, cpf):
        cipher = Fernet(self._key)
        self.cpf = cipher.encrypt(cpf.encode()).decode()

    def check_cpf(self, cpf):
        cipher = Fernet(self._key)
        decrypted_cpf = cipher.decrypt(self.cpf.encode()).decode()
        return decrypted_cpf == cpf

    def toMap(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "dataDeNascimento": self.dataDeNascimento,
            "gender": self.gender
        }