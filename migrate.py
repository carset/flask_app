#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
   数据迁移工具
"""
from app import app, db
from flask_alembic import Alembic

with app.app_context():
    alembic = Alembic(app)
    alembic.revision('add column desc')
    alembic.upgrade()


# create: 15/11/30
# End
