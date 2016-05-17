#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
   Doc
"""
import flask.ext.admin as admin
from werkzeug.security import generate_password_hash
from app import app, db
from .models import User, Role
from .views import CustomAdminIndexView
from .views import NotAuthenticatedMenuLink
from .views import AuthenticatedMenuLink
from .views import UserView
from .views import RoleView
from .views import BackupLogView
from .views import CleanCacheMenuLink

admin = admin.Admin(app, name=u'管理后台', index_view=CustomAdminIndexView(name=u'首页'))
# 登陆链接
admin.add_link(NotAuthenticatedMenuLink(name=u'登录', endpoint='admin.login_view'))
admin.add_link(AuthenticatedMenuLink(name=u'退出', endpoint='admin.logout_view'))

# 管理员
admin.add_view(UserView(category=u'系统信息', name=u'用户设置'))
admin.add_view(RoleView(category=u'系统信息', name=u'角色设置'))
admin.add_view(BackupLogView(category=u'系统信息', name=u'备份记录'))
admin.add_link(CleanCacheMenuLink(category=u'系统信息', name=u'更新缓存', endpoint='admin.clear_cache'))


@app.before_first_request
def init_admin():
    super_role = db.session.query(Role).filter_by(name=u'Administrator').first()
    if not super_role:
        super_role = Role(name=u'Administrator')
        db.session.add(super_role)
        db.session.commit()

    if not db.session.query(User).filter_by(account='root').first():
        super_user = User(account="root", password=generate_password_hash('__PASSWORD__'), role_id=super_role.id)
        db.session.add(super_user)
        db.session.commit()


__all__ = ['admin', ]

# create: 15/11/27
# End
