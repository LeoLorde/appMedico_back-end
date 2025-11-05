from flask_jwt_extended import get_jwt_identity
from flask import jsonify, request
from models.expedient_model import Expediente
from models.doctor_model import Doctor
from models.appointment_model import Appointment
from utils.validators import InputValidator
from datetime import timedelta

def search_available_time():
    try:
        data : dict = request.get_json()
        doctor : Doctor = Doctor.query.filter_by(id=data.get("id")).first()
        expediente : Expediente =  doctor.expediente
        
        data_inicio = expediente.horario_inicio
        data_fim = expediente.horario_fim
        tempo_medio = doctor.horario_min
        
        def time_to_minutes(time_obj):
            return time_obj.hour * 60 + time_obj.minute
        
        def minutes_to_time(minutes):
            return timedelta(minutes=minutes)
        
        inicio_minutos = time_to_minutes(data_inicio)
        fim_minutos = time_to_minutes(data_fim)

        disponivel_em_minutos = fim_minutos - inicio_minutos
        num_horarios_disponiveis = disponivel_em_minutos // tempo_medio
        
        horarios_disponiveis = []

        appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            Appointment.is_confirmed == "confirmed"
        ).all()

        ocupados_em_minutos = set()
        for app in appointments:
            app_inicio_minutos = time_to_minutes(app.data_marcada.time())
            app_fim_minutos = app_inicio_minutos + app.duration 
            
            for m in range(app_inicio_minutos, app_fim_minutos, tempo_medio):
                ocupados_em_minutos.add(m)

        for i in range(num_horarios_disponiveis):
            horario_disponivel = inicio_minutos + (i * tempo_medio)
            if horario_disponivel not in ocupados_em_minutos:
                horario_obj = minutes_to_time(horario_disponivel)
                horarios_disponiveis.append(str(horario_obj))

        return jsonify({"Horarios": horarios_disponiveis})
        
    except Exception as e:
        return jsonify({'message': 'Erro ao buscar expediente', 'error': str(e)}), 500