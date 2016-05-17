#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
   应用配置文件
"""
import os

# 调试开关
DEBUG = True

SECRET_KEY = '#$$%%%#*@()xxaaa$$3456##'

# 启用CSRF保护
WTF_CSRF_ENABLED = True

# 数据库配置信息
SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/DB_NAME?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# 是否打印SQL语句到控制台
SQLALCHEMY_ECHO = False

# 是否重建数据库
REBUILD_DATABASE = False

# 上传资源的存储目录
RESOURCE_DIR = os.path.join(os.path.dirname(__file__), 'tmp')

STATIC_URI = ''
SITE_URI = 'http://your_domain_name'

# 异步Celery配置
CELERY_BROKER_URL = 'amqp://'

CELERY_RESULT_BACKEND = 'amqp://'

# 公众号ID
WX_APP_ID = 'WX_APP_ID'
# 公众号安全吗
WX_APP_SECRET = 'WX_APP_SECRET'
# 接口自定义TOKEN
WX_APP_TOKEN = 'WX_APP_TOKEN'

# create: 15/11/27
# End
