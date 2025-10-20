from models.endereco_model import Address
from flask import request, jsonify
from database import db

def create_addres():
    try:
        data = request.get_json()
        
        cidade = data.get('cidade', '').strip()
        estado = data.get('estado', '').strip()
        cep = data.get('cep', '').strip()
        rua = data.get('rua', '').strip()
        numero = data.get('numero', '').strip()
        
        if not all([cidade, estado, cep, rua, numero]):
            return jsonify({'message': 'Campos obrigatórios: cidade, estado, cep, rua, numero'}), 400
        
        if len(cep) < 8 or len(cep) > 10:
            return jsonify({'message': 'CEP inválido'}), 400
        
        addres = Address(
            cidade=cidade,
            estado=estado,
            cep=cep,
            rua=rua,
            numero=numero,
            complemento=data.get('complemento', '')
        )
        
        db.session.add(addres)
        db.session.commit()
        
        return jsonify({
            'message': 'Endereço criado com sucesso',
            'data': addres.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao criar endereço', 'error': str(e)}), 500
