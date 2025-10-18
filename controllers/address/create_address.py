from models.endereco_model import Address
from flask import request, jsonify
from database import db

def create_addres():
    data = request.get_json()
    addres : Address = Address(
        id=data.get('id'),
        cidade=data.get('cidade'),
        estado=data.get('estado'),
        cep=data.get('cep'),
        rua=data.get('rua'),
        numero=data.get('numero'),
        complemento=data.get('complemento')
    )
    db.session.add(addres)
    db.session.commit()
    return jsonify({
        'message': 'Address criado com sucesso',
        'data': addres.to_dict()
    }), 201