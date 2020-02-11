#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ======== Ctuin ========
# Author: Xiao_Jin

from ping3 import ping
from logzero import logger


def do(ip, ping_amount):
    logger.debug('- ICMPING -')
    amount = 0
    status_list = []

    while amount < ping_amount:
        amount += 1  # A simple counter

        ping_result = ping(ip, unit='ms', timeout=2)
        if ping_result is None:
            status_list.append('timed-out')
        elif ping_result is False:
            status_list.append('dns-err')
        else:
            ping_ms = str(round(ping_result)) + 'ms'
            status_list.append(ping_ms)

    if status_list.count('timed-out') is ping_amount:  # 全部超时
        logger.error('ICMP阻断： ' + str(status_list))
        return False
    elif status_list.count('timed-out') > 0:  # 部分超时
        logger.warning('ICMP疑似阻断： ' + str(status_list))
        return False
    elif status_list.count('dns-err') is ping_amount:  # 无法解析，不排除DNS污染
        logger.error('DNS无法解析： ' + str(status_list))
        return False
    else:
        logger.info('ICMP正常： ' + str(status_list))
        return True
