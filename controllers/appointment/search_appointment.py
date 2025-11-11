from database import db
from models.appointment_model import Appointment
from models.doctor_model import Doctor
from models.client_model import Client
from flask import jsonify, request
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

@jwt_required()
def search_by_doctor_appointment():
    try:
        id = get_jwt_identity()
        doctor = Doctor.query.get(id)
        if not doctor:
            return jsonify({'message': 'Médico não encontrado'}), 404
        app_list = Appointment.query.filter_by(doctor_id=id).filter(Appointment.is_confirmed != "refused").all()
        lista = [app.toMap() for app in app_list]
        return jsonify({
            'message': 'Agendamento criado com sucesso',
            'data': [{"appointment": app.toMap(), "client": Client.query.get(app.client_id).toMap() } for app in app_list]
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'message': 'Erro ao criar agendamento', 'error': str(e)}), 500

@jwt_required()
def search_by_doctor_pending_appointment():
    try:
        id = get_jwt_identity()
        doctor = Doctor.query.get(id)
        if not doctor:
            return jsonify({'message': 'Médico não encontrado'}), 404

        app_list = Appointment.query.filter_by(doctor_id=id).filter_by(is_confirmed="pending").all()
        return jsonify({
            'message': 'Agendamento criado com sucesso',
            'data': [app.toMap() for app in app_list]
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'message': 'Erro ao criar agendamento', 'error': str(e)}), 500

@jwt_required()
def search_by_client_appointment():
    try:
        id = get_jwt_identity()
        client = Client.query.get(id)
        if not client:
            print("Não achamos cliente")
            return jsonify({'message': 'Cliente não encontrado'}), 404

        app_list = Appointment.query.filter_by(client_id=id).filter(Appointment.is_confirmed == "confirmed").all()
        dicto = {
            'message': 'Agendamentos encontrados com sucesso',
            'data': [
                {
                    "appointment": app.toMap(),
                    'doctor': Doctor.query.get(app.doctor_id).toMap()
                }
                for app in app_list
            ]
        }
        print(dicto)
        return jsonify(dicto), 200

        
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'message': 'Erro ao criar agendamento', 'error': str(e)}), 500

@jwt_required()
def search_appointments_by_day(data_param):
    try:
        user_id = get_jwt_identity()
        if not data_param:
            return jsonify({'message': 'É necessário enviar o parâmetro ?date=YYYY-MM-DD'}), 400

        try:
            search_date = datetime.strptime(data_param, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'message': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400

        start_datetime = datetime.combine(search_date, datetime.min.time())
        end_datetime = datetime.combine(search_date, datetime.max.time())

        doctor = Doctor.query.get(user_id)
        client = Client.query.get(user_id)

        if doctor:
            print("Usuário é médico")
            appointments = Appointment.query.filter(
                Appointment.doctor_id == user_id,
                Appointment.data_marcada >= start_datetime,
                Appointment.data_marcada <= end_datetime,
                Appointment.is_confirmed != "refused"
            ).all()

        elif client:
            print("Usuário é cliente")
            appointments = Appointment.query.filter(
                Appointment.client_id == user_id,
                Appointment.data_marcada >= start_datetime,
                Appointment.data_marcada <= end_datetime,
                Appointment.is_confirmed != "refused"
            ).all()

        else:
            return jsonify({'message': 'Usuário não é cliente nem médico.'}), 403

        lista = [appt.toMap() for appt in appointments]

        return jsonify({
            'message': 'Agendamentos encontrados com sucesso',
            'data': lista
        }), 200

    except Exception as e:
        db.session.rollback()
        print("Erro em search_appointments_by_day:", e)
        return jsonify({'message': 'Erro ao buscar agendamentos', 'error': str(e)}), 500