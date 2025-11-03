from flask import request, jsonify
from .login_client_logic import get_user_with_request, create_jwt_token, create_return_message

def client_login():
    try:
        client = get_user_with_request(request.get_json())
        jwt_token = create_jwt_token(client)
        return create_return_message(client, jwt_token)
        
    except Exception as e:
        return jsonify({'message': 'Erro ao fazer login', 'error': str(e)}), 500
