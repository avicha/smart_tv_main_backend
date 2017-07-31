# coding=utf-8
from flask import Blueprint
from backend_common.controllers.base import BaseController
from backend_common.middlewares.request_service import get_request_params
from backend_common.models.database import db
from bson.objectid import ObjectId
from backend_common.models.es import es


singer_blueprint = Blueprint('singer', __name__)


class SingerController(BaseController):

    @classmethod
    @get_request_params()
    def search(cls, data):
        result = []
        keywords = data.get('keywords')
        page = int(data.get('page', 1))
        rows = int(data.get('rows', 20))
        scores_map = {}
        ids = []
        resp = es.search(index='smart_tv', doc_type='singers', body={
            'query': {
                'multi_match': {
                    'query': keywords,
                    'fields': ['name', 'alias']
                }
            }
        }, from_=(page - 1)*rows, size=rows, sort='_score:desc', _source=False)
        max_score = resp.get('hits').get('max_score')
        hits = filter(lambda x: x.get('_score') == max_score, resp.get('hits').get('hits'))
        for x in hits:
            ids.append(ObjectId(x.get('_id')))
            scores_map.update({x.get('_id'): x.get('_score')})
        qs = {'_id': {'$in': ids}, 'status': 3}
        total_rows = db.singers.count(qs)
        q = db.singers.find(qs)
        for x in q:
            _id = str(x.get('_id'))
            x.update({'_id': _id, '_score': scores_map.get(_id)})
            result.append(x)
        result.sort(key=lambda x: -x.get('album_num'))
        return cls.success_with_list_result(total_rows, result)
