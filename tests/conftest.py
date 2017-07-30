# coding=utf-8
import sys
sys.path.append('.')
import pytest
from app import current_app
from flask import json


@pytest.fixture(scope="session")
def client():
    current_app.config['TESTING'] = True
    return current_app.test_client()


@pytest.fixture(scope="session")
def api_post(client):
    def f(url, *args, **kwargs):
        resp = client.post(url, *args, **kwargs)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        errcode = data.get('errcode')
        result = data.get('result')
        return errcode, result
    return f


@pytest.fixture(scope="session")
def api_get(client):
    def f(url, *args, **kwargs):
        resp = client.get(url, *args, **kwargs)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        errcode = data.get('errcode')
        result = data.get('result')
        return errcode, result
    return f


@pytest.fixture(scope="session")
def api_get_list(client):
    def f(url, *args, **kwargs):
        resp = client.get(url, *args, **kwargs)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        errcode = data.get('errcode')
        result = data.get('result')
        total_rows = data.get('total_rows')
        return errcode, result, total_rows
    return f
