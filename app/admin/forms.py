#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
   admin.forms
"""
from wtforms import fields, validators
from flask.ext.wtf import Form


class LoginForm(Form):
    """
        后台登陆表单
    """
    account = fields.StringField('account', validators=[validators.required()])
    password = fields.PasswordField('password', validators=[validators.required()])
    remember_me = fields.BooleanField('remember_me', default=False)

# create: 15/11/27
# End
