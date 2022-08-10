# -*- coding: utf-8 -*-
# @Time : 2020/11/16 11:37
# @File : util.py
# @Author : Rocky C@www.30daydo.com

import datetime
import random
import smtplib
import time
import warnings
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import json
import pandas as pd
import re
import requests
from .settings import config, get_config_data


def notify(title='', desp=''):
    warnings.warn("该接口需要收费了，请使用企业微信")
    url = f"https://sc.ftqq.com/{config['WECHAT_ID']}.send?text={title}&desp={desp}"
    try:
        res = requests.get(url, timeout=5)
    except Exception as e:
        print(e)
        return False

    else:
        try:
            js = res.json()
            result = True if js['data']['errno'] == 0 else False
            if result:
                print('发送成功')
                return True
            else:
                print('发送失败')
                return False

        except Exception as e:
            print(e)
            print(res.text)


def read_web_headers_cookies(website, headers=False, cookies=False):
    config = get_config_data('web_headers.json')
    return_headers = None
    return_cookies = None

    if headers:
        return_headers = config[website]['headers']

    if cookies:
        return_headers = config[website]['cookies']

    return return_headers, return_cookies


def send_message_via_wechat(_message):  # 默认发送给自己
    _config = config['enterprise_wechat']
    userid = _config['userid']
    agentid = _config['agentid']
    corpid = _config['corpid']
    corpsecret = _config['corpsecret']

    response = requests.get(f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}")
    data = json.loads(response.text)
    access_token = data['access_token']

    json_dict = {
        "touser": userid,
        "msgtype": "text",
        "agentid": agentid,
        "text": {
            "content": _message
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    json_str = json.dumps(json_dict)
    response_send = requests.post(f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}",
                                  data=json_str)
    return json.loads(response_send.text)['errmsg'] == 'ok'








