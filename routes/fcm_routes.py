from flask import Blueprint
from controllers.fcm.save_fcm import save_fcm_token
from middlewares.auth_verificator import auth_middleware

fcm_bp = Blueprint('fcm', __name__, url_prefix="/fcm")

@fcm_bp.route('/create', methods=['POST'])
@auth_middleware
def save_token():
    print("RECEBENDO NO FCM/CREATE")
    return save_fcm_token()
