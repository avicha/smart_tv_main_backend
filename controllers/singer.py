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
        exact_results = []
        fuzz_results = []
        keywords = data.get('keywords')
        page = int(data.get('page', 1))
        rows = int(data.get('rows', 20))
        scores_map = {}
        ids = []
        resp = es.search(index='smart_tv', doc_type='singers', body={
            'query': {
                'bool': {
                    'should': map(lambda x: {'multi_match': {'query': x, 'type': 'phrase', 'fields': ['name', 'alias']}}, keywords.split(','))
                }
            }
        }, from_=(page - 1)*rows, size=rows, sort='_score:desc', _source=False)
        hits = resp.get('hits').get('hits')
        if not len(hits):
            result = fuzz_results
            resp = es.search(index='smart_tv', doc_type='singers', body={
                'query': {
                    'multi_match': {
                        'query': ' '.join(keywords.split(',')),
                        'fields': ['name', 'alias^0.3'],
                        'type': 'best_fields',
                        'minimum_should_match': '80%'
                    }
                }
            }, from_=(page - 1)*rows, size=rows, sort='_score:desc', _source=False)
            hits = resp.get('hits').get('hits')
        else:
            result = exact_results
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
        result.sort(key=lambda x: -x.get('_score'))
        return cls.success_with_list_result(total_rows, {'exact_results': exact_results, 'fuzz_results': fuzz_results})
