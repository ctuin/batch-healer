#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ======== Ctuin ========
# Author: Xiao_Jin

import servers
import icmping
import tcping
import time
from logzero import logger

# Settings
version = 'DEV'
v2ray_port = 443  # The port of v2ray server TODO use the v2ray json
icmping_amount = 4  # The amount of ping of single server
delay_min = 0.2  # min

# INIT
logger.debug('=== Batch-Healer - %s ===\n\n' % version)


# DELAY
def delay(delay_time):
    logger.debug('-- 将在 %s分钟 后继续\n\n' % delay_time)
    time.sleep(delay_time * 60)


# Program
while True:
    # Get List
    servers_list = servers.get()
    if servers_list is False:
        # DELAY
        delay(delay_min)
        continue

    # Ping
    for current_server in servers_list:
        server_expression = '\n\t%s (%s) - Owner: %s' % (
            current_server['name'], current_server['ip'], current_server['owner'])
        logger.info(server_expression)

        icmping.do(current_server['ip'], icmping_amount)  # ICMPING
        tcping.do(current_server['ip'], v2ray_port)  # TCPING

    # DELAY
    delay(delay_min)
