#!/usr/bin/python
# -*- coding: UTF-8 -*-
from urllib import request, parse
import json, os, logging
import logger

Headers = {
    'Accept': 'text/json',
    'Content-type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }

def getRequest(api, data):
    return request.Request(url=f'https://dnsapi.cn/{api}', data=parse.urlencode(data).encode('utf-8'), headers=Headers, method='POST')


def get_domain_id(login_token, domain_name):
    params = dict(
        login_token=login_token,
        format="json"
    )
    req = getRequest('Domain.List', params)
    response = request.urlopen(req)
    data = json.loads(response.read().decode('utf-8'))

    if int(data['status']['code']) == 1:
        domails = data['domains']
        for domain in domails:
            if domain['name'] == domain_name:
                return domain['id']
        return 0
    else:
        return 0


def create_domain(login_token, domain_name):
    params = dict(
        login_token=login_token,
        format="json",
        domain = domain_name
    )
    req = getRequest('Domain.Create', params)
    response = request.urlopen(req)
    data = json.loads(response.read().decode('utf-8'))

    if int(data['status']['code']) == 1:
        return data['domain']['id']
    else:
        return 0


def get_record_value(login_token, domain_id, sub_domain):
    params = dict(
        login_token=login_token,
        format="json",
        domain_id = domain_id,
        sub_domain = sub_domain
    )
    req = getRequest('Record.List', params)
    response = request.urlopen(req)
    data = json.loads(response.read().decode('utf-8'))

    if int(data['status']['code']) == 1:
        records = data['records']
        for record in records:
            if record['type'] == 'A' and record['name'] == sub_domain:
                return record['value']
        return "127.0.0.1"
    else:
        return "127.0.0.1"


def get_record_id(login_token, domain_id, sub_domain):
    params = dict(
        login_token=login_token,
        format="json",
        domain_id = domain_id,
        sub_domain = sub_domain
    )
    req = getRequest('Record.List', params)
    response = request.urlopen(req)
    data = json.loads(response.read().decode('utf-8'))

    if int(data['status']['code']) == 1:
        records = data['records']
        for record in records:
            if record['type'] == 'A' and record['name'] == sub_domain:
                return record['id']
        return 0
    else:
        return 0


def create_record_id(login_token, domain_id, sub_domain, localIP):
    params = dict(
        login_token=login_token,
        format="json",
        domain_id = domain_id,
        sub_domain = sub_domain,
        record_type = 'A',
        record_line_id = "0",
        value = localIP
    )
    req = getRequest('Record.Create', params)
    response = request.urlopen(req)
    data = json.loads(response.read().decode('utf-8'))

    if int(data['status']['code']) == 1:
        logging.info(f"Sub_domain [{sub_domain}] create success")
    else:
        logging.error(f"Sub_domain [{sub_domain}] create failed")


def record_ddns(login_token, domain_id, record_id, sub_domain, localIP):
    req = getRequest('Record.Ddns')
    params = dict(
        login_token=login_token,
        format="json",
        domain_id = domain_id,
        record_id = record_id,
        sub_domain = sub_domain,
        record_line_id = "0",
        value = localIP
    )

    req = getRequest('Record.Ddns', params)
    response = request.urlopen(req)
    data = json.loads(response.read().decode('utf-8'))

    if int(data['status']['code']) == 1:
        logging.info(f"DDns Success for subdomain [{sub_domain}], IP change to {localIP}")
    else:
        logging.error(f"DDns Error for subdomain [{sub_domain}]: {data['status']['message']}")