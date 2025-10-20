from controllers.expedient.create_expedient import create_expedient
from controllers.expedient.get_expedient import search_by_id
from flask import Blueprint

expedient_bp = Blueprint("expediente", "expediente", url_prefix="/expediente")

@expedient_bp.route("/create", methods=["POST"])
def criar_expedient():
    return create_expedient()

@expedient_bp.route("/id/<int:id>", methods=["GET"])
def get_expediente(id):
    return search_by_id(id)