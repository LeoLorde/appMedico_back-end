from controllers.address.create_address import create_addres
from flask import Blueprint

address_bp = Blueprint("address", "address", url_prefix="/address")

@address_bp.route("/create", methods=["POST"])
def criar_address():
    return create_addres()
