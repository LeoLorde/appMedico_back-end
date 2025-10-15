from database import db
from .user_model import User
import os
import bcrypt

class Doctor(User):
    __tablename__ = "doctor"
    
    crm = db.Column(db.String(128), nullable=False) 
    especialidade = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.String(255), nullable=False)
    
    endereco_id = db.Column(db.Integer, db.ForeignKey('adress.id'), nullable=False)
    endereco = db.relationship('Adress', backref='doctor', uselist=False)  

    appointments = db.relationship(
        "Appointment",
        backref="doctor", 
        cascade="all, delete-orphan", 
        lazy=True
    )

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
