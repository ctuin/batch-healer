# -*- coding: UTF-8 -*-
# ======== Ctuin ========
# Author: Xiao_Jin

import base64
import json
import requests
import settings
from logzero import logger


def vmess_parse(v2ray_url):
    logger.debug('正在解析vmess链接')
    servers_list = []
    for v2ray_link in v2ray_url.split():  # 分割
        # 提取关键部分，并进行解码；压缩了代码（虽然这样不好）
        v2ray_json = base64.b64decode(v2ray_link[len('vmess://'):].encode()).decode()
        v2ray_py = json.loads(v2ray_json)
        server_dict = {
            'host': v2ray_py['host'],
            'port': int(v2ray_py['port']),  # 必须为int
            'dns-type': 'A',  # 应该没有AAAA记录的吧（侥幸心理
            'name': v2ray_py['ps']
        }
        servers_list.append(server_dict)
    return servers_list


def subscribe_url(web_url):
    logger.debug('正在获取订阅')
    try:
        vmess_urls = requests.get(web_url, headers={'user-agent': 'Health-Check'}, timeout=8)
        return vmess_parse(vmess_urls.text)
    except requests.exceptions.InvalidSchema:
        raise Exception('不是有效的订阅链接(https/http)')
    except requests.exceptions.MissingSchema:
        raise Exception('不是有效的订阅链接（怕不是字符串）')
    except Exception as e:
        raise Exception(repr(e))


def auto():
    with open(settings.V2RAY_FILE, 'r') as file:
        urls = file.read()
    scheme = urls[:urls.find('://')]
    if scheme == 'https':
        server_list = subscribe_url(urls)
    elif scheme == 'vmess':
        server_list = vmess_parse(urls)
    elif scheme == 'http':
        server_list = subscribe_url(urls)
    else:
        raise Exception('不是有效的V2RAY_URL')
    return server_list
