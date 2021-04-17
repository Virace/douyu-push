# -*- coding: utf-8 -*-
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @Site    : x-item.com
# @Software: PyCharm
# @Create  : 2021/2/19 2:13
# @Update  : 2021/4/16 15:37
# @Detail  : 

import leancloud
from common import func_retry, check_time


class Flag:

    @check_time
    def __init__(self, app_id, app_key):
        leancloud.init(app_id, app_key)

        self.Douyu = leancloud.Object.extend('douyu')
        self.query = self.Douyu.query

    @check_time
    def get_time(self, oid):
        item = func_retry(self.query.get, object_id=oid)
        return item.get('time')

    @check_time
    def update_time(self, oid, data):
        todo = self.Douyu.create_without_data(oid)
        todo.set('time', data)
        func_retry(todo.save)
