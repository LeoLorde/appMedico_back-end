from pipelines.client.create_client_pipeline import format_create_client_response
from controllers.client.login_client import client_login
from controllers.client.read_client import search_all, search_by_id, search_by_username
from controllers.client.remove_client import delete_client
from controllers.client.update_client import update_client
from controllers.client.read_self import self_client
from middlewares.auth_verificator import auth_middleware
from flask import Blueprint
from limiter import limiter

client_bp = Blueprint("client", "client", url_prefix="/client")

@client_bp.route("/create", methods=["POST"])
def criar_client():
    return format_create_client_response()

@client_bp.route("/login", methods=["POST"])
def login_cliente():
    return client_login()

@client_bp.route("/<int:limit>")
def get_all(limit):
    return search_all(limit)

@client_bp.route("/id/<int:id>")
def get_id(id):
    return search_by_id(id)

@client_bp.route("/username/<string:username>/<int:limit>")
def get_username(username, limit):
    return search_by_username(username, limit)

@client_bp.route("/update/<int:id>", methods=["PUT"])
@auth_middleware
def update_cliente(id):  
    return update_client(id)  

@client_bp.route("/delete/<int:id>", methods=["DELETE"])
@auth_middleware
def delete_cliente(id):  
    return delete_client(id)

@client_bp.route("/")
def see_self():
    return self_client()