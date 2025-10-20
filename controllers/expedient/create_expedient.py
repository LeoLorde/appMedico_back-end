from database import db
from models.expedient_model import Expediente
from flask import request

def create_expedient():
    data = request.get_json()
    expedient = Expediente(
        horario_inicio=data.get('horario_inicio'),
        horario_fim=data.get('horario_fim'),
        dias_trabalho=data.get('dias_trabalho')
    )
    db.session.add(expedient)
    db.session.commit()
    return {
        'message': 'Expediente criado com sucesso',
        'data': expedient.to_map()
    }, 201