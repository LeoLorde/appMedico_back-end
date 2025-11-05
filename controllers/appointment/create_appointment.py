from database import db
from models.appointment_model import Appointment
from models.client_model import Client
from models.doctor_model import Doctor
from models.fcm_token_model import FcmToken
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.send_message import send_message
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
        
        duration_minutes = int(doctor.horario_min)
        appointment_time = datetime.fromisoformat(data.get('data_marcada'))
        appointment_time = appointment_time.replace(tzinfo=None)
        end_time = appointment_time + timedelta(minutes=duration_minutes)

        doctor_appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor.id
        ).all()

        for appt in doctor_appointments:
            appt_start = appt.data_marcada
            appt_end = appt_start + timedelta(minutes=appt.duration)
            if appointment_time < appt_end and end_time > appt_start:
                print("Não está dispnivel (medico)")
                return jsonify({'message': 'O médico não está disponível neste horário.'}), 400

        client_appointments = Appointment.query.filter(
            Appointment.client_id == current_user
        ).all()

        for appt in client_appointments:
            appt : Appointment = appt
            appt_start = appt.data_marcada
            appt_end = appt_start + timedelta(minutes=appt.duration)
            if appointment_time < appt_end and end_time > appt_start:
                return jsonify({'message': 'Você já tem um agendamento nesse horário.'}), 400

        print("--------")
        print(f"DATA RECEBIDA: {data.get("data_marcada")}")
        print(f"DATA UTILIZADA: {appt.data_marcada}")
        print("--------")
        
        
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
        doctor : Doctor = doctor
        
        token : FcmToken = FcmToken.query.filter_by(user_id=client.id).first()
        send_message(token.fcm_token, "Sua consulta foi enviada ao Doutor", "Consulta Enviada")
        
        token : FcmToken = FcmToken.query.filter_by(user_id=doctor.id).first()
        send_message(token.fcm_token, f"Nova solicitação de consulta recebida: {appointment.motivo}", "Solicitação de Consulta")

        print("DB URI:", db.engine.url)
        print(f"Agendamento criado para {appointment_time} - {end_time}")

        return jsonify({
            'message': 'Agendamento criado com sucesso',
            'data': appointment.toMap()
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'message': 'Erro ao criar agendamento', 'error': str(e)}), 500
