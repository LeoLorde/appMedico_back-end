from models.endereco_model import Address
from database import db

def test_create_address(app):
    with app.app_context():
        addr = Address(
            cidade="São Paulo",
            estado="SP",
            cep="01000-000",
            rua="Rua Teste",
            numero="123",
            complemento="Apto 45"
        )
        db.session.add(addr)
        db.session.commit()

        assert addr.id is not None
        assert addr.cidade == "São Paulo"
        assert addr.estado == "SP"
        assert addr.cep == "01000-000"
        assert addr.rua == "Rua Teste"
        assert addr.numero == "123"
        assert addr.complemento == "Apto 45"
