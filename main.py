#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# ======== Ctuin ========
# Author: Xiao_Jin & SkEy

import servers
import settings
import time
import ping
from logzero import logger

# 设置
VERSION = '1.0.04'
SERVER_LIST = servers.auto()
ICMPING_NUM = 4
DELAY_TIME = settings.DELAY_TIME
SKIP_TIME = settings.SKIP_TIME


def init():
    logger.info('加载了 %s 台服务器' % len(SERVER_LIST))
    for server in SERVER_LIST:
        server['available'] = True
        server['skip-time'] = 0


def main():
    while True:
        for server in SERVER_LIST:
            # ping
            if server['available']:
                runping(server)
            elif server['skip-time'] == 0:
                runping(server)
            else:
                logger.info('已跳过 %s(%s) ，将在 %s 个周期后被重新选中' % (server['name'], server['host'], server['skip-time']))
                server['skip-time'] -= 1
        delay(DELAY_TIME)


def runping(server):
    logger.info('已选中 %s(%s)' % (server['name'], server['host']))
    if ping.auto_tcping(server['host'], server['port'], server['dns-type']):  # TCP失败
        if server['available']:
            logger.error('%s 的状态已转变为 <不可用> ！' % server['name'])
            server['skip-time'] = SKIP_TIME
        else:
            logger.error('%s 的状态仍然为 <不可用> ！' % server['name'])
            server['skip-time'] = SKIP_TIME
        # 放这里不影响上面的判断
        server['available'] = False

    else:  # TCP成功
        if not ping.tlsping('%s:%s' % (server['host'], server['port'])):  # TLS也成功
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
    global SERVER_LIST
    try:
        logger.debug('下个运行周期: %s 分钟后' % delay_time)
        time.sleep(delay_time * 60)
    except KeyboardInterrupt:
        logger.warning('您希望： \n[Enter] 终止运行\n[r] 重载服务器列表（这将重置测试结果）\n[其他字符] 进入下个周期')
        choice = input('[Batch-Healer] 请输入 >>>')
        if choice == '':
            logger.info('Batch-Healer 已停止运行')
            exit()
        if choice == 'r':
            SERVER_LIST = servers.auto()
            init()
        else:
            pass


if __name__ == "__main__":
    logger.info('Batch-Healer - %s 已启动' % VERSION)
    init()
    main()
