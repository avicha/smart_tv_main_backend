# coding=utf-8
import backend_common.env as common_env


class config:

    """服务器配置"""

    def __init__(self, mode):
        self.host = common_env.MAIL_HOST
        self.port = common_env.MAIL_PORT
        self.timeout = common_env.MAIL_TIMEOUT
        self.username = common_env.MAIL_USERNAME
        self.password = common_env.MAIL_PASSWORD
        self.from_addr = common_env.MAIL_FROM_ADDR
