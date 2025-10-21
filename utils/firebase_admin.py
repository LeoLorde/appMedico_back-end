import firebase_admin
from firebase_admin import credentials, messaging
import os

# Inicializar Firebase Admin (fazer isso apenas uma vez)
if not firebase_admin._apps:
    cred_path = os.getenv('FIREBASE_ADMIN_SDK_PATH', './firebase-adminsdk.json')
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

def send_push_notification(fcm_token: str, title: str, body: str, data: dict = None) -> dict:
    """
    Envia notificação push para um usuário
    
    Args:
        fcm_token: Token FCM do dispositivo
        title: Título da notificação
        body: Corpo da notificação
        data: Dados extras (appointmentId, type, etc)
    
    Returns:
        dict: {'success': bool, 'message_id': str} ou {'success': bool, 'error': str}
    """
    try:
        if data is None:
            data = {}
        
        # Converter todos os valores para string (Firebase exige)
        data_strings = {k: str(v) for k, v in data.items()}
        data_strings['click_action'] = 'FLUTTER_NOTIFICATION_CLICK'
        
        # Criar mensagem
        message = messaging.Message(
            token=fcm_token,
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            data=data_strings,
            android=messaging.AndroidConfig(
                priority='high',
                notification=messaging.AndroidNotification(
                    sound='default',
                    channel_id='appointments'
                )
            ),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        sound='default',
                        badge=1
                    )
                )
            )
        )
        
        # Enviar mensagem
        response = messaging.send(message)
        print(f'[v0] Notificação enviada com sucesso: {response}')
        
        return {'success': True, 'message_id': response}
        
    except messaging.UnregisteredError:
        print(f'[v0] Token inválido ou não registrado: {fcm_token}')
        return {'success': False, 'error': 'invalid_token'}
        
    except Exception as e:
        print(f'[v0] Erro ao enviar notificação: {str(e)}')
        return {'success': False, 'error': str(e)}


def send_multicast_notification(fcm_tokens: list, title: str, body: str, data: dict = None) -> dict:
    """
    Envia notificação para múltiplos dispositivos
    
    Args:
        fcm_tokens: Lista de tokens FCM
        title: Título da notificação
        body: Corpo da notificação
        data: Dados extras
    
    Returns:
        dict: {'success': bool, 'success_count': int, 'failure_count': int}
    """
    try:
        if data is None:
            data = {}
        
        data_strings = {k: str(v) for k, v in data.items()}
        
        message = messaging.MulticastMessage(
            tokens=fcm_tokens,
            notification=messaging.Notification(title=title, body=body),
            data=data_strings,
            android=messaging.AndroidConfig(priority='high')
        )
        
        response = messaging.send_multicast(message)
        print(f'[v0] {response.success_count} notificações enviadas com sucesso')
        
        return {
            'success': True,
            'success_count': response.success_count,
            'failure_count': response.failure_count
        }
        
    except Exception as e:
        print(f'[v0] Erro ao enviar notificações: {str(e)}')
        return {'success': False, 'error': str(e)}