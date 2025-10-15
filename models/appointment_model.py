from database import db

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataDaConsulta = db.Column(db.DateTime, nullable=False)

    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False) 
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    client = db.relationship('Client', backref='appointments', lazy=True)
    doctor = db.relationship('Doctor', backref='appointments', lazy=True)
    
    def __repr__(self):
        return (
            f"<Appointment "
            f"dataDaConsulta={self.dataDaConsulta}, "
            f"client_id={self.client_id}, "
            f"doctor_id={self.doctor_id}>"
        )