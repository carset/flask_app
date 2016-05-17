#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from celery import Celery
from flask import Flask
import flask.ext.babelex as babel
from flask.ext.wtf import CsrfProtect

from app.helper import register_template_filter


def create_app(settings_override=None):
    # 初始化Flask
    flask = Flask(__name__)
    # 加载配置文件
    flask.config.from_object('config')
    # 加载自自定义配置
    flask.config.from_object(settings_override)
    # 设置中文化
    babel.Babel(flask, default_locale='zh_hans_CN')
    # 注册模板过滤器
    register_template_filter(flask)
    return flask


def create_celery_app(app=None, settings_override=None):
    app = app or create_app(settings_override)
    celery = Celery(app.name, broker=app.config.get('CELERY_BROKER_URL'))
    celery.conf.update(app.config)

    context_task = celery.Task

    class ContextTask(context_task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return context_task.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery

# create: 15/11/30
# End
