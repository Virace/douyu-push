# -*- coding: utf-8 -*-
# @Time    : 2021/2/19 18:21
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @Site    : x-item.com
# @Software: PyCharm
# @Detail  : 推送相关

import requests
import logging
from typing import Union
from dataclasses import dataclass

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


@dataclass
class Message:
    title: str
    content: str

    def to_str(self):
        return f'{self.title}\n{self.content}'

    def to_dict(self):
        return dict(title=self.title, content=self.content)


def push_plus(token, msg: Union[str, Message], topic='', template='html'):
    """
    push+推送 官网: https://pushplus.hxtrip.com/
    :param token: 推送token
    :param msg: 消息
    :param topic: 推送群组ID(一对多推送时使用)
    :param template: json/html
    :return:
    """
    url = f'https://pushplus.hxtrip.com/send'
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

    response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    log.debug(response.json())


def cool_push(token, msg: Union[str, Message], _type: int = 0, extra: str = None):
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
    response = requests.post(url, data=data.encode('utf-8'), headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    log.debug(response.json())


if __name__ == '__main__':
    cool_push('799feb4ed90b45ea4147a043934fe2dd', Message('标题', '内容'))
