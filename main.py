#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ======== Ctuin ========
# Author: Xiao_Jin

import time
from ping import auto_tcping, httping
from logzero import logger

# 设置
VERSION = 'DEV'
SERVER_LIST = [{
    'host': 's0.ctuin.xyz',
    'name': 'SkEy-Serv'
},
{
    'host': 's1.ctuin.xyz',
    'name': 'SkEy-S1' 
},
{
    'host': 's2.ctuin.xyz',
    'name': 'SkEy-S2'
}]
PORT = 443
ICMPING_NUM = 4
DELAY_TIME = 5

logger.info('Batch-Healer - %s 已启动' % VERSION)

def delay(delay_time):
    logger.debug('下次运行: %f 分钟后' % delay_time)
    time.sleep(delay_time * 60)

while True:
    for server in SERVER_LIST:
        logger.info('已选中 %s(%s)' % (server['name'], server['host']))
        if auto_tcping(server['host'], PORT):
            logger.error('该服务器已被标记为: 不通')
    delay(DELAY_TIME)