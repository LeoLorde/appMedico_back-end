from database import db
from .user_model import User
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum as sqlenum

class Gender(Enum):
    MAN = 1
    WOMAN = 2

from cryptography.fernet import Fernet

class Client(User):
    cpf = db.Column(db.String(128), nullable=False)
    dataDeNascimento = db.Column(db.DateTime, nullable=False)
    gender = db.Column(sqlenum(Gender), nullable=False)
    _key = b'NAO-EH-SEGURO-TIRA-ESSA-MERDA'

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