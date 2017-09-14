# coding=utf-8
from flask import Blueprint
from backend_common.controllers.base import BaseController
from backend_common.middlewares.request_service import get_request_params
from backend_common.models.mongodb import db

user_blueprint = Blueprint('user', __name__)


class UserController(BaseController):

    @classmethod
    @get_request_params()
    def status(cls, data):
        user = {
            'id': 1,
            'username': 'Avicha',
            'avatar': 'https://avatars1.githubusercontent.com/u/1276962'
        }
        return cls.success_with_result(user)
