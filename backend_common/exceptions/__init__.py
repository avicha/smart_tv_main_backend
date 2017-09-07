# coding=utf-8
from backend_common.exceptions.base_error import BaseError
from backend_common.services.remote_api import RemoteAPIError


def uncaught_error_handler(e):
    import sys
    from flask import jsonify, current_app
    current_app.log_exception(sys.exc_info())
    return jsonify({'errcode': 500, 'errmsg': e.__class__.__name__})


def init_app(server):
    exceptions = [BaseError, RemoteAPIError]
    for e in exceptions:
        server.register_error_handler(e, e.handler)
    server.register_error_handler(Exception, uncaught_error_handler)
