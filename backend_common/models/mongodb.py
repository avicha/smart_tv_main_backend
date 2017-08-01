# coding=utf-8
from pymongo import MongoClient
from backend_common.config import mongodb
client = MongoClient(host=mongodb.host, port=mongodb.port, tz_aware=mongodb.tz_aware, connect=mongodb.connect, **mongodb.connection_options)
db = client[mongodb.db]
