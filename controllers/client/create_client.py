from flask import request, jsonify
from database import db
from utils.validators import ValidationError
from .create_client_logic import validate_client_data, get_non_sensible_data

def create_client():
    try:
        client = validate_client_data(request.get_json())
        
        db.session.add(client)
        db.session.commit()

        return jsonify({
            'message': 'Client criado com sucesso',
            'data': get_non_sensible_data(client)
        }), 201
        
    except ValidationError as e:
        return jsonify({'message': 'Erro de validação', 'errors': e.errors}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao criar cliente', 'error': str(e)}), 500
