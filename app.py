from flask import jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
import os

from config import create_app

load_dotenv()

app = create_app()


CORS(app)
JWTManager(app)
Mail(app=app)

@app.route("/")
def index():
    return jsonify({"message": "funcionando"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
