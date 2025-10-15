from models.client_model import Client
from flask import request, jsonify

def search_all(limit: int):
    client_list : list[Client] = Client.query.limit(limit).all()

    if not client_list:
        return {"message": "Nenhum cliente encontrado"}
    
    return jsonify([
        client.toMap()
        for client in client_list
    ])

def search_by_id(id: int):
    client : Client = Client.query.filter_by(id=id).first()
    if not client:
        return {"message": "Nenhum cliente encontrado"}, 404
    
    return jsonify(
        client.toMap()
    ), 200
    
def search_by_username(username: str, limit: int):
    client_list : Client = Client.query.filter_by(username=username).limit(limit).all()
    if not client_list:
        return {"message": "Nenhum cliente encontrado"}, 400
    
    return jsonify([
        client.toMap()
        for client in client_list
    ])