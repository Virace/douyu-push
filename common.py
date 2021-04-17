# -*- coding: utf-8 -*-
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @Site    : x-item.com
# @Software: PyCharm
# @Create  : 2021/4/16 14:54
# @Update  : 2021/4/17 17:43
# @Detail  : 

import logging
import time

import requests

log = logging.getLogger(__name__)


def check_time(func):
    """
    获取函数执行时间
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        st = time.time()
        ret = func(*args)
        log.debug(
            f'[Time Monitoring]: Func: {func.__module__}.{func.__name__}, Time Spent: {round(time.time() - st, 2)}')
        return ret

    return wrapper


def func_retry(func, __max_retries=5, __exception=Exception, **kwargs):
    assert func, '不能为空'
    _retry = 0
    while True:
        try:
            data = func(**kwargs)
        except __exception as e:
            log.debug(f'[Retry]: Func: {func.__module__}.{func.__name__}, Number Of Retries: {_retry},  Error: {str(e)}')
            _retry += 1
        else:
            return data

        if _retry >= __max_retries:
            raise Exception(f'超过最大重试次数: {__max_retries}.')


class Request:
    """
    不使用session
    简单封装一个重试请求
    可以用任何异常触发
    """

    def __init__(self, max_retries=5, exception=Exception):
        self.max_retries = max_retries
        self.exception = exception

    def get(self, url, params=None, **kwargs):
        return func_retry(requests.get, self.max_retries, self.exception, url=url, params=params, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return func_retry(requests.post, self.max_retries, self.exception, url=url, data=data, json=json, **kwargs)
