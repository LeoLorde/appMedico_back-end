from flask_jwt_extended import jwt_required
from models.doctor_model import Doctor
from database import db
from flask import jsonify

@jwt_required()
def delete_doctor(id):
    doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({
            'message': 'Doutor não encontrado'
        }), 404
    db.session.delete(doctor)
    db.session.commit()
    return jsonify({
        'message': 'Doutor deletado com sucesso'
    }), 200