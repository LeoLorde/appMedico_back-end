from flask import request, jsonify
from models.client_model import Client
from models.gender_enum import Gender
from datetime import datetime
from database import db
from classes import CPF, Email

def create_client():
    data = request.get_json()
    id = data.get("id")
    username = data.get('username')
    email = data.get('email')
    cpf = data.get('cpf')
    data_nascimento = data.get('dataDeNascimento')
    genero = data.get('genero')
    senha = data.get('senha')

    # ----- VALIDATORS -----
    if not Email.is_valid(email):
        return jsonify({'message': 'Email inválido'}), 400

    if not CPF.validator(cpf):
        return jsonify({'message': 'CPF inválido'}), 400

    # ----- CREATE CLIENT -----
    client = Client(
        username=username,
        email=Email.parse(email),
        dataDeNascimento=datetime.strptime(data_nascimento, '%Y-%m-%d').date(),
        gender=Gender.parse_gender(genero),
    )
    client.set_password(password=senha)
    client.set_cpf(cpf=CPF.parse_cpf(cpf))

    db.session.add(client)
    db.session.commit()

    return jsonify({
        'message': 'Client criado com sucesso',
        'data': client.toMap()
    }), 201
