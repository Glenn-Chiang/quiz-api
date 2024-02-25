from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException
from app import app


def error_response(status_code: int, message: str = None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    return payload, status_code


@app.errorhandler(HTTPException)
def handle_exception(error: HTTPException):
    return error_response(error.code, message=error.description)
