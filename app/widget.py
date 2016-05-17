#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
   .widget
"""
from wtforms import fields, widgets


class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(fields.TextAreaField):
    widget = CKTextAreaWidget()

# create: 15/12/2
# End
