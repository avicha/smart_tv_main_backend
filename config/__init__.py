# coding=utf-8
import config.server
import config.logger
import config.cache

from backend_common.config import *
# 服务器配置
server = server.config(mode)
# 日志配置
log = logger.config(mode)
# 缓存配置
cache = cache.config(mode)
