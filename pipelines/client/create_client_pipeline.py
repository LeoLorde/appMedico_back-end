from controllers.client.create_client import create_client
from .create_client_pipeline_logic import return_formatted_error_response, return_formatted_sucess_response
from flask import jsonify

def format_create_client_response():
    response, status_code = create_client()
    if response.get("errors") or response.get("error"):
        formatted_response = return_formatted_error_response(response)
    else:
        formatted_response = return_formatted_sucess_response(response)
    return jsonify(formatted_response), status_code
