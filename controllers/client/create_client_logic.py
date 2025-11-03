from flask import request, jsonify
from models.client_model import Client
from models.gender_enum import Gender
from datetime import datetime
from database import db
from utils.validators import InputValidator, ValidationError

def _create_client_model(validated_data, parsed_date, genero) -> Client:
    client = Client(
            username=validated_data['username'],
            email=validated_data['email'],
            dataDeNascimento=parsed_date,
            gender=Gender.parse_gender(genero),
        )
    client.set_password(password=validated_data['password'])
    client.set_cpf(cpf=validated_data['cpf'])

def _try_parse_data(data) -> datetime.strptime:
    try:
        parsed_date = datetime.strptime(data, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return jsonify({'message': 'Data de nascimento inválida. Use formato YYYY-MM-DD'}), 400

def _existing_user_by_cpf_or_email(validated_data):
    existing_email = Client.query.filter_by(email=validated_data['email']).first()
    if existing_email:
        return jsonify({'message': 'Email já cadastrado'}), 409
    
    existing_cpf = Client.query.filter_by(cpf=validated_data['cpf']).first()
    if existing_cpf:
        return jsonify({'message': 'CPF já cadastrado'}), 409

def get_non_sensible_data(client: Client) -> dict:
    response_data = client.toMap()
    response_data.pop('password', None)
    response_data.pop('password_hash', None)
    return response_data

def validate_client_data(data: dict) -> Client:
    validated_data = InputValidator.validate_client_data({
        'username': data.get('username'),
        'email': data.get('email'),
        'cpf': data.get('cpf'),
        'password': data.get('senha')
    })
    
    data_nascimento = data.get('dataDeNascimento')
    genero = data.get('genero')
    
    parsed_date = _try_parse_data(data_nascimento)
    client = _create_client_model(validated_data, parsed_date, genero)
    _existing_user_by_cpf_or_email(validated_data)
    return client