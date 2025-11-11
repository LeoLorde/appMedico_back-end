from database import db
from models.expedient_model import Expediente
from models.doctor_model import Doctor
from flask import request
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

@jwt_required()
def create_expedient():
    print("PORRA")
    try:
        print("PEGANDO DOCTOR ID")
        doctor_id = get_jwt_identity()
        print("DOCTOR ID ENCONTRADO")
        data: dict = request.get_json()
        print("PEGANDO DADOS")
        
        horario_inicio_str = data.get('horario_inicio')
        horario_fim_str = data.get('horario_fim')
        print("DADOS PEGOS:\n")
        print("FIM: " + horario_fim_str)
        print("INICIO: " + horario_inicio_str)
        horario_inicio = datetime.strptime(horario_inicio_str + ":00", "%H:%M:%S").time()
        horario_fim = datetime.strptime(horario_fim_str + ':00', "%H:%M:%S").time()
        
        expedient = Expediente(
            horario_inicio=horario_inicio,
            horario_fim=horario_fim,
            dias_trabalho=data.get('dias_trabalho'),
        )
        
        doctor: Doctor = Doctor.query.filter_by(id=doctor_id).first()
        doctor.expediente = expedient
        
        db.session.add(expedient)
        db.session.commit()
        
        return {
            'message': 'Expediente criado com sucesso',
            'data': expedient.to_map()
        }, 201
    except Exception as e:
        print(e)
        return {'error': str(e)}, 400