#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
   Doc
"""
from __future__ import absolute_import
import os
import qrcode
from PIL import Image


class QRCodeBuilder(object):
    """
        二维码生成工具
    """

    def __init__(self, data):
        self._data = data
        self.builder = None
        self.image = None

        self._init_builder()

    def _init_builder(self):
        self.builder = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

    def make(self):
        self.builder.add_data(self._data)
        self.builder.make(fit=True)
        self.image = self.builder.make_image()
        self.image = self.image.convert('RGBA')

    def data(self, format='JPEG'):
        from io import BytesIO
        output = BytesIO()
        self.image.save(output, format=format)
        return output.getvalue()

    def save(self, name, path):
        abspath = os.path.join(path, '%s.png' % name)
        self.image.save(abspath)

    def add_logo(self, logo=None):
        if logo is not None and os.path.exists(logo):
            icon = Image.open(logo)
            img_w, img_h = self.image.size
            factor = 4
            size_w = int(img_w / factor)
            size_h = int(img_h / factor)

            icon_w, icon_h = icon.size
            if icon_w > size_w:
                icon_w = size_w
            if icon_h > size_h:
                icon_h = size_h
            icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

            w = int((img_w - icon_w) / 2)
            h = int((img_h - icon_h) / 2)
            icon = icon.convert("RGBA")
            self.image.paste(icon, (w, h), icon)

# create: 15/11/27
# End
