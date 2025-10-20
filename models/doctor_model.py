from database import db
from .user_model import User
import os
import bcrypt

class Doctor(User):
    __tablename__ = "doctor"
    
    crm = db.Column(db.String(128), nullable=False, unique=True) 
    especialidade = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.String(255), nullable=False)
    
    endereco_id = db.Column(db.String(128), db.ForeignKey('address.id'), nullable=False)
    endereco = db.relationship('Address', backref='doctor', uselist=False)  
    
    expedient_id = db.Column(db.String(128), db.ForeignKey('expediente.id'), nullable=True)
    expedient = db.relationship('Expediente', backreg='doctor', uselist=False)

    def set_crm(self, crm):
        salt = bcrypt.gensalt()
        self.crm = bcrypt.hashpw(crm.encode(), salt).decode() 

    def check_crm(self, crm):
        return bcrypt.checkpw(crm.encode(), self.crm.encode())

    def toMap(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "bio": self.bio,
            "especialidade": self.especialidade,
            "endereco_id": self.endereco_id
        }
