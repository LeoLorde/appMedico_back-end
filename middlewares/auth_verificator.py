from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps

def auth_middleware(fn):
    """
    Middleware que autentica via JWT e adiciona request.identity
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            identity = get_jwt_identity()

            request.identity = identity

        except Exception as e:
            return jsonify({"error": "Token inválido ou ausente", "details": str(e)}), 401

        # Após a verificação ele continua
        return fn(*args, **kwargs)
    return wrapper
