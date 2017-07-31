# coding=utf-8
from pymongo import MongoClient
from backend_common.config import database
client = MongoClient(host=database.host, port=database.port, tz_aware=database.tz_aware, connect=database.connect, **database.connection_options)
db = client[database.db]
