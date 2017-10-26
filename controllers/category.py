# coding=utf-8
from flask import Blueprint
from backend_common.controllers.base import BaseController
import pymongo
from backend_common.models.mongodb import db

category_blueprint = Blueprint('category', __name__)


class CategoryController(BaseController):

    @classmethod
    def create(cls):
        categories = [
            {
                "type": "tv",
                "icon": "",
                "name": "电视剧",
                "desc": "我是电视剧"
            },
            {
                "type": "movie",
                "icon": "",
                "name": "电影",
                "desc": "我是电影"
            },
            {
                "type": "variety",
                "icon": "",
                "name": "综艺",
                "desc": "我是综艺"
            },
            {
                "type": "cartoon",
                "icon": "",
                "name": "动漫",
                "desc": "我是动漫"
            },
            {
                "type": "game",
                "icon": "",
                "name": "游戏",
                "desc": "我是游戏"
            },
            {
                "type": "live",
                "icon": "",
                "name": "直播",
                "desc": "我是直播"
            },
            {
                "type": "channel",
                "icon": "",
                "name": "电视",
                "desc": "我是电视"
            },
            {
                "type": "entertainment",
                "icon": "",
                "name": "娱乐",
                "desc": "我是娱乐"
            },
            {
                "type": "fun",
                "icon": "",
                "name": "搞笑",
                "desc": "我是搞笑"
            },
            {
                "type": "child",
                "icon": "",
                "name": "儿童",
                "desc": "我是儿童"
            },
            {
                "type": "music",
                "icon": "",
                "name": "音乐",
                "desc": "我是音乐"
            },
            {
                "type": "news",
                "icon": "",
                "name": "资讯",
                "desc": "我是资讯"
            },
            {
                "type": "sport",
                "icon": "",
                "name": "体育",
                "desc": "我是体育"
            },
            {
                "type": "education",
                "icon": "",
                "name": "教育",
                "desc": "我是教育"
            },
            {
                "type": "documentary",
                "icon": "",
                "name": "纪录片",
                "desc": "我是纪录片"
            },
            {
                "type": "military",
                "icon": "",
                "name": "军事",
                "desc": "我是军事"
            },
            {
                "type": "technology",
                "icon": "",
                "name": "科技",
                "desc": "我是科技"
            },
            {
                "type": "finance",
                "icon": "",
                "name": "财经",
                "desc": "我是财经"
            },
            {
                "type": "car",
                "icon": "",
                "name": "汽车",
                "desc": "我是汽车"
            },
            {
                "type": "travel",
                "icon": "",
                "name": "旅游",
                "desc": "我是旅游"
            },
            {
                "type": "baby",
                "icon": "",
                "name": "育儿",
                "desc": "我是育儿"
            }
        ]
        for index, category in enumerate(categories):
            category['sequence'] = index + 1
            db.categories.insert_one(category)
        return cls.success()

    @classmethod
    def list(cls):
        result = []
        q = db.categories.find({}, {'_id': False}).sort('sequence', pymongo.ASCENDING)
        for x in q:
            result.append(x)
        return cls.success_with_list_result(len(result), result)
