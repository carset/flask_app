#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from jinja2 import Markup
from app.admin import sqla
from .modules import db
from .modules import Member


class MemberView(sqla.ModelView):
    def __init__(self, name=None, category=None):
        super(MemberView, self).__init__(Member, db.session, name=name, category=category)

    column_labels = dict(nickname=u'昵称', memo=u'备注', remark=u'别名', sex=u'性别', avatar=u'头像', date_created=u'更新日期',
                         department=u'单位')

    can_view_details = True

    column_details_list = ('avatar', 'sex', 'nickname', 'remark', 'memo', 'date_created',)
    column_exclude_list = ('open_id',)
    form_excluded_columns = ('open_id', 'date_created')

    column_formatters = dict(
        avatar=lambda v, c, m, n: user_avator(m),
        sex=lambda v, c, m, n: Markup('<span>%s</span>' % u'F' if m.sex == '2' else u'M'),
    )


def user_avator(m):
    if m.avatar:
        return Markup('<img src="%s/64"' % m.avatar.rstrip('/0'))
    else:
        return Markup(u'<span>无</span>')

# End
