from flask import request, jsonify
from models.client_model import Client
from flask_jwt_extended import create_access_token
from datetime import timedelta

def client_login():
    try:
        data = request.get_json()
        
        email = data.get('email')
        password = data.get('senha')
        
        if not email or not password:
            return jsonify({'message': 'Email e senha são obrigatórios'}), 400

        client_exist: Client = Client.query.filter_by(email=email).first()
        
        if client_exist is None:
            return jsonify({'message': 'Credenciais inválidas'}), 401
        
        password_valid = client_exist.check_password(password)
        
        if not password_valid:
            return jsonify({'message': 'Credenciais inválidas'}), 401
        
        access_token = create_access_token(
            identity={'email': email, 'id': client_exist.id, 'type': 'client'},
            expires_delta=timedelta(hours=1)
        )
        
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': client_exist.id,
                'username': client_exist.username,
                'email': client_exist.email
            }
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Erro ao fazer login', 'error': str(e)}), 500
