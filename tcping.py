#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ======== Ctuin ========
# Author: Xiao_Jin

import socket
from logzero import logger
import time


def do(ip, port):
    logger.debug('- TCPING -')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        time_start = time.time()  # 计时开始
        s.connect((ip, port))
        s.send(b'GET / HTTP/1.1\n\n')
        time_end = time.time()  # 计时结束
        s.close()

        logger.info('TCP正常，用时%sms' % int(round(time_end - time_start, 3) * 1000))  # 小学二年级数学
        return True
    except:
        time_end = time.time()  # 计时结束
        s.close()

        logger.error('TCP阻断，耗时%sms' % int(round(time_end - time_start, 3) * 1000))  # 小学二年级数学
        return False
