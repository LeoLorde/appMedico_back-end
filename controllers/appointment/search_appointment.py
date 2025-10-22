from database import db
from models.appointment_model import Appointment
from models.doctor_model import Doctor
from flask import jsonify

def search_by_doctor_appointment(id):
    try:
        doctor = Doctor.query.get(id=id)
        if not doctor:
            return jsonify({'message': 'Médico não encontrado'}), 404

        app_list = Appointment.query.filter_by(doctor=id).all()
        
        return jsonify({
            'message': 'Agendamento criado com sucesso',
            'data': [app for app in app_list]
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao criar agendamento', 'error': str(e)}), 500
