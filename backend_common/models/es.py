# coding=utf-8
from elasticsearch import Elasticsearch
from backend_common.config import elastic_search, mode

es = Elasticsearch(elastic_search.hosts, **elastic_search.connection_options)
if mode == 'development':
    import logging
    logger = logging.getLogger('elasticsearch')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
