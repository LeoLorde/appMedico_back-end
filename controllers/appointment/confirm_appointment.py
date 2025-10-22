from database import db
from models.appointment_model import Appointment
from flask import request, jsonify
from flask_jwt_extended import jwt_required

@jwt_required()
def confirm_appointment():
    try:
        data = request.get_json()
        
        id = data.get("app_id")

        appoint : Appointment = Appointment.query.filter_by(id=id).first()
        appoint.is_confirmed = "confirmed"
        
        db.session.add(appoint)
        db.session.commit()
        
        return jsonify({
            "message": appoint.toMap()
        }), 200
    except:
        pass