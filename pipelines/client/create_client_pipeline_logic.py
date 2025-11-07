def return_formatted_error_response(response : dict):
    return {
            "success": False,
            "message": response.get("message", "Erro ao processar a solicitação."),
            "errors": response.get("errors") or response.get("error")
        }
def return_formatted_sucess_response(response: dict):
    return {
            "success": True,
            "message": response.get("message", "Operação realizada com sucesso."),
            "data": response.get("data", {})
        }