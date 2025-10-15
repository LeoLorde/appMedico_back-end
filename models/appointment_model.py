from database import db
from flask_sqlalchemy import SQLAlchemy

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataDaConsulta = db.Column(db.DateTime, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    def __repr__(self):
        return (
            f"<Appointments "
            f"dataDaConsulta={self.dataDaConsulta}, "
            f"clientId={self.cliente_id}, "
            f"doctorId={self.doctor_id}>"
        )