from models.doctor_model import Doctor
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from utils.validators import InputValidator

def search_all(limit: int):
    try:
        max_limit = min(limit, 100)
        doctor_list: list[Doctor] = Doctor.query.limit(max_limit).all()

        if not doctor_list:
            return jsonify({"message": "Nenhum médico encontrado"}), 404
        
        return jsonify([
            InputValidator.sanitize_output(doctor.toMap())
            for doctor in doctor_list
        ]), 200
        
    except Exception as e:
        return jsonify({'message': 'Erro ao buscar médicos', 'error': str(e)}), 500

def search_by_id(id: int):
    try:
        current_user = get_jwt_identity()
        if current_user.get('type') == 'doctor' and current_user.get('id') != id:
            return jsonify({'message': 'Acesso negado'}), 403
        
        doctor: Doctor = Doctor.query.filter_by(id=id).first()
        if not doctor:
            return jsonify({"message": "Nenhum médico encontrado"}), 404
        
        return jsonify(InputValidator.sanitize_output(doctor.toMap())), 200
        
    except Exception as e:
        return jsonify({'message': 'Erro ao buscar médico', 'error': str(e)}), 500

def search_by_username(username: str, limit: int):
    try:
        if not username or len(username) < 2:
            return jsonify({"message": "Username inválido"}), 400
        
        max_limit = min(limit, 100)

        doctor_list: list[Doctor] = (
            Doctor.query
            .filter(Doctor.username.ilike(f"%{username}%"))
            .limit(max_limit)
            .all()
        )

        if not doctor_list:
            return jsonify({"message": "Nenhum médico encontrado"}), 404
        
        return jsonify([
            InputValidator.sanitize_output(doctor.toMap())
            for doctor in doctor_list
        ]), 200

    except Exception as e:
        return jsonify({'message': 'Erro ao buscar médicos', 'error': str(e)}), 500