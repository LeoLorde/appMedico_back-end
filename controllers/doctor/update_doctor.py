from flask_jwt_extended import jwt_required, get_jwt_identity
from models.doctor_model import Doctor
from database import db
from flask import request, jsonify
from utils.validators import InputValidator, ValidationError

@jwt_required()
def update_doctor(id):
    try:
        current_user = get_jwt_identity()
        if current_user.get('type') != 'doctor' or current_user.get('id') != id:
            return jsonify({'message': 'Acesso negado. Você só pode atualizar seu próprio perfil'}), 403
        
        data = request.get_json()
        
        doctor: Doctor = Doctor.query.get(id)
        if not doctor:
            return jsonify({'message': 'Médico não encontrado'}), 404

        try:
            validated_data = InputValidator.validate_doctor_data(data, is_update=True)
        except ValidationError as e:
            return jsonify({'message': 'Erro de validação', 'errors': e.errors}), 400

        if 'email' in validated_data and validated_data['email'] != doctor.email:
            existing = Doctor.query.filter_by(email=validated_data['email']).first()
            if existing:
                return jsonify({'message': 'Email já cadastrado'}), 409
            doctor.email = validated_data['email']
        
        if 'crm' in validated_data and validated_data['crm'] != doctor.crm:
            existing = Doctor.query.filter_by(crm=validated_data['crm']).first()
            if existing:
                return jsonify({'message': 'CRM já cadastrado'}), 409
            doctor.set_crm(validated_data['crm'])

        if 'username' in validated_data:
            doctor.username = validated_data['username']
        if 'password' in validated_data:
            doctor.set_password(validated_data['password'])
        if 'specialty' in validated_data:
            doctor.especialidade = validated_data['specialty']
        if 'bio' in data:
            doctor.bio = data['bio']

        db.session.commit()
        
        response_data = doctor.toMap()
        response_data.pop('password', None)
        response_data.pop('password_hash', None)
        
        return jsonify({
            'message': 'Médico atualizado com sucesso',
            'data': response_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao atualizar médico', 'error': str(e)}), 500
