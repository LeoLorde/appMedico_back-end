from models.doctor_model import Doctor
from flask import request, jsonify
from database import db
from classes import Email, CRM

def create_doctor():
    data = request.get_json()

    id = data.get("id")
    username = data.get('username')
    email = data.get('email')
    crm = data.get('crm')
    bio = data.get('bio')
    especialidade = data.get('especialidade')
    senha = data.get('senha')
    endereco_id=data.get('endereco_id')

    # ----- VALIDATORS -----
    if not Email.is_valid(email):
        return jsonify({'message': 'Email inválido'}), 400

    if not CRM.is_valid(crm):
        return jsonify({'message': 'CRM inválido'}), 400

    # ----- CREATE DOCTOR -----
    doctor = Doctor(
        username=username,
        email=Email.parse(email),
        bio=bio,
        especialidade=especialidade,
        endereco_id=endereco_id
    )
    doctor.set_crm(crm=CRM.parse(crm))
    doctor.set_password(password=senha)

    db.session.add(doctor)
    db.session.commit()

    return jsonify({
        'message': 'Doctor criado com sucesso',
        'data': doctor.toMap()
    }), 201
