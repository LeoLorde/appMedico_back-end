from flask_jwt_extended import get_jwt_identity
from flask import jsonify, request
from models.expedient_model import Expediente
from models.doctor_model import Doctor
from utils.validators import InputValidator

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

        inicio_minutos = time_to_minutes(data_inicio)
        fim_minutos = time_to_minutes(data_fim)

        disponivel_em_minutos = fim_minutos - inicio_minutos

        num_horarios_disponiveis = disponivel_em_minutos // tempo_medio

        print(f'Número de horários disponíveis: {num_horarios_disponiveis}')
        return {"Horarios" : num_horarios_disponiveis}

        
    except Exception as e:
        return jsonify({'message': 'Erro ao buscar expediente', 'error': str(e)}), 500
