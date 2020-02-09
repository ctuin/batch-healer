#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ========= Ctuin Frp ========
# Author: Xiao_Jin

import servers
import time
from ping3 import ping

# Settings
version = 'DEV 20w07b'
ping_amount = 4  # The amount of ping of single server
delay_min = 0.1  # min

# INIT
print('=== Ctuin-Health-Check - %s ===' % version)

# Program
while True:
    # Get List
    servers_list = servers.get()
    if servers_list is False:
        # DELAY
        print('- Waiting for %s min' % delay_min)  # Here is better
        time.sleep(delay_min * 60)

        continue
    else:
        print('Start Pinging ...')

    # Ping
    for current_server in servers_list:
        amount = 0
        status_list = []
        print('---', end=' ')
        while amount < ping_amount:
            amount += 1  # A simple counter
            ping_result = ping(current_server['ip'], unit='ms', timeout=2)
            if ping_result is None:
                status_list.append('timed out')
                print('timed out', end=', ')
            else:
                ping_ms = str(round(ping_result)) + 'ms'
                status_list.append(ping_ms)
                print(ping_ms, end=', ')

        server_expression = '%s (%s) - Owner: %s' % (current_server['name'], current_server['ip'], current_server['owner'])
        time_prefix = '[%s]' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if status_list.count('timed out') is ping_amount:
            print('\n\033[31m%s ERR ---- %s\033[0m' % (time_prefix, server_expression))
        else:
            print('\n%s OK ---- %s' % (time_prefix, server_expression))

    # DELAY
    print('- Waiting for %s min' % delay_min)  # Here is better
    time.sleep(delay_min * 60)
