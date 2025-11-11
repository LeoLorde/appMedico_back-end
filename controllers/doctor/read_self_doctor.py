from database import db
from models.doctor_model import Doctor
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

@jwt_required()
def self_client():
    id = get_jwt_identity()
    doctor : Doctor = Doctor.query.get(id)
    return jsonify({
        "user": doctor.toMap()
    })