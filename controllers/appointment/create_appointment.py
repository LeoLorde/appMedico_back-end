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
            'client_id': data.get('client_id'),
            'doctor_id': data.get('doctor_id'),
            'date': data.get('data_marcada', ''),
            'time': ''
        }
        
        try:
            validated_data = InputValidator.validate_appointment_data(validated_data)
        except ValidationError as e:
            return jsonify({'message': 'Erro de validação', 'errors': e.errors}), 400
        
        client = Client.query.get(validated_data['client_id'])
        if not client:
            return jsonify({'message': 'Cliente não encontrado'}), 404
        
        doctor = Doctor.query.get(validated_data['doctor_id'])
        if not doctor:
            return jsonify({'message': 'Médico não encontrado'}), 404
        
        if current_user.get('type') == 'client' and current_user.get('id') != validated_data['client_id']:
            return jsonify({'message': 'Você só pode criar agendamentos para si mesmo'}), 403
        
        appointment = Appointment(
            data_marcada=data.get('data_marcada'),
            client_id=validated_data['client_id'],
            doctor_id=validated_data['doctor_id']
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        return jsonify({
            'message': 'Agendamento criado com sucesso',
            'data': appointment.toMap()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao criar agendamento', 'error': str(e)}), 500
