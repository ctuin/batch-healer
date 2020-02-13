#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ======== Ctuin ========
# Author: Xiao_Jin

import time
import ping
from logzero import logger

# 设置
VERSION = '1.0.01'
SERVER_LIST = [{
    'host': 's0.ctuin.xyz',
    'name': 'SkEy-Serv',
    'up': True
},
{
    'host': 's1.ctuin.xyz',
    'name': 'SkEy-S1',
    'up': True
},
{
    'host': 's2.ctuin.xyz',
    'name': 'SkEy-S2',
    'up': True
}]
PORT = 443
ICMPING_NUM = 4
DELAY_TIME = 5
SKIP_TIME = 4

logger.info('Batch-Healer - %s 已启动' % VERSION)

def init():
    for server in SERVER_LIST:
        server['up'] = True
        server['skip'] = 0

def main():
    while True:
        for server in SERVER_LIST:
            if server['up'] == True:
                runping(server)
            else:
                if server['skip'] >= SKIP_TIME:
                    server['skip'] = 0
                    runping(server)
                else:
                    server['skip'] += 1
        delay(DELAY_TIME)

def runping(server):
    logger.info('已选中 %s(%s)' % (server['name'], server['host']))
    if ping.auto_tcping(server['host'], PORT):
        server['up'] = False
        logger.info('%s 已被标记为: 下线' % server['name'])
    else:
        if server['up'] == True:
            logger.info('%s 已上线' % server['name'])
        server['up'] = False
        logger.info('%s 已被标记为: 在线' % server['name'])

def delay(delay_time):
    logger.info('下次运行: %d 分钟后' % delay_time)
    time.sleep(delay_time * 60)

if __name__ == "__main__":
    init()
    main()