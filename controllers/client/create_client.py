from flask import request
from models.client_model import Client
from models.gender_enum import Gender
from datetime import datetime
from database import db

def create_client():
    data = request.get_json()
    
    print(data)
    
    client = Client(
        username=data.get('username'),
        email=data.get('email'),
        dataDeNascimento=datetime.strptime(data.get('dataDeNascimento'), '%Y-%m-%d').date(),
        gender=Gender.parse_gender(data.get('genero')),
    )
    client.set_password(password=data.get('senha'))
    client.set_cpf(cpf=data.get('cpf'))
    
    print(client.toMap())
    
    db.session.add(client)
    db.session.commit()
    return {
        'message': 'Client criado com sucesso',
        'data': client.toMap()
    }, 201
