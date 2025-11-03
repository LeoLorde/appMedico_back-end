from database import db
from models.appointment_model import Appointment
from utils.send_message import send_message
from models.fcm_token_model import FcmToken
from flask import request, jsonify
from flask_jwt_extended import jwt_required

@jwt_required()
def confirm_appointment():
    try:
        data = request.get_json()
        
        id = data.get("app_id")

        appoint : Appointment = Appointment.query.filter_by(id=id).first()
        appoint.is_confirmed = "confirmed"
  
        token : FcmToken = FcmToken.query.filter_by(user_id=appoint.client_id).first()
        print(token)
        send_message(token.fcm_token, "Sua consulta foi confirmada", "Consulta Confirmada")

        db.session.add(appoint)
        db.session.commit()
        
        return jsonify({
            "message": appoint.toMap()
        }), 200
    except:
        pass