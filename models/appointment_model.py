from database import db

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_marcada = db.Column(db.DateTime, nullable=False)

    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False) 
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    client = db.relationship('Client', backref='appointments', lazy=True)
    doctor = db.relationship('Doctor', backref='appointments', lazy=True)
    
    def __repr__(self):
        return (
            f"<Appointment "
            f"data_marcada={self.data_marcada}, "
            f"client_id={self.client_id}, "
            f"doctor_id={self.doctor_id}>"
        )
        
    def toMap(self):
        return {
            "data_marcada": self.data_marcada,
            "client_id": self.client_id,
            "doctor_id": self.doctor_id
        }