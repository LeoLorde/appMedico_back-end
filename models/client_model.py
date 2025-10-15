from database import db
from .user_model import User
from .gender_enum import Gender
from sqlalchemy import Enum as sqlenum
import os
from cryptography.fernet import Fernet

cpf_key = os.getenv("CPF_KEY")

class Client(User):
    __tablename__ = "client"
    
    cpf = db.Column(db.String(128), nullable=False)
    dataDeNascimento = db.Column(db.DateTime, nullable=False)
    gender = db.Column(sqlenum(Gender, name="gender_enum"), nullable=False)
    _key = cpf_key

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
            "cpf": self.cpf,
            "dataDeNascimento": self.dataDeNascimento,
            "gender": self.gender.name
        }
