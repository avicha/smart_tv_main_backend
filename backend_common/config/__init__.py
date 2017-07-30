# coding=utf-8
import backend_common.env as common_env
import database
import mail

# 环境变量
mode = common_env.APP_MODE

# 数据库配置
database = database.config(mode)
# 邮箱配置
mail = mail.config(mode)
