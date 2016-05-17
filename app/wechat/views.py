#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from flask import redirect, url_for, flash, make_response
from flask.ext.admin import expose, base
from flask.ext.admin.contrib import sqla
from flask.ext.login import current_user
from .modules import db, Button
from .modules import Custom
from .tasks import update_wx_button, sync_wx_members, sync_wx_button
from .tasks import update_custom, del_custom
from .helpers import md5


class ButtonView(sqla.ModelView):
    column_labels = dict(type=u'类型', parent=u'父菜单', name=u'名称', key=u'识别符', url=u'链接')

    def __init__(self, name=None, category=None):
        super(ButtonView, self).__init__(Button, db.session, name=name, category=category)

    def is_accessible(self):
        return current_user.is_authenticated


class CustomView(sqla.ModelView):
    column_labels = dict(account=u'账号', nickname=u'昵称', password=u'密码')

    def __init__(self, name=None, category=None):
        super(CustomView, self).__init__(Custom, db.session, name=name, category=category)

    def is_accessible(self):
        return current_user.is_authenticated

    def after_model_delete(self, model):
        super(CustomView, self).after_model_delete(model)
        del_custom(dict(kf_account=model.account, nickname=model.nickname, password=md5(model.password)))

    def after_model_change(self, form, model, is_created):
        super(CustomView, self).after_model_change(form, model, is_created)
        update_custom(dict(kf_account=model.account, nickname=model.nickname, password=md5(model.password)), is_created)


class SynchronizeView(base.BaseView):
    """
        微信数据同步功能集合
    """

    def __init__(self, category=None, name=None):
        super(SynchronizeView, self).__init__(category=category, name=name, endpoint='synchronize')

    @expose('/')
    def sync_member(self):
        sync_wx_members()
        return redirect(url_for('member.index_view'))

    @expose('/sync_button')
    def sync_button(self):
        sync_wx_button()
        return redirect(url_for('button.index_view'))

    @expose('/update_button')
    def update_button(self):
        # update_wx_button.delay()
        if update_wx_button():
            flash(u'数据更新成功')
        else:
            flash(u'数据更新失败')
        return redirect(url_for('button.index_view'))

    @expose('/sync_custom')
    def sync_custom(self):
        return redirect(url_for('custom.index_view'))

    def is_accessible(self):
        return current_user.is_authenticated


class UpdateButtonMenuLink(base.MenuLink):
    """
        更新微信菜单
    """

    def __init__(self, category=None, name=None):
        super(UpdateButtonMenuLink, self).__init__(name=name, category=category, endpoint='synchronize.update_button')

    def is_accessible(self):
        return current_user.is_authenticated


class SyncButtonMenuLink(base.MenuLink):
    """
        同步微信菜单
    """

    def __init__(self, category=None, name=None):
        super(SyncButtonMenuLink, self).__init__(name=name, category=category, endpoint='synchronize.sync_button')

    def is_accessible(self):
        return current_user.is_authenticated


class SyncCustomMenuLink(base.MenuLink):
    """
        同步客服信息
    """

    def __init__(self, category=None, name=None):
        super(SyncCustomMenuLink, self).__init__(name=name, category=category, endpoint='synchronize.sync_button')

    def is_accessible(self):
        return current_user.is_authenticated

# End
