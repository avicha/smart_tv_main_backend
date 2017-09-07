# coding=utf-8
import http.client
import urllib
from urllib.parse import urlparse
import json
import time

import logging
handler = logging.StreamHandler()
# 实例化formatter
formatter = logging.Formatter('%(asctime)-15s %(message)s')
# 为handler添加formatter
handler.setFormatter(formatter)


class RemoteAPIError(Exception):

    def __init__(self, errcode, errmsg):
        self.errcode = errcode
        self.errmsg = errmsg

    def handler(self):
        import sys
        from flask import jsonify, current_app
        if not current_app.testing:
            current_app.log_exception(sys.exc_info())
        return jsonify({'errcode': self.errcode, 'errmsg': self.errmsg})


class RemoteAPI(object):

    def __init__(self, name, config):
        self.name = name
        self.config = config
        self.logger = logging.getLogger(name)
        self.logger.setLevel('DEBUG')
        self.logger.addHandler(handler)

    def post(self, path, payload={}):
        start = time.time()
        o = urlparse(self.config.server_host)
        # 建立连接
        if o.scheme == 'http':
            conn = httplib.HTTPConnection(o.netloc)
        else:
            conn = httplib.HTTPSConnection(o.netloc)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        # 发送请求
        conn.request('POST', self.config.api_prefix + path, body=urllib.urlencode(payload, True), headers=headers)
        # 获取返回数据
        response = conn.getresponse()
        data = response.read()
        # 关闭连接
        conn.close()
        end = time.time()
        self.logger.debug('POST FORM %s%s%s，耗时%sms', self.config.server_host, self.config.api_prefix, path, (end - start)*1000)
        # HTTP正常返回
        if response.status == 200:
            ret = json.loads(data)
            errcode = ret.get('errcode')
            errmsg = ret.get('errmsg')
            result = ret.get('result')
            total_rows = ret.get('total_rows')
            if errcode:
                raise RemoteAPIError(errcode, errmsg)
            else:
                if total_rows != None:
                    return result, total_rows
                else:
                    return result
        else:
            # HTTP请求错误
            raise RemoteAPIError(response.status, data)

    def post_json(self, path, payload={}):
        start = time.time()
        o = urlparse(self.config.server_host)
        # 建立连接
        if o.scheme == 'http':
            conn = httplib.HTTPConnection(o.netloc)
        else:
            conn = httplib.HTTPSConnection(o.netloc)
        headers = {"Content-Type": "application/json; charset=UTF-8"}
        # 发送请求
        conn.request('POST', self.config.api_prefix + path, body=json.dumps(payload), headers=headers)
        # 获取返回数据
        response = conn.getresponse()
        data = response.read()
        # 关闭连接
        conn.close()
        end = time.time()
        self.logger.info('POST JSON %s%s%s，耗时%sms', self.config.server_host, self.config.api_prefix, path, (end - start)*1000)
        # HTTP正常返回
        if response.status == 200:
            ret = json.loads(data)
            errcode = ret.get('errcode')
            errmsg = ret.get('errmsg')
            result = ret.get('result')
            total_rows = ret.get('total_rows')
            if errcode:
                raise RemoteAPIError(errcode, errmsg)
            else:
                if total_rows != None:
                    return result, total_rows
                else:
                    return result
        else:
            # HTTP请求错误
            raise RemoteAPIError(response.status, data)

    def get(self, path, payload={}):
        start = time.time()
        o = urlparse(self.config.server_host)
        # 建立连接
        if o.scheme == 'http':
            conn = httplib.HTTPConnection(o.netloc)
        else:
            conn = httplib.HTTPSConnection(o.netloc)
        # 发送请求
        url = self.config.api_prefix + path + '?' + urllib.urlencode(payload, True)
        conn.request('GET', url)
        # 获取返回数据
        response = conn.getresponse()
        data = response.read()
        # 关闭连接
        conn.close()
        end = time.time()
        self.logger.info('GET %s%s，耗时%sms', self.config.server_host, url, (end - start)*1000)
        # HTTP正常返回
        if response.status == 200:
            ret = json.loads(data)
            errcode = ret.get('errcode')
            errmsg = ret.get('errmsg')
            result = ret.get('result')
            total_rows = ret.get('total_rows')
            if errcode:
                raise RemoteAPIError(errcode, errmsg)
            else:
                if total_rows != None:
                    return result, total_rows
                else:
                    return result
        else:
            # HTTP请求错误
            raise RemoteAPIError(response.status, data)
