from flask import jsonify
from models.client_model import Client
from flask_jwt_extended import create_access_token
from datetime import timedelta

def _get_client_by_email(data):
    email = data.get('email')
    password = data.get('senha')
    print(f"0.1.1/2 - Try get Client with email: {email}")
    if not email or not password:
        return jsonify({'message': 'Email e senha são obrigatórios'}), 400
    client_exist: Client = Client.query.filter_by(email=email).first()
    if not client_exist:
        print("RAISE ERROR: CLIENT WAS NOT FOUND")
        raise Exception("Error: Client Not Found")
    print(f"0.1.2/2 - Client found with email {client_exist.username}")
    return client_exist, password

def _check_client_password(password, client : Client) -> bool:
    print("0.2.1/2 - Try check client password")
    if not client:
        print("Client Not Found - INVALID EXCEPTION")
        return
    else:
        print(client.toMap())
    print("0.2.2/2 - Client Exist, try Check Password")
    print(f"0.2.3/2 - Client Name is {client.username}")
    print("---")
    password_valid = client.check_password(password)
    print(f"Password has been checked. Result: {password_valid}")
    if not password_valid:
        print("Deu Merda")
        return False
    return True

def get_user_with_request(request):
    print("0.1/2 - Getting Client with Email")
    client, password = _get_client_by_email(request)
    print("0.2/2 - Checking Client Password")
    if _check_client_password(password, client):
        print("0.4/2 - Client Worked")
        return client
    print("0.3/2 - Client Password is Wrong")
    return None

def create_jwt_token(client: Client):
    return create_access_token(
            identity=str(client.id), 
            additional_claims={
                "email": client.email,
                "type": "client"
            },
            expires_delta=timedelta(hours=1)
    )
    
def create_return_message(client : Client, token):
    return jsonify({
            'access_token': token,
            'user': {
                'id': client.id,
                'username': client.username,
                'email': client.email
            }
    }), 200