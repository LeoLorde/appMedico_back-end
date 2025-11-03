from flask import request, jsonify
from models.doctor_model import Doctor
from flask_jwt_extended import create_access_token
from datetime import timedelta

def doctor_login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('senha')
        
        if not email or not password:
            return jsonify({'message': 'Email e senha são obrigatórios'}), 400

        print("CHEGOU AQUI")
        doctor_exist: Doctor = Doctor.query.filter_by(email=email).first()
        print("CHEGOU AQUI 2")
        if doctor_exist is None:
            print("CHEGOU AQUI 3")
            return jsonify({'message': 'Credenciais inválidas'}), 401
        
        if not doctor_exist.check_password(password):
            return jsonify({'message': 'Credenciais inválidas'}), 401
        print("CHEGOU AQUI 4")
        access_token = create_access_token(
            identity=str(doctor_exist.id), 
            additional_claims={
                "email": email,
                "type": "doctor"
            },
            expires_delta=timedelta(hours=1)
        )
        response = jsonify({
            'access_token': access_token,
            'user': {
                'id': doctor_exist.id,
                'username': doctor_exist.username,
                'email': doctor_exist.email,
                'crm': doctor_exist.crm,
                'especialidade': doctor_exist.especialidade
            }
        })
        print(response)
        return response, 200
        
    except Exception as e:
        return jsonify({'message': 'Erro ao fazer login', 'error': str(e)}), 500
