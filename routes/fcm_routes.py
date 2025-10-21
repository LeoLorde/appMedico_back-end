from flask import Blueprint
from controllers.fcm.fcm_controller import save_fcm_token, delete_fcm_token
# from middleware.auth import require_auth

fcm_bp = Blueprint('fcm', __name__, url_prefix="/fcm")

@fcm_bp.route('/fcm-token', methods=['POST'])
# @require_auth
def save_token():
    return save_fcm_token()

@fcm_bp.route('/fcm-token', methods=['DELETE'])
# @require_auth
def delete_token():
    return delete_fcm_token()