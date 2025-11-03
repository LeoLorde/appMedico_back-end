from database import db
from models.appointment_model import Appointment
from models.client_model import Client
from models.doctor_model import Doctor
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta

@jwt_required()
def create_appointment():
    print("RECEIVED REQUEST")
    try:
        data = request.get_json()
        current_user = get_jwt_identity()
        
        validated_data = {
            'doctor_id': data.get('doctor_id'),
            'date': data.get('data_marcada', ''),
            'time': data.get('time', '')
        }
        
        client = Client.query.get(current_user)
        if not client:
            return jsonify({'message': 'Cliente não encontrado'}), 404
        
        doctor = Doctor.query.get(validated_data['doctor_id'])
        if not doctor:
            return jsonify({'message': 'Médico não encontrado'}), 404
        
        if current_user != current_user:
            return jsonify({'message': 'Você só pode criar agendamentos para si mesmo'}), 403
        
        appointment_time = datetime.fromisoformat(data.get('data_marcada'))
        duration_minutes = doctor.horario_min 
        end_time = appointment_time + timedelta(minutes=duration_minutes)
        
        doctor_appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            Appointment.data_marcada < end_time,
            (Appointment.data_marcada + timedelta(minutes=Appointment.duration)) > appointment_time
        ).all()
        
        if doctor_appointments:
            return jsonify({'message': 'O médico não está disponível neste horário.'}), 400

        client_appointments = Appointment.query.filter(
            Appointment.client_id == current_user,
            Appointment.data_marcada < end_time,
            (Appointment.data_marcada + timedelta(minutes=Appointment.duration)) > appointment_time
        ).all()

        if client_appointments:
            return jsonify({'message': 'Você já tem um agendamento nesse horário.'}), 400

        appointment = Appointment(
            data_marcada=appointment_time,
            client_id=current_user,
            doctor_id=validated_data['doctor_id'],
            is_confirmed="pending",
            motivo=data.get("motivo"),
            duration=duration_minutes
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
