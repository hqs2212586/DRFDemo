# -*- coding:utf-8 -*-
__author__ = 'Qiushi Huang'

import time
from rest_framework.throttling import BaseThrottle

VISIT_RECORD = {}

class MyThrottle(BaseThrottle):

    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        # 实现限流的逻辑
        # 以ip地址限流：要求访问站点的频率一分钟不超过3次
        # 访问列表  {ip: [time1,time2,time3]}
        # 1、获取请求的ip地址
        remote_ip = request.META.get("REMOTE_ADDR")
        ctime = time.time()
        # 2、判断ip地址是否在访问列表
        if remote_ip not in VISIT_RECORD:
            # 2.1 不在，给访问列表添加key,value
            VISIT_RECORD[remote_ip] = [ctime, ]
            return True

        # 2.2 在，需要获取该ip的访问记录，把当前时间加入列表
        history = VISIT_RECORD.get(remote_ip)    # 取到列表

        # 3、确保列表里最新访问即最老访问的时间差 是1分钟
        while history and history[0] - history[-1] > 60:
            history.pop()               # 删最后一个
        self.history = history
        # 4、得到列表的长度，判断是否是允许的次数
        if len(history) < 3:
            # 未达到频率限制
            history.insert(0, ctime)    # 加到第一个
            return True
        else:
            return False

    def wait(self):
        # 返回还剩多久可继续访问
        ctime = 60 - (self.history[0] - self.history[-1])    # 最新的时间减去最老的时间(可能是已经删除的时间)
        return ctime