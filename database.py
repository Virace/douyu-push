# -*- coding: utf-8 -*-
# @Time    : 2021/2/19 2:13
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @Site    : x-item.com
# @Software: PyCharm
# @Detail  :
import leancloud
from config import LEANCLOUD_APP_ID, LEANCLOUD_APP_KEY, LEANCLOUD_OID


leancloud.init(LEANCLOUD_APP_ID, LEANCLOUD_APP_KEY)

Douyu = leancloud.Object.extend('douyu')
query = Douyu.query


def get_time():
    item = query.get(LEANCLOUD_OID)
    return item.get('time')


def update_time(data):
    todo = Douyu.create_without_data(LEANCLOUD_OID)
    todo.set('time', data)
    todo.save()


if __name__ == '__main__':
    print(get_time())

