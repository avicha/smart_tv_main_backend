# coding=utf-8
import backend_common.env as common_env
import mongodb
import elastic_search
import mail

# 环境变量
mode = common_env.APP_MODE

# 数据库配置
mongodb = mongodb.config(mode)
# ES配置
elastic_search = elastic_search.config(mode)
# 邮箱配置
mail = mail.config(mode)
