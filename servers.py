# -*- coding: UTF-8 -*-
# ======== Ctuin ========
# Author: Xiao_Jin

import base64
import json
import requests
import settings
from logzero import logger

sid = 0


def vmess_parse(v2ray_url, add=True):
    global sid
    if add:
        sid += 1

    logger.debug('[%d] 正在解析vmess链接' % sid)
    # 提取关键部分，并进行解码；压缩了代码（虽然这样不好）
    v2ray_json = base64.b64decode(v2ray_url[len('vmess://'):].encode()).decode()
    v2ray_py = json.loads(v2ray_json)
    server_dict = {
        'sid': sid,
        'host': v2ray_py['host'],
        'port': int(v2ray_py['port']),  # 必须为int
        'dns-type': 'A',  # 应该没有AAAA记录的吧（侥幸心理
        'name': v2ray_py['ps']
    }
    return server_dict


def subscribe_url(web_url):
    global sid
    logger.debug('[*] 正在获取订阅')
    try:
        vmess_base64 = requests.get(web_url, headers={'user-agent': 'Health-Check'}, timeout=8)
        vmess_urls = base64.b64decode(vmess_base64.text).decode()
        servers_list = []
        for vmess_url in vmess_urls.split():
            sid += 1
            servers_list.append(vmess_parse(vmess_url, add=False))
        return servers_list
    except requests.exceptions.InvalidSchema:
        raise Exception('[%d] 不是有效的订阅链接(https/http)' % sid)
    except requests.exceptions.MissingSchema:
        raise Exception('[%d] 不是有效的订阅链接（怕不是字符串）' % sid)
    except Exception as e:
        raise Exception(repr(e))


def auto_parse():
    with open(settings.V2RAY_FILE, 'r') as file:
        urls = file.read()

    def subscribe(links):
        for i in links:
            server_list.append(i)

    server_list = []
    # 分类
    for link in urls.split():  # 按行分割
        scheme = link[:link.find('://')]
        if scheme == 'https':
            subscribe(subscribe_url(link))
        elif scheme == 'vmess':
            server_list.append(vmess_parse(link))
        elif scheme == 'http':
            subscribe(subscribe_url(link))
        else:
            raise Exception('[%d] 含有无效的URL' % sid)
    return server_list