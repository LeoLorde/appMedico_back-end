from models.client_model import Client
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.validators import InputValidator

@jwt_required()
def search_all(limit: int):
    try:
        max_limit = min(limit, 100)
        client_list: list[Client] = Client.query.limit(max_limit).all()

        if not client_list:
            return jsonify({"message": "Nenhum cliente encontrado"}), 404
        
        return jsonify([
            InputValidator.sanitize_output(client.toMap())
            for client in client_list
        ]), 200
        
    except Exception as e:
        return jsonify({'message': 'Erro ao buscar clientes', 'error': str(e)}), 500

@jwt_required()
def search_by_id(id: int):
    try:
        current_user = get_jwt_identity()
        if current_user.get('type') == 'client' and current_user.get('id') != id:
            return jsonify({'message': 'Acesso negado'}), 403
        
        client: Client = Client.query.filter_by(id=id).first()
        if not client:
            return jsonify({"message": "Nenhum cliente encontrado"}), 404
        
        return jsonify(InputValidator.sanitize_output(client.toMap())), 200
        
    except Exception as e:
        return jsonify({'message': 'Erro ao buscar cliente', 'error': str(e)}), 500

@jwt_required()    
def search_by_username(username: str, limit: int):
    try:
        if not username or len(username) < 2:
            return jsonify({"message": "Username inválido"}), 400
        
        max_limit = min(limit, 100)
        client_list: list[Client] = Client.query.filter_by(username=username).limit(max_limit).all()
        
        if not client_list:
            return jsonify({"message": "Nenhum cliente encontrado"}), 404
        
        return jsonify([
            InputValidator.sanitize_output(client.toMap())
            for client in client_list
        ]), 200
        
    except Exception as e:
        return jsonify({'message': 'Erro ao buscar clientes', 'error': str(e)}), 500
