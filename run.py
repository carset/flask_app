#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
   Doc
"""
# import sys
#
# if "darwin" == sys.platform:
#     # Monkey path socket.sendall to handle EAGAIN (Errno 35) on mac.
#     import socket
#     import time
#
#
#     def socket_socket_sendall(self, data):
#         print '>>>>>>>>>>>>>>>>>', 'xxxxx'
#         while len(data) > 0:
#             try:
#                 bytes_sent = self.send(data)
#                 data = data[bytes_sent:]
#             except socket.error, e:
#                 if str(e) == "[Errno 35] Resource temporarily unavailable":
#                     time.sleep(0.1)
#                 else:
#                     raise e
#
#
#     socket._socketobject.sendall = socket_socket_sendall

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# create: 15/11/27
# End
