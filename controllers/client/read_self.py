from database import db
from models.client_model import Client
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

@jwt_required()
def self_client():
    id = get_jwt_identity()
    client : Client = Client.query.get(id)
    return jsonify({
        "user": client.toMap()
    })