from database import db
from models.appointment_model import Appointment
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from models.fcm_token_model import FcmToken
from models.client_model import Client
from utils.send_message import send_message

@jwt_required()
def refused_appointment():
    try:
        data = request.get_json()
        
        id = data.get("app_id")

        appoint : Appointment = Appointment.query.filter_by(id=id).first()
        appoint.is_confirmed = "refused"
        
        db.session.add(appoint)
        db.session.commit()
        
        token : FcmToken = FcmToken.query.filter_by(user_id=appoint.client_id).first()
        print(token)
        send_message(token.fcm_token, "Sua consulta foi recusada", "Consulta Recusada")
        
        
        return jsonify({
            "message": appoint.toMap()
        }), 200
    except:
        pass