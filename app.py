from flask import jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from flasgger import Flasgger
from flask_jwt_extended import JWTManager
import os

from app_config import create_flask_app
from limiter import limiter

import firebase_admin
from firebase_admin import credentials, messaging

if not firebase_admin._apps:
    cred = credentials.Certificate("doctorhub-1f3c2-firebase-adminsdk-fbsvc-1d210b52b8.json")
    firebase_admin.initialize_app(cred)

load_dotenv()

app = create_flask_app()

allowed_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
CORS(app)

Flasgger(app, template_file="swagger.yaml")
JWTManager(app)

@app.route("/")
def index():
    return jsonify({"message": "funcionando"})

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
