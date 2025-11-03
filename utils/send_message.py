def send_message(token, message, title):
    import firebase_admin
    from firebase_admin import messaging

    if not firebase_admin._apps:
        from firebase_admin import credentials
        cred = credentials.Certificate("doctorhub-1f3c2-firebase-adminsdk-fbsvc-1d210b52b8.json")
        firebase_admin.initialize_app(cred)

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=message,
        ),
        token=token,
    )

    response = messaging.send(message)
    print("✅ Notificação enviada com sucesso! ID:", response)
