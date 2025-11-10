from models.appointment_model import Appointment
from flask import jsonify

def search_all():
    try:
        app_list = Appointment.query.all()
        return jsonify({
            'message': 'Agendamento criado com sucesso',
            'data': [app.toMap() for app in app_list]
        }), 200
        
    except Exception as e:
        print(e)
        return jsonify({'message': 'Erro ao criar agendamento', 'error': str(e)}), 500
