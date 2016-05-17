#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from flask import Blueprint, request

from app.wechat.helpers import access_token
from .modules import db, Member

# from .modules import db, MemberMeta

home = Blueprint('home_act', __name__, url_prefix='/home')


@home.route('/auto_login')
def auto_login():
    code = request.args.get('code', None)
    user_info = access_token(code) if code is not None else None
    query = db.session.query(Member).filter_by(open_id=user_info['openid']).first() if user_info is not None else None
    if query is not None:
        return "Success."
    else:
        return "invalid user."

# End
