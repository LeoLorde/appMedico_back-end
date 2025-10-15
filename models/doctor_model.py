from database import db
from .user_model import User
import os
from cryptography.fernet import Fernet

crm_key = os.getenv("CRM_KEY")

class Doctor(User):
    __tablename__ = "doctor"
    
    crm = db.Column(db.String(128), nullable=False)
    especialidade = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.String(255), nullable=False)
    _key = crm_key
    
    endereco_id = db.Column(db.Integer, db.ForeignKey('adress.id'), nullable=False)
    endereco = db.relationship('Adress', backref='doctor', uselist=False)  

    appointments = db.relationship(
        "Appointment",
        backref="doctor", 
        cascade="all, delete-orphan", 
        lazy=True
    )

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
            "especialidade": self.especialidade,
            "endereco_id": self.endereco_id
        }
