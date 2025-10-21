from flask import request, jsonify
from models.notification_model import Notification
from models.fcm_token_model import FcmToken
from utils.firebase_admin import send_push_notification
from database import db 
import math

def get_notifications():
    try:
        user_id = request.user['id']
        user_type = request.user['type']
        
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        offset = (page - 1) * limit

        notifications = (
            Notification.query
            .filter_by(user_id=user_id, user_type=user_type)
            .order_by(Notification.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        total = Notification.query.filter_by(
            user_id=user_id, user_type=user_type
        ).count()

        # Transforma em JSON (dict)
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
    try:
        user_id = request.user['id']
        user_type = request.user['type']

        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id,
            user_type=user_type
        ).first()

        if not notification:
            return jsonify({'error': 'Notificação não encontrada'}), 404

        notification.read = True
        db.session.commit()

        return jsonify({'message': 'Notificação marcada como lida'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao marcar notificação'}), 500


def send_notification_to_user(user_id: int, user_type: str, title: str, body: str, 
                              notification_type: str, data: dict = None) -> dict:
    """
    Envia notificação para um usuário específico
    """
    try:
        if data is None:
            data = {}

        notification = Notification(
            user_id=user_id,
            user_type=user_type,
            title=title,
            body=body,
            type=notification_type,
            data=data
        )
        db.session.add(notification)
        db.session.commit()
        db.session.refresh(notification)

        notification_id = notification.id

        fcm_token_obj = FcmToken.query.filter_by(
            user_id=user_id,
            user_type=user_type
        ).first()

        if not fcm_token_obj:
            print(f'[v0] Usuário {user_type} {user_id} não tem token FCM registrado')
            return {'success': True, 'sent': False, 'reason': 'no_token'}

        fcm_token = fcm_token_obj.fcm_token
        data_with_id = data.copy()
        data_with_id['type'] = notification_type
        data_with_id['notificationId'] = notification_id

        result = send_push_notification(fcm_token, title, body, data_with_id)

        # DEVE REMOVER O FCM TOKEN SE FOR INVÁLIDO
        if not result['success'] and result.get('error') == 'invalid_token':
            FcmToken.query.filter_by(
                user_id=user_id,
                user_type=user_type
            ).delete()
            db.session.commit()
            
        return result

    except Exception as e:
        db.session.rollback()
        return {'success': False, 'error': str(e)}
