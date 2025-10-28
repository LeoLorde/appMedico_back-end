from database import db
from models.appointment_model import Appointment
from models.doctor_model import Doctor
from models.client_model import Client
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
        app_list = Appointment.query.filter_by(doctor_id=id).filter(Appointment.is_confirmed != "refused").all()
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

@jwt_required()
def search_by_doctor_pending_appointment():
    try:
        id = get_jwt_identity()
        print(id)
        doctor = Doctor.query.get(id)
        print(doctor)
        if not doctor:
            print("Não achamos doutor")
            return jsonify({'message': 'Médico não encontrado'}), 404

        app_list = Appointment.query.filter_by(doctor_id=id).filter_by(is_confirmed="pending").all()
        
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

@jwt_required()
def search_by_client_appointment():
    try:
        id = get_jwt_identity()
        print(id)
        client = Client.query.get(id)
        print(client)
        if not client:
            print("Não achamos cliente")
            return jsonify({'message': 'Cliente não encontrado'}), 404

        app_list = Appointment.query.filter_by(client_id=id).filter(Appointment.is_confirmed != "refused").all()
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
