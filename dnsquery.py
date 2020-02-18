# -*- coding: UTF-8 -*-
# ======== Ctuin ========
# Author: Xiao_Jin

import requests
import dns.resolver

TIMEOUT = 7
doh_headers = {'accept': 'application/dns-json'}


def _cloudflare(domain, dns_type):
    doh_addr = 'https://cloudflare-dns.com/dns-query?name=%s&type=%s' % (domain, dns_type)
    req = requests.get(doh_addr, headers=doh_headers, timeout=TIMEOUT)
    resolve = req.json()
    results = []
    for ip in resolve['Answer']:
        results.append(ip['data'])
    return results


def _localdns(domain, dns_type):
    ans = dns.resolver.query(domain, dns_type)
    results = []
    for i in ans.response.answer:
        for j in i:
            if j.rdtype == 1:
                results.append(j.address)
    return results


def diff(domain, dns_type):
    authoritative_dns = sorted(_cloudflare(domain, dns_type))
    local_dns = sorted(_localdns(domain, dns_type))
    if authoritative_dns == local_dns:
        return False  # 没污染
    else:
        return True  # 污染
