# coding=utf-8
from flask import Blueprint
from backend_common.controllers.base import BaseController
import time

common_blueprint = Blueprint('common', __name__)


class CommonController(BaseController):

    @classmethod
    def now(cls):
        return cls.success_with_result(int(time.time()*1000))

    @classmethod
    def weather(cls):
        result = {
            'weather': '晴',
            'temperature': 32
        }
        return cls.success_with_result(result)
