from flask import Blueprint
from controllers.fcm.fcm_controller import save_fcm_token, delete_fcm_token
from middlewares.auth_verificator import auth_middleware

fcm_bp = Blueprint('fcm', __name__, url_prefix="/fcm")

@fcm_bp.route('/fcm-token', methods=['POST'])
@auth_middleware
def save_token():
    return save_fcm_token()

@fcm_bp.route('/fcm-token', methods=['DELETE'])
@auth_middleware
def delete_token():
    return delete_fcm_token()