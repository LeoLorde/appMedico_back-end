from flask import request, jsonify
from models.client_model import Client
from flask_jwt_extended import create_access_token
from datetime import timedelta

def client_login():
    data = request.get_json()
    email=data.get('email')
    password = data.get('senha')

    client_exist : Client = Client.query.filter_by(email=email).first()
    if client_exist == None:
        return jsonify({
            "message":f"Usuário com email '{email}' não encontrado"
        })
    if client_exist.check_password(password) == False:
        return jsonify({
            "message":f"Senha incorreta"
        })
    
    access_token = create_access_token(
        identity=email,
        expires_delta=timedelta(hours=1)
    )
    return jsonify({
        'access_token': access_token
    }), 200