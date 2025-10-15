from flask import request
from models.client_model import Client
from models.gender_enum import Gender
from database import db

def create_client():
    data = request.get_json()
    
    client = Client(
        username=data.get('username'),
        email=data.get('email'),
        dataDeNascimento=data.get('dataDeNascimento'),
        gender=Gender.parse_gender(data.get('genero')),
    )
    client.set_password(password=data.get('senha'))
    client.set_cpf(cpf=data.get('cpf'))
    
    db.session.add(client)
    db.session.commit()
    return {
        'message': 'Client criado com sucesso',
        'data': client.toMap()
    }, 201
