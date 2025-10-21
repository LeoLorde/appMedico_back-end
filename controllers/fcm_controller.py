from flask import request, jsonify
from sqlalchemy.orm import Session
from models.fcm_token import FcmToken
from database import get_db  # Sua função para obter sessão do DB

def save_fcm_token():
    """
    Salva ou atualiza o token FCM do usuário
    POST /api/fcm-token
    """
    try:
        data = request.get_json()
        fcm_token = data.get('fcm_token')
        device_info = data.get('device_info')
        
        # Dados do usuário vêm do middleware de autenticação JWT
        user_id = request.user['id']
        user_type = request.user['type']  # 'client' ou 'doctor'
        
        if not fcm_token:
            return jsonify({'error': 'fcm_token é obrigatório'}), 400
        
        db: Session = get_db()
        
        # Verificar se já existe um token para este usuário
        existing_token = db.query(FcmToken).filter_by(
            user_id=user_id,
            user_type=user_type
        ).first()
        
        if existing_token:
            # Atualizar token existente
            existing_token.fcm_token = fcm_token
            existing_token.device_info = device_info
        else:
            # Inserir novo token
            new_token = FcmToken(
                user_id=user_id,
                user_type=user_type,
                fcm_token=fcm_token,
                device_info=device_info
            )
            db.add(new_token)
        
        db.commit()
        print(f'[v0] Token FCM salvo para {user_type} {user_id}')
        
        return jsonify({
            'message': 'Token FCM salvo com sucesso',
            'success': True
        }), 200
        
    except Exception as e:
        print(f'[v0] Erro ao salvar token FCM: {str(e)}')
        return jsonify({'error': 'Erro ao salvar token FCM'}), 500


def delete_fcm_token():
    """
    Remove o token FCM (quando usuário faz logout)
    DELETE /api/fcm-token
    """
    try:
        user_id = request.user['id']
        user_type = request.user['type']
        
        db: Session = get_db()
        
        db.query(FcmToken).filter_by(
            user_id=user_id,
            user_type=user_type
        ).delete()
        
        db.commit()
        
        return jsonify({'message': 'Token removido com sucesso'}), 200
        
    except Exception as e:
        print(f'[v0] Erro ao remover token: {str(e)}')
        return jsonify({'error': 'Erro ao remover token'}), 500