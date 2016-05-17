#!/usr/bin/env python
# -*- encoding:utf-8 -*-
# import datetime

from flask import Blueprint
from flask import render_template
from flask import request
# from app import app
from app import csrf
from app.member.modules import Member
from .helpers import MessageResolver
from .helpers import message_handler
from .helpers import verify_signature

gateway = Blueprint('gw_act', __name__, url_prefix='/gw')


@gateway.route('/receive', methods=['GET'])
def verify():
    """
        接口验证
    :return:
    """
    if verify_signature(request.args.get('signature'), request.args.get('timestamp'),
                        request.args.get('nonce')):
        return render_template('gw/message.html', data=request.args.get('echostr'))
    else:
        return render_template("gw/fail.html")


@gateway.route('/receive', methods=['POST'])
@csrf.exempt
def receive():
    """
        接受微信事件通知
    :return:
    """
    if verify_signature(request.args.get('signature'), request.args.get('timestamp'),
                        request.args.get('nonce')):
        resolver = MessageResolver(request.data)
        # print request.data
        return resolver.handle()


@message_handler(None)
def default_handler(resolver):
    return render_template("gw/message/default.html")


@message_handler('click', 'search_device')
def find_device(resolver):
    """
        查询所有设备
    :param resolver:
    :return:
    """
    from_user = resolver.xpath('FromUserName')
    to_user = resolver.xpath('ToUserName')
    member = db.session.query(Member).filter_by(open_id=from_user).one_or_none()
    # if member is not None and member.department_id is not None:
    #     query = db.session.query(Device).filter_by(department_id=member.department_id)

    #     return render_template('gw/message/device_message.html',
    #                            from_user=to_user,
    #                            to_user=from_user,
    #                            create_time=datetime.datetime.now(),
    #                            count=query.count(),
    #                            devices=query.all(),
    #                            config=app.config)
    # else:
    #     return render_template('gw/message/fail.html',
    #                            from_user=to_user,
    #                            to_user=from_user,
    #                            create_time=datetime.datetime.now())
    pass
# End
