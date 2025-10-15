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
    client : Client = Client.query.filter_by(id=id)
    if not client:
        return {"message": "Nenhum cliente encontrado"}
    
    return jsonify({
        client.toMap()
    })
    
def search_by_username(username: str):
    client : Client = Client.query.filter_by(username=username)
    if not client:
        return {"message": "Nenhum cliente encontrado"}
    
    return jsonify({
        client.toMap()
    })