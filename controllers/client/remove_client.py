from flask_jwt_extended import jwt_required
from models.client_model import Client
from database import db
from flask import jsonify

@jwt_required()
def delete_client(id):
    client = Client.query.get(id)
    if not client:
        return jsonify({
            'message': 'Cliente não encontrado'
        }), 404
    db.session.delete(client)
    db.session.commit()
    return jsonify({
        'message': 'Cliente deletado com sucesso'
    }), 200