#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
   Doc
"""
import os
import zipfile


class ZipBuilder(object):
    def __init__(self, archive):
        self.__zip = zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED)

    def add_bytes(self, arcname, data):
        self.__zip.writestr(arcname, data)

    def add_file(self, f):
        self.__zip.write(f, os.path.basename(f))

    def close(self):
        for f in self.__zip.filelist:
            f.create_system = 0
        self.__zip.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

# create: 15/11/27
# End
