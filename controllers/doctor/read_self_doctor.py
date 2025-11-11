from database import db
from models.doctor_model import Doctor
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

@jwt_required()
def self_client():
    print("getting id")
    id = get_jwt_identity()
    print("id gotten")
    doctor : Doctor = Doctor.query.get(id)
    print(doctor.toMap())
    return jsonify({
        "user": doctor.toMap()
    })