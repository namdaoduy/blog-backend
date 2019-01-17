import traceback

from flask import jsonify
from marshmallow import fields, Schema

from main import app


class Error(Exception):
    def __init__(self, error_data=None):
        super(Error)
        self.error_data = error_data or {}

    def to_response(self):
        resp = jsonify(ErrorSchema().dump(self).data)
        resp.status_code = self.status_code
        return resp


class ErrorSchema(Schema):
    error_code = fields.Int()
    error_message = fields.String()
    error_data = fields.Raw()


class StatusCode:
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    INTERNAL_SERVER_ERROR = 500


class ErrorCode:
    BAD_REQUEST = 40000
    VALIDATION_ERROR = 40001
    USER_ALREADY_EXISTS = 40002
    USER_DOES_NOT_EXIST = 40003
    METHOD_NOT_ALLOWED = 40007
    UNAUTHORIZED = 40100
    PERMISSION_DENIED = 40301
    NOT_FOUND = 40400
    INTERNAL_SERVER_ERROR = 50000


class NotFound(Error):
    status_code = StatusCode.NOT_FOUND
    error_code = ErrorCode.NOT_FOUND
    error_message = 'Not found'


class MethodNotAllowed(Error):
    status_code = StatusCode.METHOD_NOT_ALLOWED
    error_code = ErrorCode.METHOD_NOT_ALLOWED
    error_message = 'Method not allowed'


class Unauthorized(Error):
    status_code = StatusCode.UNAUTHORIZED
    error_code = ErrorCode.UNAUTHORIZED
    error_message = 'Unauthorized'


@app.errorhandler(404)
def page_not_found(error):
    return NotFound().to_response()


@app.errorhandler(405)
def method_not_allowed(error):
    return MethodNotAllowed().to_response()


@app.errorhandler(Error)
def error_handler(error):
    return error.to_response()


@app.errorhandler(Exception)
def internal_server_error_handler(error):
    traceback_exception = traceback.format_exc()
    print traceback_exception

    return jsonify({
        'error_message': 'Something went wrong',
        'error_code': ErrorCode.INTERNAL_SERVER_ERROR,
        'error_data': {}
    }), StatusCode.INTERNAL_SERVER_ERROR
