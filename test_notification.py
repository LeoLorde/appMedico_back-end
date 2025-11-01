import firebase_admin
from firebase_admin import messaging

# já inicializado no app.py, mas se quiser rodar separado:
if not firebase_admin._apps:
    from firebase_admin import credentials
    cred = credentials.Certificate("doctorhub-1f3c2-firebase-adminsdk-fbsvc-1d210b52b8.json")
    firebase_admin.initialize_app(cred)

# 🔥 Coloca aqui o FCM Token do seu celular (aquele que aparece no app notification_test)
token = "c_G87o0kTzymOcbE4IpyZ-:APA91bETZyvxxWD5p5ndZNswF6XiYgGrUpTym6QcUfNaeVQyKAVVlI4XqPS3_Pa_rIObI2nM5nZCY1szO8a2aa82r54n-S6s7MHO6MldLCCte48VeukAsMg"

# Cria a notificação
message = messaging.Message(
    notification=messaging.Notification(
        title="Nova solicitação de consulta 🩺",
        body="Um paciente solicitou uma nova consulta!",
    ),
    token=token,
)

# Envia
response = messaging.send(message)
print("✅ Notificação enviada com sucesso! ID:", response)
