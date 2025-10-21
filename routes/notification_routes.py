from flask import Blueprint
from controllers.notifcation.notification_controller import get_notifications, mark_as_read
# from middleware.auth import require_auth

notification_bp = Blueprint('notifications', __name__, url_prefix="/notification")

@notification_bp.route('/notifications', methods=['GET'])
# @require_auth
def get_user_notifications():
    return get_notifications()

@notification_bp.route('/notifications/<int:notification_id>/read', methods=['PUT'])
# @require_auth
def mark_notification_read(notification_id):
    return mark_as_read(notification_id)