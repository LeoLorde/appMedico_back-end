from database import db
from .user_model import User
from enum import Enum
from sqlalchemy import Enum as sqlenum

from cryptography.fernet import Fernet

class Doctor(User):
    crm = db.Column(db.String(128), nullable=False)
    speciality = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.String(255), nullable=False)
    _key = b'NAO-EH-SEGURO-TIRA-ESSA-MERDA'

    def set_crm(self, crm):
        cipher = Fernet(self._key)
        self.crm = cipher.encrypt(crm.encode()).decode()

    def check_crm(self, crm):
        cipher = Fernet(self._key)
        decrypted_crm = cipher.decrypt(self.crm.encode()).decode()
        return decrypted_crm == crm

    def toMap(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "bio": self.bio,
            "speciality": self.speciality
        }