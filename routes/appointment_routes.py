from controllers.appointment.create_appointment import create_appointment
from controllers.appointment.confirm_appointment import confirm_appointment
from flask import Blueprint

appointment_bp = Blueprint("appointment", "appointment", url_prefix="/appointment")

@appointment_bp.route("/create", methods=["POST"])
def criar_appointment():
    return create_appointment()

@appointment_bp.route("/confirm", methods=["PUT"])
def conf_appointment():
    return confirm_appointment()
