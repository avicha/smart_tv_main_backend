# coding=utf-8
import backend_common.env as common_env


class config:

    """数据库相关配置"""

    def __init__(self, mode):
        self.host = common_env.DB_HOST
        self.port = common_env.DB_PORT
        self.tz_aware = common_env.DB_TZ_AWARE
        self.connect = common_env.DB_CONNECT
        self.connect_options = common_env.DB_OPTIONS
