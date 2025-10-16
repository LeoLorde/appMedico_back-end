import pytest
from database import db
from models.doctor_model import Doctor
from models.endereco_model import Address
from datetime import datetime

def test_create_doctor(app):
    """Testa a criação de um doctor e hash do CRM"""
    with app.app_context():
        address = Address(
            rua="Rua Teste",
            numero="123",
            cidade="Cidade",
            estado="Estado",
            cep="00000-000"
        )
        db.session.add(address)
        db.session.commit()
        
        crm_raw = "555820/SP"

        doctor = Doctor(
            username="Mauricio",
            email="mauricio@example.com",
            especialidade="qualquer coisa",
            bio="tambem qualquer coisa",
            endereco_id = address.id
        )

        doctor.set_crm(crm_raw)
        
        db.session.add(doctor)
        db.session.commit()

        saved_doctor : Doctor = Doctor.query.first()
        assert saved_doctor.username == "Mauricio"
        assert saved_doctor.email == "mauricio@example.com"
        assert saved_doctor.especialidade == "qualquer coisa"
        assert saved_doctor.bio == "tambem qualquer coisa"
        
        assert saved_doctor.crm != crm_raw
        assert saved_doctor.check_crm(crm_raw) is True
        assert saved_doctor.check_crm("11122233344") is False

def test_toMap(app):
    """Testa o método toMap"""
    with app.app_context():
        address = Address(
            rua="Rua Teste",
            numero="123",
            cidade="Cidade",
            estado="Estado",
            cep="00000-000"
        )
        db.session.add(address)
        db.session.commit()
        crm_raw = "09307018952"

        doctor = Doctor(
            username="Mauricio",
            email="mauricio@example.com",
            especialidade="qualquer coisa",
            bio="tambem qualquer coisa",
            endereco_id = address.id
        )
        
        doctor.set_crm(crm_raw)
        db.session.add(doctor)
        db.session.commit()

        saved_doctor : Doctor = Doctor.query.first()
        mapa = saved_doctor.toMap()

        assert mapa["username"] == "Mauricio"
        assert mapa["email"] == "mauricio@example.com"
        assert mapa["especialidade"] == "qualquer coisa"
        assert mapa["bio"] == "tambem qualquer coisa"
