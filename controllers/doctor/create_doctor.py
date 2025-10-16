from models.doctor_model import Doctor
from flask import request, jsonify
from database import db

def create_doctor():
    data = request.get_json()
    doctor : Doctor = Doctor(
        username=data.get('username'),
        email=data.get('email'),
        bio=data.get('bio'),
        especialidade=data.get('especialidade'),
        endereco_id=1
    )
    doctor.set_crm(crm=data.get('crm'))
    doctor.set_password(password=data.get('senha'))
    
    db.session.add(doctor)
    db.session.commit()
    return jsonify({
        'message': 'Doctor criado com sucesso',
        'data': doctor.toMap()
    }), 201