# coding=utf-8
APP_MODE = 'development'
# Mongodb数据库配置
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DATABASE = 'smart_tv'
MONGODB_TZ_AWARE = True
MONGODB_CONNECT = True
MONGODB_CONNECTION_OPTIONS = {
    'minPoolSize': 4,
    'maxPoolSize': 16,
    'connectTimeoutMS': 5000,
    'socketTimeoutMS': 10000,
    'appname': 'appname'
}
# ES配置
ES_HOSTS = ['localhost:9200']
ES_CONNECTION_OPTIONS = {

}
# 邮件配置
MAIL_HOST = 'smtp.exmail.qq.com'
MAIL_PORT = 587
MAIL_TIMEOUT = 20
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_FROM_ADDR = '一起开工社区'
