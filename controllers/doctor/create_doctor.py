from models.doctor_model import Doctor
from flask import request, jsonify
from database import db
from utils.validators import InputValidator, ValidationError

def create_doctor():
    try:
        data = request.get_json()

        validated_data = InputValidator.validate_doctor_data({
            'username': data.get('username'),
            'email': data.get('email'),
            'crm': data.get('crm'),
            'password': data.get('senha'),
            'specialty': data.get('especialidade')
        })

        bio = data.get('bio', '')
        endereco_id = data.get('endereco_id')

        existing_email = Doctor.query.filter_by(email=validated_data['email']).first()
        if existing_email:
            return jsonify({'message': 'Email já cadastrado'}), 409
        
        existing_crm = Doctor.query.filter_by(crm=validated_data['crm']).first()
        if existing_crm:
            return jsonify({'message': 'CRM já cadastrado'}), 409

        doctor = Doctor(
            username=validated_data['username'],
            email=validated_data['email'],
            bio=bio,
            especialidade=validated_data.get('specialty', ''),
            endereco_id=endereco_id
        )
        doctor.set_crm(crm=validated_data['crm'])
        doctor.set_password(password=validated_data['password'])

        db.session.add(doctor)
        db.session.commit()

        response_data = doctor.toMap()
        response_data.pop('password', None)
        response_data.pop('password_hash', None)

        return jsonify({
            'message': 'Doctor criado com sucesso',
            'data': response_data
        }), 201
        
    except ValidationError as e:
        return jsonify({'message': 'Erro de validação', 'errors': e.errors}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao criar médico', 'error': str(e)}), 500
