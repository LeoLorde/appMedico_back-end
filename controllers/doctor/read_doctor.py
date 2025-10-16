from models.doctor_model import Doctor
from flask import request, jsonify

def search_all(limit: int):
    doctor_list : list[Doctor] = Doctor.query.limit(limit).all()

    if not doctor_list:
        return {"message": "Nenhum Doctore encontrado"}
    
    return jsonify([
        doctor.toMap()
        for doctor in doctor_list
    ])

def search_by_id(id: int):
    doctor : Doctor = Doctor.query.filter_by(id=id).first()
    if not doctor:
        return {"message": "Nenhum Doctore encontrado"}, 404
    
    return jsonify(
        doctor.toMap()
    ), 200
    
def search_by_username(username: str, limit: int):
    doctor_list : Doctor = Doctor.query.filter_by(username=username).limit(limit).all()
    if not doctor_list:
        return {"message": "Nenhum Doctore encontrado"}, 400
    
    return jsonify([
        doctor.toMap()
        for doctor in doctor_list
    ])