#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ========= Ctuin Frp ========
# Author: Xiao_Jin

import socket
import logprint


def do(ip, port):
    logprint.log('- TCPING -')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
    try:
        s.connect((ip, port))  # v2ray服务器的443端口
        s.send(b'GET / HTTP/1.1\n\n')
        s.close()  # 关闭连接
        return True
    except:
        s.close()  # 关闭连接
        return False


if __name__ == '__main__':
    do('google.com', 443)