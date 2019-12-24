# -*- coding:utf-8 -*-
__author__ = 'Qiushi Huang'

from rest_framework import versioning

class MyVersion:
    def determine_version(self, request, *args, **kwargs):
        # 该方法返回值给了 request.version
        # 返回版本号
        # 版本号携带在过滤条件中  xxx?version=v1
        version = request.query_params.get("version", "v1")
        return version