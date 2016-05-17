#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
    微信配置管理
"""
from app import app, db
from app.admin import admin
from .modules import ButtonType
from .views import ButtonView
from .views import SynchronizeView
from .views import UpdateButtonMenuLink
from .views import SyncButtonMenuLink
# from .views import CustomView
from .views import SyncCustomMenuLink

admin.add_view(ButtonView(category=u'系统设置', name=u'菜单信息设置'))
# admin.add_view(CustomView(category=u'系统设置', name=u'客服信息管理'))

admin.add_link(UpdateButtonMenuLink(category=u'数据同步', name=u'应用菜单设置'))
admin.add_view(SynchronizeView(category=u'数据同步', name=u'同步用户到本地'))
admin.add_link(SyncButtonMenuLink(category=u'数据同步', name=u'同步菜单到本地'))
admin.add_link(SyncCustomMenuLink(category=u'数据同步', name=u'同步客服到本地'))


@app.before_first_request
def init_button_type():
    """
        初始化按钮类型
    :return:
    """

    if db.session.query(ButtonType).filter_by(code='click').one_or_none() is None:
        db.session.add(ButtonType(name=u'点击推事件', code=u'click'))
        db.session.add(ButtonType(name=u'跳转URL', code=u'view'))
        # db.session.add(ButtonType(name=u'扫码推事件', code=u'scancode_push'))
        db.session.add(ButtonType(name=u'扫码推事件带提示', code=u'scancode_waitmsg'))
        # db.session.add(ButtonType(name=u'弹出系统拍照发图', code=u'pic_sysphoto'))
        db.session.add(ButtonType(name=u'弹出拍照或者相册发图', code=u'pic_photo_or_album'))
        # db.session.add(ButtonType(name=u'弹出微信相册发图器', code=u'pic_weixin'))
        # db.session.add(ButtonType(name=u'弹出地理位置选择器', code=u'location_select'))
        db.session.commit()

# End
