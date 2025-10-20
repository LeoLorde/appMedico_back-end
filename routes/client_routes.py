from controllers.client.create_client import create_client
from controllers.client.login_client import client_login
from controllers.client.read_client import search_all, search_by_id, search_by_username
from controllers.client.remove_client import delete_client
from controllers.client.update_client import update_client
from flask import Blueprint
from limiter import limiter

client_bp = Blueprint("client", "client", url_prefix="/client")

@client_bp.route("/create", methods=["POST"])
def criar_client():
    return create_client()

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
def update_cliente(id):  
    return update_client(id)  

@client_bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_cliente(id):  
    return delete_client(id)
