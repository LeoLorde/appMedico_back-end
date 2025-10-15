from flask import Flask
from database import db
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_KEY")

JWTManager(app)

db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)