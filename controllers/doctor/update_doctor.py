from flask_jwt_extended import jwt_required
from models.doctor_model import Doctor
from database import db
from flask import request, jsonify

@jwt_required()
def update_doctor(id):
    data = request.get_json()
    
    doctor: Doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({
            'message': 'Doutor não encontrado'
        }), 404

    if 'username' in data:
        doctor.username = data['username']
    if 'email' in data:
        doctor.email = data['email']
    if 'password' in data:
        doctor.set_password(data['password'])
    if 'cpf' in data:
        doctor.set_cpf(data['cpf']) 
    if 'dataDeNascimento' in data:
        doctor.dataDeNascimento = data['dataDeNascimento']
    if 'gender' in data:
        doctor.gender = data['gender']

    db.session.commit()
    return jsonify({
        'message': 'Doutor atualizado com sucesso',
        'data': doctor.toMap()
    }), 200
