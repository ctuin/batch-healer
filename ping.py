#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ======== Ctuin ========
# Author: Xiao_Jin

import time
import socket
from logzero import logger

TCPING_MAX_TRY = 4
TLSPING_PATH = '/health-check'

def auto_tcping(ip, port):
    tried = 0
    while tried < TCPING_MAX_TRY:
        if tcping(ip, port) == False:
            return False
        tried += 1
    logger.error("连续 %d 次 TCPing 失败" % tried)
    return True

def tcping(ip, port):
    logger.info('正在运行TCPing...')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.debug('Socket 已初始化')
    try:
        time_start = time.time()  # 计时开始
        logger.debug('正在建立 TCP 连接')
        s.connect((ip, port))
        logger.debug('连接正常 正在发送 GET 字符串')
        s.send(b'GET')
        logger.debug('一切正常 测试结束')
        time_end = time.time()  # 计时结束
        s.close()
        logger.info('TCPing正常: 耗时%sms' % int(round(time_end - time_start, 3) * 1000))
        return False
    except Exception as e:
        time_end = time.time()  # 计时结束
        logger.debug('出现错误: %s' % repr(e))
        s.close()
        logger.warning('TCPing失败: 耗时%sms' % int(round(time_end - time_start, 3) * 1000))
        return True

def tlsping(host):
    logger.info('正在运行TLSPing...')
