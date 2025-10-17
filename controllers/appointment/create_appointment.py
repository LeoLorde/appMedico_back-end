from database import db
from models.appointment_model import Appointment
from flask import request, jsonify

def create_appointment():
    data = request.get_json()
    appointment : Appointment = Appointment(
        data_marcada=data.get('data_marcada'),
        client_id=data.get('client_id'),
        doctor_id=data.get('doctor_id')
    )
    db.session.add(appointment)
    db.session.commit()
    return jsonify({
        'message': 'Appointment criado com sucesso',
        'data': appointment.toMap()
    }), 201