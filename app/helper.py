#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
   Doc
"""
import hashlib
import importlib
import os
import pkgutil
from datetime import datetime
from flask import Blueprint, request, redirect, flash, url_for


def register_blueprints(app, package_name, package_path):
    """
        自动注册 Blueprint
    :param app:
    :param package_name:
    :param package_path:
    :return:
    """
    for _, name, _ in pkgutil.iter_modules(package_path):
        name = '%s.%s' % (package_name, name)
        m = importlib.import_module(name)
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, (Blueprint,)):
                app.register_blueprint(item)


def check_resource_dir(resource_dir, model=0755):
    """
        检查上传目录是否创建
    :param model:
    :param resource_dir:
    :return:
    """
    if not os.path.exists(resource_dir):
        os.mkdir(resource_dir, model)


def redirect_back(message=None):
    """
        返回上一个链接地址
    :param message:
    :return:
    """

    def back_referrer():
        for target in request.values.get('next'), request.referrer:
            if not target:
                continue
            return target

    if message is not None:
        flash(message)
    return redirect(back_referrer())


def encode_string(string):
    """Encodes a string to bytes, if it isn't already.

    :param string: The string to encode"""

    if isinstance(string, basestring):
        string = string.encode('utf-8')
    return string


def register_template_filter(app):
    """
        注册模板过滤器
    :param app:
    :return:
    """
    # 时间格式化
    app.add_template_filter(lambda t, f='%m/%d/%Y': t.strftime(f) if isinstance(t, datetime) else t, 'strftime')
    # md5字符串
    app.add_template_filter(lambda v: hashlib.md5(encode_string(v)).hexdigest(), 'md5')

# create: 15/12/1
# End
