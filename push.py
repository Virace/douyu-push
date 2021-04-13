# -*- coding: utf-8 -*-
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @Site    : x-item.com
# @Software: PyCharm
# @Create  : 2021/2/19 18:21
# @Update  : 2021/4/13 18:33
# @Detail  : 推送相关

import logging
from typing import Union

import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


@dataclass
class Message:
    content: str
    title: str = None

    def to_html(self):
        if self.title:
            return f'{self.title}\n{self.content}'
        else:
            return self.content

    def to_str(self):
        s = self.to_html().replace('<br>', '\n')
        soup = BeautifulSoup(s, 'lxml')
        return soup.get_text().strip('\n')

    def to_dict(self):
        return dict(title=self.title, content=self.content)


def request(max_retries=5, timeout=10):
    """
    requests.post 增加重试(仅对timeout情况重试)
    :param max_retries: 最大重试次数 默认5
    :param timeout: 超时时间 默认10, 单位 秒
    :return: 返回 请求方法, 调用方法与requests.post 一致
    """
    def _request(url, data=None, json=None, **kwargs):
        retry = 0
        while True:
            try:
                response = requests.post(url, data=data, json=json, **kwargs, timeout=timeout)
            except requests.exceptions.ConnectTimeout:
                retry += 1
            else:
                return response
            if retry >= max_retries:
                raise Exception(f'超过最大重试次数: {max_retries}.')

    return _request


def push_plus(token, msg: Union[str, Message], topic='', template='html'):
    """
    push+推送 官网: https://pushplus.hxtrip.com/
    :param token: 推送token
    :param msg: 消息
    :param topic: 推送群组ID(一对多推送时使用)
    :param template: json/html
    :return:
    """
    url = f'https://www.pushplus.plus/send'
    data = {'token': token,
            'topic': topic,
            "template": template}

    if isinstance(msg, Message):
        data.update(msg.to_dict())
    elif isinstance(msg, str):
        data.update(dict(
            title='通知',
            content=msg
        ))
    else:
        raise Exception('msg参数类型错误')

    response = request()(url, json=data, headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    log.debug(response.json())


def cool_push(token, msg: Union[str, Message], _type: int = 0, extra: str = None):
    """
    酷推 推送
    :param token: 推送token
    :param msg: 推送消息
    :param _type: 推送类型, 取值范围0~3,分别对应 私聊/群/私有私聊/私有群
    :param extra: 指定推送参数, QQ号或群号
    :return:
    """
    url_format = {
        0: ('send', lambda x: f'userId={x}' if x else None),
        2: ('psend', lambda x: f'userId={x}' if x else None),
        1: ('group', lambda x: f'groupId={x}' if x else None),
        3: ('pgroup', lambda x: f'groupId={x}' if x else None)
    }

    try:
        path = url_format[_type][0]
        parameter = url_format[_type][1](extra)
    except KeyError:
        raise Exception('_type取值范围0~3')

    if isinstance(msg, Message):
        data = msg.to_str()
    elif isinstance(msg, str):
        data = msg
    else:
        raise Exception('msg参数类型错误')

    url = f'https://push.xuthus.cc/{path}/{token}'
    if parameter:
        url = f'{url}?{parameter}'
    response = request()(url, data=data.encode('utf-8'), headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    log.debug(response.json())


def wxpusher_push(token, msg: Union[str, Message], _type: int = 1, topic_ids: list = None, url: str = None):
    """
    WxPusher 推送
    :param token: 推送token
    :param msg: 消息
    :param _type: 消息类型 对应 data -> contentType
    :param topic_ids: 推送的主题ID
    :param url: 消息提示链接
    :return:
    """
    assert _type in [1, 2, 3], '_type取值范围1~3'
    assert topic_ids, 'topic_ids不能为空, 至少推送一个主题'

    if _type == 1 and isinstance(msg, Message):
        msg = msg.to_str()

    data = {
        "appToken": token,
        "contentType": _type,
        "topicIds": topic_ids,

    }

    if isinstance(msg, Message):
        data.update({
            "content": msg.content,
            "summary": msg.title,
        })
    elif isinstance(msg, str):
        data.update({
            "content": msg,
        })
    else:
        raise Exception('msg参数类型错误')

    if url:
        data.update({
            "url": url
        })

    url = 'http://wxpusher.zjiecode.com/api/send/message'

    response = request()(url, json=data, headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    log.debug(response.json())
