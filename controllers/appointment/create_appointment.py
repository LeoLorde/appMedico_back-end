from database import db
from models.appointment_model import Appointment
from models.client_model import Client
from models.doctor_model import Doctor
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

@jwt_required()
def create_appointment():
    print("RECEIVED REQUEST")
    try:
        data = request.get_json()
        current_user = get_jwt_identity()
        
        validated_data = {
            'doctor_id': data.get('doctor_id'),
            'date': data.get('data_marcada', ''),
            'time': ''
        }
        
        client = Client.query.get(current_user)
        if not client:
            return jsonify({'message': 'Cliente não encontrado'}), 404
        
        doctor = Doctor.query.get(validated_data['doctor_id'])
        if not doctor:
            return jsonify({'message': 'Médico não encontrado'}), 404
        
        if current_user != current_user:
            return jsonify({'message': 'Você só pode criar agendamentos para si mesmo'}), 403
        
        print(data.get('data_marcada'))
        appointment = Appointment(
            data_marcada=datetime.fromisoformat(data.get('data_marcada')),
            client_id=current_user,
            doctor_id=validated_data['doctor_id'],
            is_confirmed="pending"
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        return jsonify({
            'message': 'Agendamento criado com sucesso',
            'data': appointment.toMap()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'message': 'Erro ao criar agendamento', 'error': str(e)}), 500
