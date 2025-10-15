# app.py
from flask import Flask
from database import db
from flask_jwt_extended import JWTManager

def create_app(testing=False) -> Flask:
    app = Flask(__name__)

    # GERAL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'sua_chave_jwt_aqui'

    if testing:
        # TESTES
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True

    # OTHER
    db.init_app(app)
    JWTManager(app)

    # BLUEPRINTS
    from routes.client_routes import client_bp
    app.register_blueprint(client_bp)

    return app
