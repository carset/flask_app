#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import json
import re
import datetime
from app import app, celery, cache
from app.member.modules import Member
from .modules import db, Button, ButtonType, Custom
from .helpers import create_button, get_user_list, batch_get_user_info
from .helpers import get_button
from .helpers import add_custom, update_custom, del_custom, get_custom


@celery.task
def update_wx_button():
    """
        更新微信按钮菜单
    :return:
    """
    with app.app_context():
        query = db.session.query(Button).filter_by(parent=None).all()
        items = []
        for item in query:
            button = dict(name=item.name)  # 初始化一个Button
            if item.type:
                button['type'] = item.type.code
            if item.key:
                button['key'] = item.key
            if item.url:
                button['url'] = item.url
            create_sub_button(button, item.id)
            items.append(button)
        payload = json.dumps(dict(button=items), ensure_ascii=False).encode('utf8')
        return create_button(payload)


@celery.task
def sync_wx_members():
    """
        获取关注用户列表;并更新到本地数据库
    :return:
    """
    with app.app_context():
        step = 100  # 微信接口限制批量获取用户信息最大每次100条
        data = get_user_list()
        for offset in xrange(0, len(data), step):
            item_id = data[offset:offset + step]
            items = batch_get_user_info(item_id)
            if items is not None:
                for item in items:
                    member = db.session.query(Member).filter_by(open_id=item['openid']).first() or Member()
                    member.nickname = strip_emoji(item['nickname'])
                    member.open_id = item['openid']
                    member.remark = item['remark']
                    member.sex = item['sex']
                    member.avatar = item['headimgurl']
                    member.date_created = datetime.datetime.now()
                    db.session.add(member)
        db.session.commit()


@celery.task
def sync_wx_button():
    """
        同步自定义菜单
    :return:
    """
    buttons = get_button()
    items = buttons.get('menu', {}).get('button', {})
    # 清空本地 - mysql only
    db.session.execute('TRUNCATE %s' % Button.__tablename__)
    for item in items:
        button = Button()
        button.name = item.get('name')
        # button.key = item.get('key')
        db.session.add(button)
        db.session.commit()
        for sub in item.get('sub_button'):
            child = Button()
            child.name = sub.get('name')
            child.key = sub.get('key')
            child.type_id = button_type().get(sub.get('type'))
            child.parent = button
            child.url = sub.get('url')
            db.session.add(child)
    db.session.commit()
    pass


@celery.task
def update_custom(custom, is_created=True):
    """
        更新客服信息
    :param is_created:
    :param custom:
    :return:
    """
    if is_created:
        return add_custom(custom)
    else:
        return update_custom(custom)


@celery.task
def delete_custom(custom):
    """
        删除客服信息
    :param custom:
    :return:
    """
    return del_custom(custom)


@celery.task
def sync_wx_custom():
    """
        同步客服信息
    :return:
    """
    db.session.query(Custom).delete()
    items = get_custom()
    if items is not None:
        for c in items:
            custom = Custom()
            custom.account = c['kf_account']
            custom.nickname = c['kf_nick']
    pass


@cache.cached(timeout=50, key_prefix='__type_dict')
def button_type():
    type_dict = dict()
    query = db.session.query(ButtonType).all()
    for item in query:
        type_dict.setdefault(item.code, item.id)
    return type_dict


def strip_emoji(text):
    """
        过滤用户昵称中的特殊符号(emoji)
    :param text:
    :return:
    """
    co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub('', text)


def create_sub_button(button, item_id):
    query = db.session.query(Button).filter_by(parent_id=item_id).all()
    for item in query:
        if 'sub_button' not in button:
            button['sub_button'] = []
        s = dict(name=item.name)  # 初始化一个Button
        if item.type:
            s['type'] = item.type.code
        if item.key:
            s['key'] = item.key
        if item.url:
            s['url'] = item.url
        button['sub_button'].append(s)

# End
