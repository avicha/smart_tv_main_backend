# coding=utf-8
from flask import Blueprint
from backend_common.controllers.base import BaseController
from backend_common.middlewares.request_service import get_request_params


album_blueprint = Blueprint('album', __name__)


class AlbumController(BaseController):

    @classmethod
    @get_request_params()
    def search(cls, data):
        exact_results = []
        fuzz_results = []
        total_rows = 0
        keywords = data.get('keywords')
        page = int(data.get('page', 1))
        rows = int(data.get('rows', 20))
        return cls.success_with_list_result(total_rows, {'exact_results': exact_results, 'fuzz_results': fuzz_results})
