from flask import Flask
from database import db
from flask_jwt_extended import JWTManager
import os

from models.user_model import User
from models.appointment_model import Appointment
from models.client_model import Client
from models.doctor_model import Doctor
from models.endereco_model import Address 

from routes.client_routes import client_bp
from routes.doctor_routes import doctor_bp
from routes.address_routes import address_bp

def create_flask_app(testing=False) -> Flask:
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')

    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True

    db.init_app(app)

    with app.app_context():
        if app.config.get('DEBUG', False):
            print("🔍 Models registrados:")
            print("  - User:", User)
            print("  - Doctor:", Doctor)
            print("  - Client:", Client)
            print("  - Appointment:", Appointment)
            print("  - Address:", Address)

            print("\nTabelas encontradas pelo metadata:")
            print(list(db.metadata.tables.keys()))

        db.create_all()

        if app.config.get('DEBUG', False):
            print("\nTabelas criadas com sucesso!")

    JWTManager(app)
    app.register_blueprint(client_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(address_bp)

    return app
