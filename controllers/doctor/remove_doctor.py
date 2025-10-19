from flask_jwt_extended import jwt_required, get_jwt_identity
from models.doctor_model import Doctor
from database import db
from flask import jsonify

@jwt_required()
def delete_doctor(id):
    try:
        current_user = get_jwt_identity()
        if current_user.get('type') != 'doctor' or current_user.get('id') != id:
            return jsonify({'message': 'Acesso negado. Você só pode deletar seu próprio perfil'}), 403
        
        doctor = Doctor.query.get(id)
        if not doctor:
            return jsonify({'message': 'Médico não encontrado'}), 404
            
        db.session.delete(doctor)
        db.session.commit()
        
        return jsonify({'message': 'Médico deletado com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao deletar médico', 'error': str(e)}), 500
