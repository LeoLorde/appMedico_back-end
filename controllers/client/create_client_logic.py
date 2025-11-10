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
    return client

def _try_parse_data(data) -> datetime:
    try:
        parsed_date = datetime.strptime(data, '%Y-%m-%d').date()
        return parsed_date
    except (ValueError, TypeError):
        raise ValidationError({'dataDeNascimento': 'Data de nascimento inválida. Use formato YYYY-MM-DD'})
    
def _existing_user_by_cpf_or_email(validated_data):
    print("0.1/4 - Verificando se o usuário já existe (email ou CPF)")
    existing_email = Client.query.filter_by(email=validated_data['email']).first()
    if existing_email:
        print("0.2/4 - Email já cadastrado:", validated_data['email'])
        return jsonify({'message': 'Email já cadastrado'}), 409
    
    existing_cpf = Client.query.filter_by(cpf=validated_data['cpf']).first()
    if existing_cpf:
        print("0.2/4 - CPF já cadastrado:", validated_data['cpf'])
        return jsonify({'message': 'CPF já cadastrado'}), 409
    print("0.3/4 - Nenhum usuário encontrado com esse email ou CPF")
    return None

def get_non_sensible_data(client: Client) -> dict:
    print("0.1/4 - Extraindo dados não sensíveis do cliente")
    response_data = client.toMap()
    response_data.pop('password', None)
    response_data.pop('password_hash', None)
    print("0.2/4 - Dados não sensíveis extraídos:", response_data)
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
    if isinstance(parsed_date, tuple):
        return parsed_date
    
    existing_check = _existing_user_by_cpf_or_email(validated_data)
    if existing_check:
        return existing_check
    
    client = _create_client_model(validated_data, parsed_date, genero)
    
    print("3/4 - Validação de dados do cliente finalizada. Cliente criado:", client)
    return client
