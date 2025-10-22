from database import db
from models.appointment_model import Appointment
from models.client_model import Client
from models.doctor_model import Doctor
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.validators import InputValidator, ValidationError

@jwt_required()
def create_appointment():
    try:
        data = request.get_json()
        current_user = get_jwt_identity()
        
        validated_data = {
            'doctor_id': data.get('doctor_id'),
        }
        
        try:
            validated_data = InputValidator.validate_appointment_data(validated_data)
        except ValidationError as e:
            return jsonify({'message': 'Erro de validação', 'errors': e.errors}), 400
        
        doctor = Doctor.query.get(validated_data['doctor_id'])
        if not doctor:
            return jsonify({'message': 'Médico não encontrado'}), 404

        app_list = Appointment.query.filter_by(doctor=validated_data['doctor_id']).all()
        
        return jsonify({
            'message': 'Agendamento criado com sucesso',
            'data': [app for app in app_list]
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao criar agendamento', 'error': str(e)}), 500
