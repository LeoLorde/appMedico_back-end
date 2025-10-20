from flask_jwt_extended import get_jwt_identity
from flask import jsonify, request
from models.expedient_model import Expediente
from utils.validators import InputValidator

def search_by_id(id: int):
    try:
        doctor: Expediente = Expediente.query.filter_by(id=id).first()
        if not doctor:
            return jsonify({"message": "Nenhum expediente encontrado"}), 404
        
        return jsonify(InputValidator.sanitize_output(doctor.toMap())), 200
        
    except Exception as e:
        return jsonify({'message': 'Erro ao buscar expediente', 'error': str(e)}), 500
