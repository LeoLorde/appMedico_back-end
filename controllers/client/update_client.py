from flask_jwt_extended import jwt_required
from models.client_model import Client
from database import db
from flask import request, jsonify

@jwt_required()
def update_client(id):
    data = request.get_json()
    
    client: Client = Client.query.get(id)
    if not client:
        return jsonify({
            'message': 'Cliente não encontrado'
        }), 404

    if 'username' in data:
        client.username = data['username']
    if 'email' in data:
        client.email = data['email']
    if 'password' in data:
        client.set_password(data['password'])
    if 'cpf' in data:
        client.set_cpf(data['cpf']) 
    if 'dataDeNascimento' in data:
        client.dataDeNascimento = data['dataDeNascimento']
    if 'gender' in data:
        client.gender = data['gender']

    db.session.commit()
    return jsonify({
        'message': 'Cliente atualizado com sucesso',
        'data': client.toMap()
    }), 200
