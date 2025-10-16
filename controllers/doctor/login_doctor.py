from flask import request, jsonify
from models.doctor_model import Doctor
from flask_jwt_extended import create_access_token
from datetime import timedelta

def doctor_login():
    data = request.get_json()
    email=data.get('email')
    password = data.get('senha')

    doctor_exist : Doctor = Doctor.query.filter_by(email=email).first()
    if doctor_exist == None:
        return jsonify({
            "message":f"Usuário com email '{email}' não encontrado"
        })
    if doctor_exist.check_password(password) == False:
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