#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
   admin.Views
"""
from flask import request, redirect, url_for, flash
import flask.ext.admin as admin
from werkzeug.security import check_password_hash, generate_password_hash
import flask.ext.login as login
from app import db
from app.admin import sqla
from .forms import LoginForm
from .models import User, Role, BackupLog
from app.helper import redirect_back


class CustomAdminIndexView(admin.AdminIndexView):
    """
        后台功能定义
    """

    @admin.expose('/')
    @login.login_required
    def index(self):
        return super(CustomAdminIndexView, self).index()

    @admin.expose('/login', methods=['GET', 'POST'])
    def login_view(self):
        form = LoginForm(request.form)
        if form.validate_on_submit():
            user = db.session.query(User).filter_by(account=form.account.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login.login_user(user, remember=form.remember_me.data)
                return redirect(url_for('.index'))
            else:
                flash(u'账号密码信息错误')
        self._template_args['form'] = form
        return self.render('admin/login.html')

    @admin.expose('/logout')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))

    @admin.expose('/clear_cache')
    @login.login_required
    def clear_cache(self):
        from app import cache
        cache.clear()
        return redirect_back(u'缓存已经成功更新。')
        # return redirect_back('Cache clear success.')


class UserView(sqla.ModelView):
    """
        用户管理视图
    """
    column_list = ('role', 'account', 'date_created',)
    form_excluded_columns = ['date_created']
    column_labels = dict(account=u'账号', password=u'密码', role=u'角色', date_created=u'创建时间')

    def __init__(self, name=None, category=None):
        super(UserView, self).__init__(User, db.session, name=name, category=category)

    def on_model_change(self, form, model):
        if len(model.password):
            model.password = generate_password_hash(form.password.data)


class RoleView(sqla.ModelView):
    """
        角色管理视图
    """
    column_list = ('name', 'date_created',)
    column_labels = dict(name=u'角色名称', date_created=u'创建时间')
    form_excluded_columns = ['date_created']

    def __init__(self, name=None, category=None):
        super(RoleView, self).__init__(Role, db.session, name=name, category=category)


class AuthenticatedMenuLink(admin.base.MenuLink):
    """退出链接"""

    def is_accessible(self):
        return login.current_user.is_authenticated


class NotAuthenticatedMenuLink(admin.base.MenuLink):
    """登陆链接"""

    def is_accessible(self):
        return not login.current_user.is_authenticated


class CleanCacheMenuLink(admin.base.MenuLink):
    """
        清空缓存
    """

    def is_accessible(self):
        return login.current_user.is_authenticated


class BackupLogView(sqla.ModelView):
    """
        数据库备份视图
    """
    can_create = False
    can_delete = False
    can_edit = False

    column_labels = dict(event=u'事件', level=u'级别', admin=u'用户', msg=u'内容', ip=u'IP', date_created=u'时间')

    def __init__(self, name=None, category=None):
        super(BackupLogView, self).__init__(BackupLog, db.session, name=name, category=category)

# create: 15/11/27
# End
