from flask import request, jsonify
from models.client_model import Client
from models.gender_enum import Gender
from datetime import datetime
from database import db
from utils.validators import InputValidator, ValidationError

def create_client():
    try:
        data = request.get_json()
        
        validated_data = InputValidator.validate_client_data({
            'username': data.get('username'),
            'email': data.get('email'),
            'cpf': data.get('cpf'),
            'password': data.get('senha')
        })
        
        data_nascimento = data.get('dataDeNascimento')
        genero = data.get('genero')
        
        try:
            parsed_date = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return jsonify({'message': 'Data de nascimento inválida. Use formato YYYY-MM-DD'}), 400

        existing_email = Client.query.filter_by(email=validated_data['email']).first()
        if existing_email:
            return jsonify({'message': 'Email já cadastrado'}), 409
        
        existing_cpf = Client.query.filter_by(cpf=validated_data['cpf']).first()
        if existing_cpf:
            return jsonify({'message': 'CPF já cadastrado'}), 409

        client = Client(
            username=validated_data['username'],
            email=validated_data['email'],
            dataDeNascimento=parsed_date,
            gender=Gender.parse_gender(genero),
        )
        client.set_password(password=validated_data['password'])
        client.set_cpf(cpf=validated_data['cpf'])

        db.session.add(client)
        db.session.commit()

        response_data = client.toMap()
        response_data.pop('password', None)
        response_data.pop('password_hash', None)

        return jsonify({
            'message': 'Client criado com sucesso',
            'data': response_data
        }), 201
        
    except ValidationError as e:
        return jsonify({'message': 'Erro de validação', 'errors': e.errors}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao criar cliente', 'error': str(e)}), 500
