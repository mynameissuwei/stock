#-*-coding=utf-8-*-
import datetime
import json
import os
import re
import time

import requests
import parsel
from loguru import logger
from configure.util import send_message_via_wechat


class BaseService(object):

    def __init__(self, logfile='default.log'):
        self.logger = logger
        self.logger.add(logfile)
        self.init_const_data()
        self.params=None
        self.cookies=None

    def init_const_data(self):
        '''
        常见的数据初始化
        '''
        self.today = datetime.datetime.now().strftime('%Y-%m-%d')

    def check_path(self, path):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except Exception as e:
                self.logger.error(e)

    def get_url_filename(self, url):
        return url.split('/')[-1]

    def save_iamge(self, content, path):
        with open(path, 'wb') as fp:
            fp.write(content)

    def get(self, url, _json=False, binary=False, retry=5):

        start = 0
        while start < retry:

            try:
                r = requests.get(
                    url=url,
                    params=self.params,
                    headers=self.headers,
                    cookies=self.cookies)

            except Exception as e:
                self.logger.error('base class error '.format(e))
                start += 1
                continue

            else:
                if _json:
                    result = r.json()
                elif binary:
                    result = r.content
                else:
                    r.encoding='utf8'
                    result = r.text
                return result

        return None

    def post(self, url, post_data, _json=False, binary=False, retry=5):

        start = 0
        while start < retry:

            try:
                r = requests.post(
                    url=url,
                    headers=self.headers,
                    data=post_data
                )

            except Exception as e:
                print(e)
                start += 1
                continue

            else:

                if _json:
                    r.encoding='utf8'
                    result = r.json()
                elif binary:
                    result = r.content
                else:

                    result = r.text
                return result

        return None

    @property
    def headers(self):
        raise NotImplemented

    def parse(self, content):
        '''
        页面解析
        '''
        response = parsel.Selector(text=content)

        return response

    def process(self, data, history=False):
        '''
        数据存储
        '''
        pass
    def time_str(self,x):
        return x.strftime('%Y-%m-%d')

    def trading_time(self):
        '''
        判定时候交易时间 0 为交易时间， 1和-1为非交易时间
        :return:
        '''
        TRADING = 0
        MORNING_STOP = -1
        AFTERNOON_STOP = 1
        NOON_STOP=-1
        current = datetime.datetime.now()
        year, month, day = current.year, current.month, current.day
        start = datetime.datetime(year, month, day, 9, 23, 0)
        noon_start = datetime.datetime(year, month, day, 12, 58, 0)

        morning_end = datetime.datetime(year, month, day, 11, 31, 0)
        end = datetime.datetime(year, month, day, 15, 2, 5)

        if current > start and current < morning_end:
            return TRADING

        elif current > noon_start and current < end:
            return TRADING

        elif current > end:
            return AFTERNOON_STOP

        elif current < start:
            return MORNING_STOP

        else:
            return NOON_STOP

    def notify(self, title):
        send_message_via_wechat(title)
