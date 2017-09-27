# coding=utf-8
from flask import Blueprint
from backend_common.controllers.base import BaseController
from backend_common.middlewares.request_service import get_request_params
from backend_common.models.mongodb import db

tv_blueprint = Blueprint('tv', __name__)


class TVController(BaseController):

    @classmethod
    @get_request_params()
    def search(cls, data):
        results = []
        total_rows = 0
        keywords = data.get('keywords')
        page = int(data.get('page', 1))
        rows = int(data.get('rows', 20))
        query = {'name': {'$regex': keywords}, 'category': 'tv'}
        total_rows = db.videos.count(query)
        cursor = db.videos.find(query).skip((page - 1)*rows).limit(rows)
        for x in cursor:
            x.update({'_id': str(x.get('_id'))})
            results.append(x)
        return cls.success_with_list_result(total_rows, results)
