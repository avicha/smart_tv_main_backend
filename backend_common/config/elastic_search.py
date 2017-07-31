# coding=utf-8
import backend_common.env as common_env


class config:

    """数据库相关配置"""

    def __init__(self, mode):
        self.hosts = common_env.ES_HOSTS
        self.connection_options = common_env.ES_CONNECTION_OPTIONS
