from chalice import Response


def base_error_json(message: str, status_code: int):
    body = {"status": "error", "error": message}
    return Response(body=body,
                    status_code=status_code,
                    headers={'Content-Type': 'application/json'})


def base_success_json(message: str, status_code: int, additional_data: dict = None):
    body = {"status": "ok", "details": message}
    if additional_data:
        body.update(additional_data)
    return Response(body=body,
                    status_code=status_code,
                    headers={'Content-Type': 'application/json'})