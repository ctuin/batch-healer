#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ========= Ctuin Frp ========
# Author: Xiao_Jin

import time


def log(values):
    time_prefix = '[%s] ' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(time_prefix + values)


def delay(delay_time):
    print('-- Waiting for %s min' % delay_time)
    time.sleep(delay_time * 60)