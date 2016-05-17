#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from app import db


class Member(db.Model):
    """
        会员信息
    """
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    open_id = db.Column(db.String(128), unique=True)
    nickname = db.Column(db.String(128))
    remark = db.Column(db.String(128))
    sex = db.Column(db.String(3))
    avatar = db.Column(db.String(256))
    memo = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __unicode__(self):
        return u'%s' % self.nickname

# End
