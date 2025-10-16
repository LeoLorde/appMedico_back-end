from controllers.doctor.create_doctor import create_doctor
from controllers.doctor.login_doctor import doctor_login
from flask import Blueprint

doctor_bp = Blueprint("doctor", "doctor", url_prefix="/doctor")

@doctor_bp.route("/")
def index_main():
    return {"message": "connected"}

@doctor_bp.route("/create", methods=["POST"])
def create_doctor_func():
    return create_doctor()

@doctor_bp.route("/login", methods=["POST"])
def login_doctor():
    return doctor_login()