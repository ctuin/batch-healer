#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ======== Ctuin ========
# Author: Xiao_Jin

from logzero import logger

# ToDO instead with the v2ray link
requests_url = 'http://localhost/api/servers.json'  # Web-API address


def get():
    import requests
    try:
        req = requests.get(requests_url)
    except requests.exceptions.ConnectionError:
        logger.error('无法连接至主服务器\nURL: %s\n - requests.exceptions.ConnectionError' % requests_url)
        return False

    # If connected successfully
    if req.status_code == 200:
        logger.info('服务器列表已重载')
        return req.json()
    else:
        logger.error('无法获取服务器列表\nURL: %s\nHTTP状态码: %d' % (requests_url, req.status_code))
        return False
