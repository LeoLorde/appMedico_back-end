from flask import request, jsonify
from sqlalchemy.orm import Session
from models.notification_model import Notification
from models.fcm_token_model import FcmToken
from utils.firebase_admin import send_push_notification
from database import get_db
import math

def get_notifications():
    """
    Busca notificações do usuário
    GET /api/notifications?page=1&limit=20
    """
    try:
        user_id = request.user['id']
        user_type = request.user['type']
        
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        offset = (page - 1) * limit
        
        db: Session = get_db()
        
        # Buscar notificações
        notifications = db.query(Notification).filter_by(
            user_id=user_id,
            user_type=user_type
        ).order_by(Notification.created_at.desc()).limit(limit).offset(offset).all()
        
        # Contar total
        total = db.query(Notification).filter_by(
            user_id=user_id,
            user_type=user_type
        ).count()
        
        return jsonify({
            'notifications': [n.to_dict() for n in notifications],
            'total': total,
            'page': page,
            'totalPages': math.ceil(total / limit)
        }), 200
        
    except Exception as e:
        print(f'[v0] Erro ao buscar notificações: {str(e)}')
        return jsonify({'error': 'Erro ao buscar notificações'}), 500


def mark_as_read(notification_id):
    """
    Marca notificação como lida
    PUT /api/notifications/<id>/read
    """
    try:
        user_id = request.user['id']
        user_type = request.user['type']
        
        db: Session = get_db()
        
        notification = db.query(Notification).filter_by(
            id=notification_id,
            user_id=user_id,
            user_type=user_type
        ).first()
        
        if not notification:
            return jsonify({'error': 'Notificação não encontrada'}), 404
        
        notification.read = True
        db.commit()
        
        return jsonify({'message': 'Notificação marcada como lida'}), 200
        
    except Exception as e:
        print(f'[v0] Erro ao marcar notificação: {str(e)}')
        return jsonify({'error': 'Erro ao marcar notificação'}), 500


def send_notification_to_user(user_id: int, user_type: str, title: str, body: str, 
                              notification_type: str, data: dict = None) -> dict:
    """
    Envia notificação para um usuário específico
    (Função auxiliar usada por outros controllers)
    
    Args:
        user_id: ID do usuário
        user_type: 'client' ou 'doctor'
        title: Título da notificação
        body: Corpo da notificação
        notification_type: Tipo da notificação (ex: 'appointment_confirmed')
        data: Dados extras (appointmentId, doctorId, etc)
    
    Returns:
        dict: {'success': bool, 'sent': bool, 'reason': str}
    """
    try:
        if data is None:
            data = {}
        
        db: Session = get_db()
        
        # 1. Salvar notificação no banco
        notification = Notification(
            user_id=user_id,
            user_type=user_type,
            title=title,
            body=body,
            type=notification_type,
            data=data
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        
        notification_id = notification.id
        
        # 2. Buscar token FCM do usuário
        fcm_token_obj = db.query(FcmToken).filter_by(
            user_id=user_id,
            user_type=user_type
        ).first()
        
        if not fcm_token_obj:
            print(f'[v0] Usuário {user_type} {user_id} não tem token FCM registrado')
            return {'success': True, 'sent': False, 'reason': 'no_token'}
        
        fcm_token = fcm_token_obj.fcm_token
        
        # 3. Enviar notificação push
        data_with_id = data.copy()
        data_with_id['type'] = notification_type
        data_with_id['notificationId'] = notification_id
        
        result = send_push_notification(fcm_token, title, body, data_with_id)
        
        # 4. Se o token for inválido, remover do banco
        if not result['success'] and result.get('error') == 'invalid_token':
            db.query(FcmToken).filter_by(
                user_id=user_id,
                user_type=user_type
            ).delete()
            db.commit()
            print(f'[v0] Token inválido removido para {user_type} {user_id}')
        
        return result
        
    except Exception as e:
        print(f'[v0] Erro ao enviar notificação: {str(e)}')
        return {'success': False, 'error': str(e)}