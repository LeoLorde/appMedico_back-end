import pytest
from database import db
from models.client_model import Client
from models.gender_enum import Gender
from datetime import datetime

def test_create_client(app):
    """Testa a criação de um client e hash do CPF"""
    with app.app_context():
        cpf_raw = "11144477735"

        client = Client(
            username="Mauricio",
            email="mauricio@example.com",
            dataDeNascimento=datetime(2005, 10, 16),
            gender=Gender.MAN
        )

        client.set_cpf(cpf_raw)
        
        db.session.add(client)
        db.session.commit()

        saved_client = Client.query.first()
        assert saved_client.username == "Mauricio"
        assert saved_client.email == "mauricio@example.com"
        assert saved_client.gender == Gender.MAN
        assert saved_client.dataDeNascimento == datetime(2005, 10, 16)
        
        assert saved_client.cpf != cpf_raw
        assert saved_client.check_cpf(cpf_raw) is True
        assert saved_client.check_cpf("11122233344") is False

def test_toMap(app):
    """Testa o método toMap"""
    with app.app_context():
        cpf_raw = "09307018952"

        client = Client(
            username="Lucas",
            email="lucas@example.com",
            dataDeNascimento=datetime(2000, 1, 1),
            gender=Gender.MAN
        )
        client.set_cpf(cpf_raw)
        db.session.add(client)
        db.session.commit()

        saved_client = Client.query.first()
        mapa = saved_client.toMap()

        assert mapa["username"] == "Lucas"
        assert mapa["email"] == "lucas@example.com"
        assert mapa["cpf"] == saved_client.cpf
        assert mapa["dataDeNascimento"] == datetime(2000, 1, 1)
        assert mapa["genero"] == "MAN"
