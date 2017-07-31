# coding=utf-8
APP_MODE = 'development'
# 数据库配置
DB_HOST = '127.0.0.1'
DB_PORT = 27017
DB_DATABASE = 'smart_tv'
DB_TZ_AWARE = True
DB_CONNECT = True
DB_OPTIONS = {
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
