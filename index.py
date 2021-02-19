# -*- coding: utf-8 -*-
# @Time    : 2021/2/19 2:13
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @Site    : x-item.com
# @Software: PyCharm
# @Detail  : 斗鱼订阅推送

import time
import requests
import logging
from typing import Union

from database import get_time, update_time
from config import PUSH_PLUS_TOKEN

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


def notification_push(title: str, msg: Union[str, dict], topic='', template='html'):
    """
    push+推送 官网: https://pushplus.hxtrip.com/
    :param title: 标题
    :param msg: 消息
    :param topic: 推送群组ID(一对多推送时使用)
    :param template: json/html
    :return:
    """
    url = f'https://pushplus.hxtrip.com/send'
    data = {'token': PUSH_PLUS_TOKEN,
            'title': title,
            'content': msg,
            'topic': topic,
            "template": template}
    response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    log.debug(response.json())


def get_status(rid: str) -> tuple:
    """
    通过斗鱼 网页端/安卓端 搜索接口获取直播间状态
    :param rid: 直播间ID
    :return: 返回元组格式(状态, 源)
    """
    # url = f'https://www.douyu.com/japi/search/api/getSearchRec?kw={rid}'
    url = f'https://apiv2.douyucdn.cn/japi/search/api/getSearchRec?kw={rid}&tagTest=a&client_sys=android'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()['data']
    log.debug(data)
    for item in data['recList']:
        item = item['roomInfo']
        if item['rid'] == int(rid):
            return item['isLive'] == 1, item


def monitor_and_notify(rid: str, push_id=''):
    """
    监测并推送
    :param rid: 直播间ID
    :param push_id: push+ 推送群组ID
    :return:
    """
    status, data = get_status(rid)
    log.info(f'{rid} 直播状态: {status}')
    lst = time.strftime("%Y年%m月%d日 %H点%M分%S秒", time.localtime(data["lastShowTime"]))

    if status:
        try:
            old = get_time()
            if old == data["lastShowTime"]:
                return

            else:
                update_time(data["lastShowTime"])
        except Exception as e:
            log.warning(e)
            return
        else:
            notification_push(
                f'您关注的主播 {data["nickName"]} 正在直播!',
                f'最后开播时间: {lst}<br>'
                f'<img src={data["avatar"]}>',
                push_id
            )


def main_handler(event, context):
    if event and 'Message' in event:
        data = event['Message'].split(',')
        assert len(data) == 2, '触发器格式不正确'
        monitor_and_notify(data[0], data[1])

