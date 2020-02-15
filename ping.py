# -*- coding: UTF-8 -*-
# ======== Ctuin ========
# Author: Xiao_Jin & SkEy

import time
import socket
import requests
import dnsquery
from logzero import logger

TCPING_MAX_TRY = 4
TCPING_TIMEOUT = 1.5
TLSPING_PATH = '/health-check'
TLSPING_TIMEOUT = 4


def s_to_ms(second):  # 数学太难了，以至于我要单独写个函数
    return int(round(second, 3) * 1000)


def auto_tcping(host, port, dns_type):
    tried = 0
    while tried < TCPING_MAX_TRY:
        if not tcping(host, port):
            return False
        else:
            tried += 1

    # TCPing失败
    logger.error("连续 %d 次 TCPing 失败！" % tried)
    logger.info('正在检查是否为DNS污染...')
    try:
        if dnsquery.diff(host, dns_type):
            logger.error('域名 %s 已遭受DNS污染！' % host)
        else:
            logger.info('域名 %s 的 %s记录 正常' % (host, dns_type))
        return True
    except Exception as e:
        logger.warning('无法检查DNS污染情况，因为\n%s' % repr(e))
        return True


def tcping(host, port):
    logger.debug('正在运行TCPing...')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TCPING_TIMEOUT)
    logger.debug('Socket 已初始化')
    try:
        logger.debug('正在建立 TCP 连接')

        time_start = time.time()  # 计时开始
        s.connect((host, port))
        logger.debug('连接正常 正在尝试发送数据')
        s.send(b'Health-Check')
        time_end = time.time()  # 计时结束

        logger.debug('一切正常 测试结束')
        s.close()
        logger.info('TCPing正常: 用时 %sms' % s_to_ms(time_end - time_start))
        return False
    except Exception as e:
        logger.warning('出现错误: %s' % repr(e))
        s.close()
        logger.warning('TCPing失败！')
        return True


def tlsping(host):
    logger.debug('正在运行TLSPing...')
    try:
        time_start = time.time()  # 计时开始
        req = requests.get('https://%s%s' % (host, TLSPING_PATH), headers={'user-agent': 'Health-Check'},
                           timeout=TLSPING_TIMEOUT)
        time_end = time.time()  # 计时结束
        # 判断
        if req.status_code != 200:
            logger.error('HTTP状态码不正常！其为 [%s]' % req.status_code)
            return True
        elif req.text == 'OK':
            logger.info('TLSPing正常，用时 %sms' % s_to_ms(time_end - time_start))
            return False
        else:
            logger.error('TLSPing不正常！其返回内容如下\n%s' % req.text)
            return True
    except Exception as e:
        logger.error('出现错误: %s' % repr(e))
        logger.error('TLSPing失败！')
        return True
