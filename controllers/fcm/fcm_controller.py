from flask import request, jsonify
from flask_jwt_extended import jwt_required
from database import db
from models.fcm_token_model import FcmToken

@jwt_required()
def save_fcm_token():
    try:
        data = request.get_json()
        fcm_token = data.get('fcm_token')
        device_info = data.get('device_info')
        
        user_id = request.user['id']
        user_type = request.user['type']  # 'client' ou 'doctor'
        
        if not fcm_token:
            return jsonify({'error': 'fcm_token é obrigatório'}), 400
        
        existing_token = FcmToken.query.filter_by(
            user_id=user_id,
            user_type=user_type
        ).first()
        
        if existing_token:
            existing_token.fcm_token = fcm_token
            existing_token.device_info = device_info
        else:
            new_token = FcmToken(
                user_id=user_id,
                user_type=user_type,
                fcm_token=fcm_token,
                device_info=device_info
            )
            db.session.add(new_token)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Token FCM salvo com sucesso',
            'success': True
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro ao salvar token FCM'}), 500

@jwt_required()
def delete_fcm_token():
    try:
        user_id = request.user['id']
        user_type = request.user['type']
        
        FcmToken.query.filter_by(
            user_id=user_id,
            user_type=user_type
        ).delete()
        
        db.session.commit()
        
        return jsonify({'message': 'Token removido com sucesso'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro ao remover token'}), 500
