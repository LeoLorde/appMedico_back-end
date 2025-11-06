from flask import request, jsonify
from flask_jwt_extended import jwt_required
from create_appointment_logic import get_doctor_and_client_with_request, check_if_appointment_is_possible, create_appointment_model, send_notification_to_users
from database import db

@jwt_required()
def create_appointment():
    try:
        doctor, client = get_doctor_and_client_with_request(request.get_json())
        
        duration, start_time = check_if_appointment_is_possible(doctor, client, request.get_json()["data_marcada"])
        appointment = create_appointment_model(start_time, client, doctor, request.get_json()["motivo"], duration)
        
        send_notification_to_users(client, doctor, appointment)
        
        db.session.add(appointment)
        db.session.commit()

        return jsonify({
            'message': 'Agendamento criado com sucesso',
            'data': appointment.toMap()
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'message': 'Erro ao criar agendamento', 'error': str(e)}), 500