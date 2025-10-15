from controllers.client.create_client import create_client
from flask import Blueprint

client_bp = Blueprint("client", "client", url_prefix="/client")

@client_bp.route("/create", methods=["POST"])
def criar_client():
    return create_client()