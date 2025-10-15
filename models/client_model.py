from database import db
from .user_model import User
from .gender_enum import Gender
from sqlalchemy import Enum as sqlenum
import os
import bcrypt

class Client(User):
    __tablename__ = "client"
    
    cpf = db.Column(db.String(128), nullable=False)
    dataDeNascimento = db.Column(db.DateTime, nullable=False)
    gender = db.Column(sqlenum(Gender, name="gender_enum"), nullable=False)

    def set_cpf(self, cpf):
        salt = bcrypt.gensalt()
        self.cpf = bcrypt.hashpw(cpf.encode(), salt).decode()

    def check_cpf(self, cpf):
        return bcrypt.checkpw(cpf.encode(), self.cpf.encode())

    def toMap(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "cpf": self.cpf, 
            "dataDeNascimento": self.dataDeNascimento,
            "genero": self.gender.name
        }