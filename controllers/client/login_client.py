from flask import request, jsonify
from models.client_model import Client
from flask_jwt_extended import create_access_token
from datetime import timedelta

def client_login():
    data = request.get_json()
    print(f"[DEBUG] Login attempt - Data received: {data}")
    
    email=data.get('email')
    password = data.get('senha')
    
    print(f"[DEBUG] Email: {email}")
    print(f"[DEBUG] Password received: {'Yes' if password else 'No'}")

    client_exist : Client = Client.query.filter_by(email=email).first()
    
    print(f"[DEBUG] Client found: {client_exist is not None}")
    
    if client_exist == None:
        print(f"[DEBUG] Client not found with email: {email}")
        return jsonify({
            "message":f"Usuário com email '{email}' não encontrado"
        }), 401
        
    print(f"[DEBUG] Checking password...")
    password_valid = client_exist.check_password(password)
    print(f"[DEBUG] Password valid: {password_valid}")
    
    if password_valid == False:
        print(f"[DEBUG] Invalid password for email: {email}")
        return jsonify({
            "message":f"Senha incorreta"
        }), 401
    
    print(f"[DEBUG] Login successful for: {email}")
    access_token = create_access_token(
        identity=email,
        expires_delta=timedelta(hours=1)
    )
    return jsonify({
        'access_token': access_token
    }), 200
