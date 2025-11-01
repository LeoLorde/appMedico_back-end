import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("doctorhub-1f3c2-firebase-adminsdk-fbsvc-1d210b52b8.json")
firebase_admin.initialize_app(cred)

def send_fcm_notification(token, title, body, data=None):
    """Envia uma notificação via Firebase Cloud Messaging"""
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=token,
        data=data or {}
    )
    response = messaging.send(message)
    print("Notificação enviada:", response)
