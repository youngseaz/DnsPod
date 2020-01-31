#!/usr/bin/python3

# API使用规范 https://www.dnspod.cn/docs/info.html
# API参考文档 https://www.dnspod.cn/docs/index.html

import os
import sys
import json
import logging
import requests

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))

from shell import gettoken


__all__ = ["get_ip", "add_record", "get_domain_id", "get_record_id", "get_info", "update"]


token = gettoken()


def get_ip():
    """
    获取当前主机的公网ip
    :return: ip address in string
    """
    url = "http://ipinfo.io"
    response = requests.get(url)
    data = json.loads(response.text)
    return data["ip"]


def request(url, data):
    """
    请求的时候必须设置UserAgent，如果不设置或者设置为不合法的（比如设置为浏览器的）也会导致帐号被封禁API。
    UserAgent的格式必须为：程序英文名称/版本(联系邮箱)，比如：MJJ DDNS Client/1.0.0 (shallwedance@126.com)。
    :param url:
    :param data:
    :return:
    """
    headers = {"User-Agent": "ddns powered by DnsPod/1.0.0 (email@youngseaz.com)",
               "Accept": "text/json"
               }
    try:
        response = requests.post(url=url, data=data, headers=headers, verify=True)
    except Exception as e:
        print("An exception occurred: ", e)
        sys.exit(1)
    return response


def get_info(domain, recordid):
    global token
    url = "https://dnsapi.cn/Record.Info"
    payload = {"login_token":token,
               "domain":domain,
               "record_id":recordid,
               "format":"json"
               }
    response = request(url, payload)
    data = json.loads(response.text)
    status = data["status"]
    if status["code"] != "1":
        logging.warning("code: %s   %s" % (status["code"], status["message"]))
        return None
    else:
        return data["record"]


def get_domain_id(yourdomain):
    url = "https://dnsapi.cn/Domain.List"
    payload = {"login_token":token, "format":"json"}
    response = request(url, payload)
    data = json.loads(response.text)
    if data.get("domains"):
        for domain in data["domains"]:
            if domain["name"] == yourdomain:
                return domain["id"]
    return None


def add_record(domain, recordtype="A", subdomain="@", line="默认"):
    """
    # https://www.dnspod.cn/docs/records.html#record-create

    :param domainid: example.com
    :param recordtype: A, AAAA, MX...etc
    :param subdomain: @, www, m...etc
    :param line: 默认，电信，移动，联通等
    """

    url = "https://dnsapi.cn/Record.Create"
    ip = get_ip()
    payload = {"login_token":token,
               "domain":domain,
               "sub_domain": subdomain,
               "record_type":recordtype,
               "value":ip,
               "record_line":line,
               "format":"json"
               }
    response = request(url, payload)
    data = json.loads(response.text)
    status = data["status"]
    code = int(status["code"])
    if code not in (1, 104):  # 1: add record successfully   104： record existed
        logging.critical("Fail to create record, code: %s   %s\n\
        visit https://www.dnspod.cn/docs/records.html#record-create for details." % (code, status["message"]))
        sys.exit(1)
    if code == 104:
        logging.info("code: %s   %s" % (code, status["message"]))
        return None
    else:
        logging.info("code: %s   %s" % (code, status["message"]))
        record = data["record"]
        return record["id"]
        
        
def get_record_id(domain, subdomain="@", recordtype="A", line="默认"):
    global token
    url = "https://dnsapi.cn/Record.List"
    payload = {"login_token":token,
               "domain":domain, 
               "sub_domain":subdomain,
               "record_type":recordtype,
               "record_line":line,
               "format":"json"
               }
    response = request(url, payload)
    data = json.loads(response.text)
    status = data["status"]
    code = status["code"]
    if code != "1":
        logging.error("Fail to obtain the id of %s, code:%s   %s" % (domain, code, status["message"]))
        return None
    record = data["records"][0]
    return record["id"]


def update(ip, domain, recordid, subdomain="@",  recordtype="A", line="默认", mx=None):
    """
    注意事项：
    如果1小时之内，提交了超过5次没有任何变动的记录修改请求，该记录会被系统锁定1小时，
    不允许再次修改。比如原记录值已经是 1.1.1.1，新的请求还要求修改为 1.1.1.1。

    """
    global token
    url = " https://dnsapi.cn/Record.Modify"
    payload = {"login_token":token,
               "domain":domain,
               "value":ip,
               "record_type":recordtype,
               "sub_domain":subdomain,
               "record_line":line,
               "record_id":recordid,
               "format": "json"
               }
    if recordtype == "MX" and mx != None:
        d = {"MX":mx}
        payload.update(d)
    response = request(url, payload)
    data = json.loads(response.text)
    status = data["status"]
    if status["code"] != "1":
        logging.error("Fail to update record, code: %s   %s\
                      visit https://www.dnspod.cn/docs/records.html#record-modify \
                      for details" % (status["code"], status["message"]))
    else:
        logging.info("%s, update at %s" % (status["message"], status["created_at"]))

