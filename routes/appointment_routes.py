from controllers.appointment.create_appointment import create_appointment
from controllers.appointment.confirm_appointment import confirm_appointment
from controllers.appointment.search_appointment import search_by_doctor_appointment, search_by_doctor_pending_appointment, search_by_client_appointment, search_appointments_by_day
from controllers.appointment.refuse_appointment import refused_appointment
from controllers.appointment.get_all_appointments import search_all
from flask import Blueprint

appointment_bp = Blueprint("appointment", "appointment", url_prefix="/appointment")

@appointment_bp.route("/create", methods=["POST"])
def criar_appointment():
    return create_appointment()

@appointment_bp.route("/confirm", methods=["PUT"])
def conf_appointment():
    return confirm_appointment()

@appointment_bp.route("/doc", methods=["GET"])
def by_doctor():
    return search_by_doctor_appointment()

@appointment_bp.route("/refuse", methods=["PUT"])
def ref_app():
    return refused_appointment()

@appointment_bp.route("/doc/pending", methods=["GET"])
def by_doctor_pend():
    return search_by_doctor_pending_appointment()

@appointment_bp.route("/client", methods=["GET"])
def by_client():
    return search_by_client_appointment()

@appointment_bp.route("/date/<string:date>", methods=["GET"])
def search_by_day(date):
    return search_appointments_by_day(date)

@appointment_bp.route("/")
def get_all():
    return search_all()