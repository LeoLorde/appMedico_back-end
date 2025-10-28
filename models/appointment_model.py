from database import db
import uuid

class Appointment(db.Model):
    id = db.Column(db.String(128), primary_key=True, default=lambda: str(uuid.uuid4()))
    data_marcada = db.Column(db.DateTime, nullable=False)

    client_id = db.Column(db.String(128), db.ForeignKey('client.id'), nullable=False) 
    doctor_id = db.Column(db.String(128), db.ForeignKey('doctor.id'), nullable=False)
    motivo = db.Column(db.String(128), nullable=True)
    plano_de_saude = db.Column(db.String(256), nullable=False, default="none")

    client = db.relationship('Client', backref='appointments', lazy=True)
    doctor = db.relationship('Doctor', backref='appointments', lazy=True)
    
    is_confirmed = db.Column(db.String(32), nullable=False)
    
    def __repr__(self):
        return (
            f"<Appointment "
            f"data_marcada={self.data_marcada}, "
            f"client_id={self.client_id}, "
            f"doctor_id={self.doctor_id}>"
        )
        
    def toMap(self):
        return {
            "data_marcada": self.data_marcada.isoformat() if self.data_marcada else None,
            "client_id": self.client_id,
            "doctor_id": self.doctor_id,
            "id": self.id,
            "motivo": self.motivo,
            "plano_de_saude": self.plano_de_saude,
            "is_confirmed": self.is_confirmed
        }
