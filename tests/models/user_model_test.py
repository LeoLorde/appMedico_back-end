from models.user_model import User
import pytest
def test_set_and_check_password():
    user = User(username="teste", email="teste@teste.com")
    user.set_password("senha123")

    assert user.password_hash is not None
    assert user.check_password("senha123") is True
    assert user.check_password("outrasenha") is False