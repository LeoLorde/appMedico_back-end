from database import db
from models.fcm_token_model import FcmToken
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

@jwt_required()
def create_fcm_token():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        fcm_token = data.get('fcm_token')
        device_info = data.get('device_info', '')

        if not fcm_token:
            return jsonify({'message': 'Token FCM é obrigatório'}), 400

        existing = FcmToken.query.filter_by(user_id=user_id).first()

        if existing:
            existing.fcm_token = fcm_token
            existing.device_info = device_info
            existing.updated_at = datetime.utcnow()
        else:
            new_token = FcmToken(
                user_id=user_id,
                fcm_token=fcm_token,
                device_info=device_info,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(new_token)

        db.session.commit()
        return jsonify({'message': 'FCM Token registrado com sucesso'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao registrar token', 'error': str(e)}), 500
