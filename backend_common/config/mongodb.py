# coding=utf-8
import backend_common.env as common_env


class config:

    """数据库相关配置"""

    def __init__(self, mode):
        self.host = common_env.MONGODB_HOST
        self.port = common_env.MONGODB_PORT
        self.tz_aware = common_env.MONGODB_TZ_AWARE
        self.connect = common_env.MONGODB_CONNECT
        self.connection_options = common_env.MONGODB_CONNECTION_OPTIONS
        self.db = common_env.MONGODB_DATABASE
