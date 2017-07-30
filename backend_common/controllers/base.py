# coding=utf-8
from flask import current_app, jsonify, redirect
from backend_common.exceptions import BaseError


class BaseController():

    @staticmethod
    def success_with_result(result):
        return jsonify({'errcode': 0, 'result': result})

    @staticmethod
    def success():
        return jsonify({'errcode': 0})

    @staticmethod
    def success_with_list_result(total_rows, result):
        return jsonify({'errcode': 0, 'total_rows': total_rows, 'result': result})

    @staticmethod
    def error_with_message(code, message):
        raise BaseError(code, message)

    @staticmethod
    def redirect(location):
        redirect_res = redirect(location)
        response = current_app.make_response(redirect_res)
        return response

    @staticmethod
    def response_with_json(json):
        return jsonify(json)
