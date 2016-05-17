#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
   Flask初始化脚本
"""
from flask import render_template, redirect, request, url_for
from flask.ext import login
from flask.ext.cache import Cache
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import CsrfProtect
from app.factory import create_app, create_celery_app
from app.helper import register_blueprints, check_resource_dir

# 初始化Flask
app = create_app()

# 跨域保护
csrf = CsrfProtect(app)

# 设置缓存
cache = Cache(app, config={'CACHE_TYPE': app.config.get('CACHE_TYPE', 'simple')})

# 异步线程应用
if app.config.get('CELERY_BROKER_URL', None):
    celery = create_celery_app(app)

# 定义数据库标示符
db = SQLAlchemy(app)

# 定义login_manager
login_manager = login.LoginManager(app)
login_manager.session_protection = 'strong'

# 加载所有的blueprints
register_blueprints(app, __name__, __path__)

check_resource_dir(app.config.get('RESOURCE_DIR'))


@login_manager.user_loader
def load_user(user_id):
    """
        加载用户信息
    :param user_id:
    :return:
    """
    from app.admin.models import User
    return db.session.query(User).filter_by(id=int(user_id)).one_or_none()


@login_manager.unauthorized_handler
def redirect_login():
    """验证失败的处理"""
    if request.path.startswith('/admin/'):
        return redirect(url_for('admin.login_view'))
    else:
        return redirect('/')


@app.errorhandler(404)
def error_404(error):
    """
        定义404错误页信息
    :param error:
    :return:
    """
    return render_template('404.html', error=error), 404


@app.errorhandler(400)
def error_404(error):
    """
        定义404错误页信息
    :param error:
    :return:
    """
    return render_template('400.html', error=error), 400


@app.errorhandler(403)
def error_403(error):
    """
        定义404错误页信息
    :param error:
    :return:
    """
    return render_template('403.html', error=error), 403


@app.errorhandler(500)
def error_500(error):
    """
        定义404错误页信息
    :param error:
    :return:
    """
    return render_template('500.html', error=error), 500


# 创建所有的数据库表
if app.config.get('REBUILD_DATABASE', False):
    db.drop_all()
db.create_all()

__all__ = ['app', 'cache', 'celery', 'db', 'csrf']
# create: 15/11/27
# End
