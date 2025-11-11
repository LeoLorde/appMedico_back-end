from controllers.doctor.create_doctor import create_doctor
from controllers.doctor.login_doctor import doctor_login
from controllers.doctor.read_doctor import search_all, search_by_id, search_by_username
from controllers.doctor.remove_doctor import delete_doctor
from controllers.doctor.update_doctor import update_doctor
from controllers.doctor.read_self_doctor import self_client

from middlewares.auth_verificator import auth_middleware

from flask import Blueprint
from limiter import limiter

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

@doctor_bp.route("/id/<string:id>")
def get_id(id):
    return search_by_id(id)

@doctor_bp.route("/username/<string:username>/<int:limit>")
def get_username(username, limit):
    return search_by_username(username, limit)

@doctor_bp.route("/update/<int:id>", methods=["PUT"])
@auth_middleware
def update_doctor_func(id):
    return update_doctor(id)

@doctor_bp.route("/delete/<int:id>", methods=["DELETE"])
@auth_middleware
def doctor_delete(id):
    return delete_doctor(id)

@doctor_bp.route("/")
def get_self_doctor():
    return self_client()