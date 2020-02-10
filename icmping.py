#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ========= Ctuin Frp ========
# Author: Xiao_Jin

from ping3 import ping
import logprint


def do(ip, ping_amount):
    logprint.log('- ICMPING -')
    amount = 0
    status_list = []

    while amount < ping_amount:
        amount += 1  # A simple counter

        ping_result = ping(ip, unit='ms', timeout=2)
        if ping_result is None:
            status_list.append('timed out')
            print('timed out', end=', ')
        else:
            ping_ms = str(round(ping_result)) + 'ms'
            status_list.append(ping_ms)
            print(ping_ms, end=', ')

    if status_list.count('timed out') is ping_amount:
        return False
    else:
        return True
