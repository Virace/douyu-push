# -*- coding: utf-8 -*-
# @Time    : 2021/2/19 2:13
# @Author  : Virace
# @Email   : Virace@aliyun.com
# @Site    : x-item.com
# @Software: PyCharm
# @Detail  :
import leancloud


class Flag:

    def __init__(self, app_id, app_key, oid):
        leancloud.init(app_id, app_key)

        self.Douyu = leancloud.Object.extend('douyu')
        self.query = self.Douyu.query
        self.oid = oid

    def get_time(self):
        item = self.query.get(self.oid)
        return item.get('time')

    def update_time(self, data):
        todo = self.Douyu.create_without_data(self.oid)
        todo.set('time', data)
        todo.save()
