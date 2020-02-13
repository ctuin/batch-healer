#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ======== Ctuin ========
# Author: Xiao_Jin

import time
import socket
from logzero import logger

MAXTRY = 4
def auto_ping(ip, port):
    tried = 0
    while tried < MAXTRY:
        if tcping(ip, port) == False:
            return False
        tried += 1
    logger.error("连续 %d 次 TCPing 失败")
    return True

def tcping(ip, port):
    logger.info('正在运行TCPing...')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        time_start = time.time()  # 计时开始
        s.connect((host, port))
        s.send(b' ')
        time_end = time.time()  # 计时结束
        s.close()
        logger.info('TCPing正常: 耗时%sms' % int(round(time_end - time_start, 3) * 1000))
        return False
    except:
        time_end = time.time()  # 计时结束
        s.close()
        logger.warning('TCPing失败: 耗时%sms' % int(round(time_end - time_start, 3) * 1000))
        return True

def httping(host):
    logger.info('正在运行HTTPing...')
