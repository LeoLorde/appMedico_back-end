from flask_jwt_extended import jwt_required, get_jwt_identity
from models.client_model import Client
from database import db
from flask import jsonify, request

def delete_client(id):
    try:
        if request.identity.get('type') != 'client' or request.identity.get('id') != id:
            return jsonify({'message': 'Acesso negado. Você só pode deletar seu próprio perfil'}), 403
        
        client = Client.query.get(id)
        if not client:
            return jsonify({'message': 'Cliente não encontrado'}), 404
            
        db.session.delete(client)
        db.session.commit()
        
        return jsonify({'message': 'Cliente deletado com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao deletar cliente', 'error': str(e)}), 500
