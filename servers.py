#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ========= Ctuin Frp ========
# Author: Xiao_Jin

import time

requests_url = 'http://localhost/api/servers.json'  # Web-API address


def get():
    import requests
    try:
        req = requests.get(requests_url)
    except requests.exceptions.ConnectionError:
        time_prefix = '[%s]' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print('\033[31m%s\nURL: %s\n - requests.exceptions.ConnectionError\033[0m' % (time_prefix, requests_url))
        return False

    # If connected successfully
    time_prefix = '[%s]' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if req.status_code == 200:
        print('%s Servers List Loaded from Cloud' % time_prefix)
        return req.json()
    else:
        print('\033[31m%s\nURL: %s\nHTTP Status Code: %d\033[0m' % (time_prefix, requests_url, req.status_code))
        return False
