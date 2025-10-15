from flask import Flask, jsonify
from database import db
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

from flask_cors import CORS
import os

from routes.client_routes import client_bp

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_KEY")

CORS(app=app)
JWTManager(app)

@app.route("/")
def index():
    return jsonify(
        {
            "message": "funcionando"
        }
    )

db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(client_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)