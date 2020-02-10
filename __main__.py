#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ========= Ctuin Frp ========
# Author: Xiao_Jin

import servers
import logprint
import icmping
import tcping
import time
from ping3 import ping

# Settings
version = 'DEV'
v2ray_port = 443  # The port of v2ray server
ping_amount = 4  # The amount of ping of single server
delay_min = 0.1  # min

# INIT
print('=== Ctuin-Health-Check - %s ===' % version)

# Program
while True:
    print('=' * 60)

    # Get List
    servers_list = servers.get()
    if servers_list is False:
        # DELAY
        logprint.delay(delay_min)
        continue
    else:
        print('Start Pinging ...')

    # Ping
    for current_server in servers_list:
        server_expression = '%s (%s) - Owner: %s' % (
            current_server['name'], current_server['ip'], current_server['owner'])

        # ICMPING
        icmp_result = icmping.do(current_server['ip'], ping_amount)
        if icmp_result:
            print()  # Need a 'line feed symbol'
            logprint.log('\n OK ---- %s' % server_expression)
        else:
            print()  # Need a 'line feed symbol'
            logprint.log('\033[31m ERR ---- %s\033[0m' % server_expression)

        # TCPING
        tcp_result = tcping.do(current_server['ip'], v2ray_port)
        if tcp_result:
            logprint.log(' OK ---- %s' % server_expression)
        else:
            logprint.log('\033[31m ERR ---- %s\033[0m' % server_expression)

    # DELAY
    logprint.delay(delay_min)
