#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ======== Ctuin ========
# Author: Xiao_Jin & SkEy

import time
import ping
from logzero import logger

# 设置
VERSION = '1.0.04'
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
DELAY_TIME = 0.3
SKIP_TIME = 2


def init():
    logger.info('Batch-Healer - %s 已启动' % VERSION)
    logger.info('从列表中加载了 %s 台服务器' % len(SERVER_LIST))
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
    if ping.auto_tcping(server['host'], PORT, server['dns-type']):  # TCP失败
        if server['available']:
            logger.error('%s 的状态已转变为 <不可用> ！' % server['name'])
            server['skip-time'] = SKIP_TIME
        else:
            logger.error('%s 的状态仍然为 <不可用> ！' % server['name'])
            server['skip-time'] = SKIP_TIME
        # 放这里不影响上面的判断
        server['available'] = False

    else:  # TCP成功
        if not ping.tlsping(server['host']):  # TLS也成功
            if not server['available']:
                logger.info('%s 已从 <不可用> 恢复为 <可用>' % server['name'])
                server['available'] = True
        else:  # TLS失败
            if server['available']:
                logger.error('%s 的状态已转变为 <不可用> ！' % server['name'])
                server['skip-time'] = SKIP_TIME
            else:
                logger.error('%s 的状态仍然为 <不可用> ！' % server['name'])
                server['skip-time'] = SKIP_TIME
            server['available'] = False


def delay(delay_time):
    try:
        logger.debug('下个运行周期: %s 分钟后' % delay_time)
        time.sleep(delay_time * 60)
    except KeyboardInterrupt:
        logger.warning('您希望 [Enter]终止运行 还是 [AnyKey]进入下个周期')
        choice = input('[Batch-Healer] Enter / AnyKey&Enter >>>')
        if choice == '':
            logger.info('Batch-Healer 已停止运行')
            exit()
        else:
            pass


if __name__ == "__main__":
    init()
    main()
