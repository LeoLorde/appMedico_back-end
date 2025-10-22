from database import db
from models.appointment_model import Appointment
from models.doctor_model import Doctor
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

@jwt_required()
def search_by_doctor_appointment():
    try:
        id = get_jwt_identity()
        print(id)
        doctor = Doctor.query.get(id)
        print(doctor)
        if not doctor:
            return jsonify({'message': 'Médico não encontrado'}), 404

        app_list = Appointment.query.filter_by(doctor_id=id).all()
        
        lista = [app.toMap() for app in app_list]
        print(lista)
        return jsonify({
            'message': 'Agendamento criado com sucesso',
            'data': [app.toMap() for app in app_list]
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'message': 'Erro ao criar agendamento', 'error': str(e)}), 500
