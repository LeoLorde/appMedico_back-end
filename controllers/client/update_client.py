from flask_jwt_extended import jwt_required, get_jwt_identity
from models.client_model import Client
from database import db
from flask import request, jsonify
from utils.validators import InputValidator, ValidationError

def update_client(id):
    try:
        current_user = get_jwt_identity()
        if current_user.get('type') != 'client' or current_user.get('id') != id:
            return jsonify({'message': 'Acesso negado. Você só pode atualizar seu próprio perfil'}), 403
        
        data = request.get_json()
        
        client: Client = Client.query.get(id)
        if not client:
            return jsonify({'message': 'Cliente não encontrado'}), 404

        try:
            validated_data = InputValidator.validate_client_data(data, is_update=True)
        except ValidationError as e:
            return jsonify({'message': 'Erro de validação', 'errors': e.errors}), 400

        if 'email' in validated_data and validated_data['email'] != client.email:
            existing = Client.query.filter_by(email=validated_data['email']).first()
            if existing:
                return jsonify({'message': 'Email já cadastrado'}), 409
            client.email = validated_data['email']
        
        if 'cpf' in validated_data and validated_data['cpf'] != client.cpf:
            existing = Client.query.filter_by(cpf=validated_data['cpf']).first()
            if existing:
                return jsonify({'message': 'CPF já cadastrado'}), 409
            client.set_cpf(validated_data['cpf'])

        if 'username' in validated_data:
            client.username = validated_data['username']
        if 'password' in validated_data:
            client.set_password(validated_data['password'])
        if 'dataDeNascimento' in data:
            client.dataDeNascimento = data['dataDeNascimento']
        if 'gender' in data:
            client.gender = data['gender']

        db.session.commit()
        
        response_data = client.toMap()
        response_data.pop('password', None)
        response_data.pop('password_hash', None)
        
        return jsonify({
            'message': 'Cliente atualizado com sucesso',
            'data': response_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao atualizar cliente', 'error': str(e)}), 500
