# -*- coding:utf-8 -*-
__author__ = 'Qiushi Huang'

from rest_framework.permissions import BasePermission


class MyPermission(BasePermission):
    message = "您没有权限"

    def has_permission(self, request, view):
        # 判断用户是否有权限
        user_obj = request.user

        # 普通用户
        if user_obj.type == 3:
            return False
        else:
            return True




