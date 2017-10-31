# coding=utf-8
from flask import Blueprint
import re
import pymongo
from backend_common.controllers.base import BaseController
from backend_common.middlewares.request_service import get_request_params
from backend_common.models.mongodb import db

tv_blueprint = Blueprint('tv', __name__)


class TVController(BaseController):

    @classmethod
    def get_search_options(cls):
        search_options = [{
            'key': 'type',
            'text': '类型',
            'type': 'radio',
            'values': [{
                'text': '不限',
                'value': '-1'
            }, {
                'text': '剧情',
                'value': '11'
            }, {
                'text': '青春',
                'value': '13'
            }, {
                'text': '都市',
                'value': '18'
            }, {
                'text': '玄幻',
                'value': '21'
            }, {
                'text': '历史',
                'value': '20'
            }, {
                'text': '悬疑',
                'value': '15'
            }, {
                'text': '战争',
                'value': '19'
            }, {
                'text': '武侠',
                'value': '22'
            }, {
                'text': '科幻',
                'value': '16'
            }, {
                'text': '喜剧',
                'value': '17'
            }, {
                'text': '网剧',
                'value': '14'
            }, {
                'text': '原创',
                'value': '12'
            }, {
                'text': '儿童',
                'value': '23'
            }, {
                'text': '其他',
                'value': '24'
            }]
        }, {
            'key': 'region',
            'text': '地区',
            'type': 'radio',
            'values': [{
                'text': '不限',
                'value': '-1'
            }, {
                'text': '内地',
                'value': '100'
            }, {
                'text': '香港',
                'value': '101'
            }, {
                'text': '台湾',
                'value': '102'
            }, {
                'text': '韩国',
                'value': '105'
            }, {
                'text': '美国',
                'value': '103'
            }, {
                'text': '日本',
                'value': '106'
            }, {
                'text': '英国',
                'value': '104'
            }, {
                'text': '其他',
                'value': '107'
            }]
        }, {
            'key': 'years',
            'text': '年份',
            'type': 'radio',
            'values': [{
                'text': '不限',
                'value': ''
            }, {
                'text': '2017',
                'value': '2017'
            }, {
                'text': '2016',
                'value': '2016'
            }, {
                'text': '2015',
                'value': '2015'
            }, {
                'text': '2014',
                'value': '2014'
            }, {
                'text': '2013',
                'value': '2013'
            }, {
                'text': '2012',
                'value': '2012'
            }, {
                'text': '2011',
                'value': '2011'
            }, {
                'text': '2010',
                'value': '2010'
            }, {
                'text': '2000-2009',
                'value': '2000-2009'
            }, {
                'text': '90年代',
                'value': '1990-1999'
            }, {
                'text': '其他',
                'value': '-1989'
            }]
        }, {
            'key': 'is_vip',
            'text': '资费',
            'type': 'radio',
            'values': [{
                'text': '不限',
                'value': '-1'
            }, {
                'text': '免费',
                'value': '0'
            }, {
                'text': 'VIP',
                'value': '1'
            }]
        }, {
            'key': 'sort',
            'text': '排序',
            'type': 'radio',
            'values': [{
                'text': '最新',
                'value': 'new'
            }, {
                'text': '最热',
                'value': 'hot'
            }]
        }]
        return cls.success_with_result(search_options)

    @classmethod
    @get_request_params()
    def search(cls, data):
        results = []
        total_rows = 0
        keywords = data.get('keywords')
        tv_type = data.get('type')
        years = data.get('years', '')
        is_vip = data.get('is_vip')
        region = data.get('region')
        page = int(data.get('page', 1))
        rows = int(data.get('rows', 20))
        sort = data.get('sort', 'new')
        query = {'category': 'tv'}
        resource_query = {'status': {'$not': {'$eq': -1}}}
        fields = ['_id', 'name', 'resources.id', 'resources.source', 'resources.folder', 'resources.actors', 'resources.is_vip', 'resources.status']
        query_tags = []
        if keywords:
            query.update({'name': {'$regex': keywords}})
        if tv_type and tv_type != '-1':
            query_tags.append(int(tv_type))
        if region and region != '-1':
            query_tags.append(int(region))
        if len(query_tags):
            query.update({'tags': {'$all': query_tags}})
        if is_vip == '0':
            resource_query.update({'is_vip': False})
        if is_vip == '1':
            resource_query.update({'is_vip': True})
        if re.match(r'^\d{4}$', years):
            start_time = years + '-01-01'
            end_time = years + '-12-31'
            resource_query.update({'publish_date': {'$gte': start_time, '$lte': end_time}})
        if re.match(r'^-\d{4}$', years):
            end_time = years[1:-1] + '-12-31'
            resource_query.update({'$or': [{'publish_date': {'$lte': end_time}}, {'publish_date': {'$eq': None}}]})
        if re.match(r'^\d{4}-$', years):
            start_time = years[0:4] + '-01-01'
            resource_query.update({'$or': [{'publish_date': {'$gte': start_time}}, {'publish_date': {'$eq': None}}]})
        if re.match(r'^\d{4}-\d{4}$', years):
            start_time = re.match(r'^(\d{4})-\d{4}$', years).group(1) + '-01-01'
            end_time = re.match(r'^\d{4}-(\d{4})$', years).group(1) + '-12-31'
            resource_query.update({'publish_date': {'$gte': start_time, '$lte': end_time}})
        query.update({'resources': {'$elemMatch': resource_query}})
        print(query)
        if sort == 'new':
            sorts = [('resources.publish_date', pymongo.DESCENDING), ('resources.created_at', pymongo.ASCENDING)]
        elif sort == 'hot':
            sorts = [('resources.play_count', pymongo.DESCENDING), ('resources.created_at', pymongo.ASCENDING)]
        else:
            sorts = [('resources.publish_date', pymongo.DESCENDING), ('resources.created_at', pymongo.ASCENDING)]
        total_rows = db.videos.count(query)
        cursor = db.videos.find(query, fields).skip((page - 1)*rows).limit(rows).sort(sorts)
        for x in cursor:
            x.update({'_id': str(x.get('_id'))})
            resources = x.get('resources')
            resource = resources[0]
            del x['resources']
            x.update({'resource': resource})
            results.append(x)
        return cls.success_with_list_result(total_rows, results)

    @classmethod
    @get_request_params()
    def get_detail(cls, data):
        id = data.get('id')
        source = int(data.get('source'))
        fields = ['_id', 'name', 'resources.id', 'resources.source', 'resources.status', 'resources.current_part', 'resources.part_count', 'resources.director', 'resources.alias', 'resources.types', 'resources.desc', 'resources.actors_detail', 'resources.actors', 'resources.update_notify_desc', 'resources.score', 'resources.publish_date', 'resources.folder', 'resources.region', 'resources.is_vip']
        tv = db.videos.find_one({'resources': {'$elemMatch': {'id': id, 'source': source}}}, fields)
        resource = list(filter(lambda x: x.get('id') == id, tv.get('resources')))[0]
        del tv['resources']
        tv.update({'_id': str(tv.get('_id')), 'resource': resource})
        return cls.success_with_result(tv)

    @classmethod
    @get_request_params()
    def get_parts(cls, data):
        id = data.get('id')
        source = int(data.get('source'))
        query = {'id': id, 'source': source}
        video_parts = db.video_parts.find_one(query)
        videos = video_parts.get('parts')
        for video in videos:
            video.update({'id': id, 'source': source})
        return cls.success_with_list_result(len(videos), videos)
