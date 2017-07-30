# coding=utf-8
import sys
sys.path.append('.')
import pytest


@pytest.fixture(scope="session")
def dict_utils():
    import dict_utils
    return dict_utils
