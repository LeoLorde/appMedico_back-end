from models.appointment_model import Appointment
from models.client_model import Client
from models.doctor_model import Doctor
from models.fcm_token_model import FcmToken
from models.user_model import User
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from utils.send_message import send_message
from datetime import datetime, timedelta

def get_doctor_and_client_with_request(data) -> tuple[Doctor, Client]:
    current_user = get_jwt_identity()
    
    validated_data = {
        'doctor_id': data.get('doctor_id'),
        'date': data.get('data_marcada', ''),
        'time': data.get('time', '')
    }
    
    client = Client.query.get(current_user)
    if not client:
        raise ValueError("Cliente não existe")
    
    doctor = Doctor.query.get(validated_data['doctor_id'])
    if not doctor:
        raise ValueError("Doutor não existe")
    
    return doctor, client

def calculate_end_time(data_marcada: str, duracao_minutos: int) -> datetime:
    inicio = datetime.fromisoformat(data_marcada).replace(tzinfo=None)
    fim = inicio + timedelta(minutes=duracao_minutos)
    return fim

def format_appointment_date(data_marcada: str):
    return datetime.fromisoformat(data_marcada).replace(tzinfo=None)

def check_user_datetime_is_free(user : User, appointment_time, end_time):
    user_appointments = Appointment.query.filter(
            Appointment.client_id == user.id
        ).all()

    for appointment in user_appointments:
        appointment_start = appointment.data_marcada
        appointment_end = appointment_start + timedelta(minutes=appointment.duration)
        if appointment_time < appointment_end and end_time > appointment_start:
            print("Não está dispnivel (medico)")
            return jsonify({'message': 'O médico não está disponível neste horário.'}), 400

def send_notification_to_users(user1: User, user2: User, appointment: Appointment):
        token : FcmToken = FcmToken.query.filter_by(user_id=user1.id).first()
        send_message(token.fcm_token, "Sua consulta foi enviada ao Doutor", "Consulta Enviada")
        
        token : FcmToken = FcmToken.query.filter_by(user_id=user2.id).first()
        send_message(token.fcm_token, f"Nova solicitação de consulta recebida: {appointment.motivo}", "Solicitação de Consulta")

def check_if_appointment_is_possible(doctor, client, data_marcada):
        duration_minutes = int(doctor.horario_min)
        end_time = calculate_end_time(data_marcada, duration_minutes)

        appointment_time = format_appointment_date(data_marcada)

        check_user_datetime_is_free(doctor, appointment_time, end_time)
        check_user_datetime_is_free(client, appointment_time, end_time)
        
        return duration_minutes, appointment_time
        
def create_appointment_model(appointment_time, client, doctor, motivo, duration):
        return Appointment(
            data_marcada=appointment_time,
            client_id=client.id,
            doctor_id=doctor.id,
            is_confirmed="pending",
            motivo=motivo,
            duration=duration
        )
