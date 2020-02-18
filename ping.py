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


def dns_query(host, dns_type):
    try:
        if dnsquery.diff(host, dns_type):
            return True  # 污染
        else:
            return False  # 没污染
    except Exception as e:
        return {'return': None, 'e': repr(e)}  # 无法检查会返回原因


def auto_tcping(sid, host, port):
    tried = 0
    while tried < TCPING_MAX_TRY:
        if not tcping(sid, host, port):
            return False
        else:
            tried += 1

    # TCPing失败
    logger.error("[%d] 连续 %d 次 TCPing 失败！" % (sid, tried))
    return True


def tcping(sid, host, port):
    logger.debug('[%d] 正在运行TCPing...' % sid)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TCPING_TIMEOUT)
    try:
        time_start = time.time()  # 计时开始
        s.connect((host, port))
        s.send(b'Health-Check')
        time_end = time.time()  # 计时结束

        s.close()
        logger.info('[%d] TCPing正常: 用时 %sms' % (sid, s_to_ms(time_end - time_start)))
        return False
    except Exception as e:
        logger.warning('[%d] 出现错误: %s' % (sid, repr(e)))
        s.close()
        logger.warning('[%d] TCPing失败！' % sid)
        return True


def tlsping(sid, host):
    logger.debug('[%d] 正在运行TLSPing...' % sid)
    try:
        time_start = time.time()  # 计时开始
        req = requests.get('https://%s%s' % (host, TLSPING_PATH), headers={'user-agent': 'Health-Check'},
                           timeout=TLSPING_TIMEOUT)
        time_end = time.time()  # 计时结束
        # 判断
        if req.status_code != 200:
            logger.error('[%d] HTTP状态码不正常！其为 [%s]' % req.status_code)
            return True
        elif req.text == 'OK':
            logger.info('[%d] TLSPing正常，用时 %sms' % (sid, s_to_ms(time_end - time_start)))
            return False
        else:
            logger.error('[%d] TLSPing不正常！其返回内容如下\n%s' % req.text)
            return True
    except Exception as e:
        logger.error('[%d] 出现错误: %s' % (sid, repr(e)))
        logger.error('[%d] TLSPing失败！' % sid)
        return True
