#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
   admin.models
"""
import flask.ext.login as login
from app import db


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())


class Role(Base):
    """
        Admin后台用户角色定义
    """
    __tablename__ = 'sys_roles'

    name = db.Column(db.String(64))
    description = db.Column(db.String(128))

    def __unicode__(self):
        return u'%s' % self.name


class User(Base, login.UserMixin):
    """
        Admin后台用户定义
    """
    __tablename__ = 'sys_users'

    account = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey(Role.id))

    role = db.relationship(Role)

    def __unicode__(self):
        return u'%s' % self.account


class BackupLog(Base):
    """
        数据备份表
    """
    __tablename__ = 'sys_backup'

    event = db.Column(db.String(256))
    level = db.Column(db.String(128))
    admin = db.Column(db.String(128))
    msg = db.Column(db.Text())
    ip = db.Column(db.String(128))

    def __unicode__(self):
        return self.user_id

# create: 15/11/27
# End
