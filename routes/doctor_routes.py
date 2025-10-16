from controllers.doctor.create_doctor import create_doctor
from controllers.doctor.login_doctor import doctor_login
from controllers.doctor.read_doctor import search_all, search_by_id, search_by_username
from controllers.doctor.remove_doctor import delete_doctor
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

@doctor_bp.route("/<int:limit>")
def get_all(limit):
    return search_all(limit)

@doctor_bp.route("/id/<int:id>")
def get_id(id):
    return search_by_id(id)

@doctor_bp.route("/username/<string:username>/<int:limit>")
def get_username(username, limit):
    return search_by_username(username, limit)

@doctor_bp.route("/delete/<int:id>")
def doctor_delete(id):
    return delete_doctor(id)