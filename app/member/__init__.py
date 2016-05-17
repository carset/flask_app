#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
    单位机构, 会员信息管理
"""
from app.admin import admin
from .views import MemberView

admin.add_view(MemberView(category=u'用户管理', name=u'用户信息管理'))

# End
