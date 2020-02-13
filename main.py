#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ======== Ctuin ========
# Author: Xiao_Jin & SkEy

import time
import ping
from logzero import logger

# 设置
VERSION = '1.0.03'
SERVER_LIST = [
    {
        'host': 's0.ctuin.xyz',
        'dns-type': 'A',
        'name': 'SkEy-Serv',
        'skip-time': 0,
        'available': True
    },
    {
        'host': 's1.ctuin.xyz',
        'dns-type': 'A',
        'name': 'SkEy-S1',
        'skip-time': 0,
        'available': True
    },
    {
        'host': 's2.ctuin.xyz',
        'dns-type': 'A',
        'name': 'SkEy-S2',
        'skip-time': 0,
        'available': True
    },
    {
        'host': 'lncn.org',
        'dns-type': 'A',
        'name': '[测试] Lncn.org',
        'skip-time': 0,
        'available': True
    }

]

PORT = 443
ICMPING_NUM = 4
DELAY_TIME = 0.2
SKIP_TIME = 1

logger.info('Batch-Healer - %s 已启动' % VERSION)


def init():
    for server in SERVER_LIST:
        server['available'] = True
        server['skip-time'] = 0


def main():
    while True:
        for server in SERVER_LIST:
            if server['available']:
                runping(server)
            elif server['skip-time'] == 0:
                runping(server)
            else:
                logger.info('- 已临时跳过 %s(%s) ，将在 %s 个周期后被重新选中' % (server['name'], server['host'], server['skip-time']))
                server['skip-time'] -= 1
        delay(DELAY_TIME)


def runping(server):
    logger.info('- 已选中 %s(%s)' % (server['name'], server['host']))
    if ping.auto_tcping(server['host'], PORT, server['dns-type']):
        if server['available']:
            logger.error('%s 的状态已转变为 <不可用> ！' % server['name'])
        else:
            logger.error('%s 的状态仍然为 <不可用> ！' % server['name'])
        # 放这里不影响上面的判断
        server['available'] = False

    else:
        if not server['available']:
            logger.info('%s 已从 <不可用> 恢复为 <可用>' % server['name'])
        server['available'] = True
        # logger.info('%s 已被标记为: 在线' % server['name'])


def delay(delay_time):
    logger.debug('下个运行周期: %s 分钟后' % delay_time)
    time.sleep(delay_time * 60)


if __name__ == "__main__":
    init()
    main()
