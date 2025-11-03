from flask import jsonify
from models.client_model import Client
from flask_jwt_extended import create_access_token
from datetime import timedelta

def _get_client_by_email(data):
    email = data.get('email')
    password = data.get('senha')
    
    if not email or not password:
        return jsonify({'message': 'Email e senha são obrigatórios'}), 400
    
    client_exist: Client = Client.query.filter_by(email=email).first()
    if not client_exist:
        return jsonify({"message": "Fudeu"}), 400
    
    return client_exist, password

def _check_client_password(password, client : Client) -> bool:
    password_valid = client.check_password(password)
    if not password_valid:
        return False
    return True

def get_user_with_request(request):
    client, password = _get_client_by_email(request)
    if _check_client_password(password, client):
        return client
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