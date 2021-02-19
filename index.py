# -*- coding: utf-8 -*-
# @Time    : 2021/2/19 2:13
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @Site    : x-item.com
# @Software: PyCharm
# @Detail  : 斗鱼订阅推送

import os
import json
import time
import requests
import logging

from database import Flag

from push import push_plus, cool_push, Message

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

LEANCLOUD_APP_ID = os.environ.get('LEANCLOUD_APP_ID')
LEANCLOUD_APP_KEY = os.environ.get('LEANCLOUD_APP_KEY')
LEANCLOUD_OID = os.environ.get('LEANCLOUD_OID')
assert LEANCLOUD_APP_ID, 'LEANCLOUD_APP_ID不能为空'
assert LEANCLOUD_APP_KEY, 'LEANCLOUD_APP_KEY不能为空'
assert LEANCLOUD_OID, 'LEANCLOUD_OID不能为空'

flag = Flag(LEANCLOUD_APP_ID, LEANCLOUD_APP_KEY, LEANCLOUD_OID)


def notification_push(msg: Message, extra: dict = None):
    """
    消息推送
    :param msg: 消息主题
    :param extra: 额外参数:
    {
        # push+ 群组推送ID
        "push_plus_topic": '',
        # push+ 推送模板
        "push_plus_template": '',

        # coolpush 推送类型(私人推送或群组推送)
        "cool_push_type": '',
        # coolpush 指定推送ID, userId/groupId
        "cool_push_specific": ''
    }
    :return:
    """
    if extra is None:
        extra = {}

    push_plus_token = os.environ.get('PUSH_PLUS_TOKEN')
    cool_push_token = os.environ.get('COOL_PUSH_TOKEN')

    if push_plus_token:
        push_plus(
            push_plus_token,
            msg,
            topic=extra.get('push_plus_topic', ''),
            template=extra.get('push_plus_template', 'html')
        )

    elif cool_push_token:
        cool_push(
            push_plus_token,
            msg,
            _type=extra.get('cool_push_type', 0),
            extra=extra.get('cool_push_specific', None))

    else:
        raise Exception('未提供任何推送token')


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
    else:
        return None, None


def monitor_and_notify(rid: str, extra: dict = None):
    """
    监测并推送
    :param rid: 直播间ID
    :param extra: 额外参数
    :return:
    """
    status, data = get_status(rid)
    log.info(f'{rid} 直播状态: {status}')
    lst = time.strftime("%Y年%m月%d日 %H点%M分%S秒", time.localtime(data["lastShowTime"]))

    if status:
        try:
            old = flag.get_time()
            if old == data["lastShowTime"]:
                return

            else:
                flag.update_time(data["lastShowTime"])
        except Exception as e:
            log.warning(e)
            return
        else:
            notification_push(
                Message(title=f'您关注的主播 {data["nickName"]} 正在直播!',
                        content=f'最后开播时间: {lst}<br>'
                                f'<img src={data["avatar"]}>'),
                extra
            )


def main_handler(event, context):
    """
    云函数调用函数
    :param event:
    :param context:
    :return:
    """
    if event and 'Message' in event:
        try:
            data = json.loads(event['Message'].strip())
        except Exception as e:
            raise Exception('触发器格式不正确', e)
        else:
            for item in data.items():
                monitor_and_notify(item[0], item[1])
    else:
        raise Exception('请配置触发器参数')


if __name__ == '__main__':
    monitor_and_notify('71415', dict(
        push_plus_topic='71415',
        cool_push_type='1'
    ))
