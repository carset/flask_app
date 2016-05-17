#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from app import db


class ButtonType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    code = db.Column(db.String(128))

    def __unicode__(self):
        return u'%s' % self.name


class Button(db.Model):
    __tablename__ = 'button'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_id = db.Column(db.Integer, db.ForeignKey(ButtonType.id))
    name = db.Column(db.String(128), nullable=False)
    key = db.Column(db.String(128))
    parent_id = db.Column(db.Integer, db.ForeignKey('button.id'))
    url = db.Column(db.String(128))

    type = db.relationship(ButtonType, uselist=False)
    parent = db.relationship('Button', uselist=False, remote_side=[id])

    def __unicode__(self):
        return u'%s' % self.name


class Custom(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(128), nullable=False)
    nickname = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)

# End
