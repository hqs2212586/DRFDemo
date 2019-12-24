# -*- coding:utf-8 -*-
__author__ = 'Qiushi Huang'
from rest_framework.exceptions import AuthenticationFailed
from authDemo.models import User
from rest_framework.authentication import BaseAuthentication   # 基础认证类


# class MyAuth(object):   # 不能继承object
class MyAuth(BaseAuthentication):     # 继承基础认证类
    def authenticate(self, request):
        # 做认证 看他是否登录
        # 从url过滤条件里拿到token
        # 去数据库看token是否合法
        # 合法的token能够获取用户信息
        token = request.query_params.get("token", "")   # 拿不到为空字符串
        if not token:
            raise AuthenticationFailed("没有携带token")   # 抛出异常信息
        user_obj = User.objects.filter(token=token).first()
        if not user_obj:
            raise AuthenticationFailed("token不合法")

        return (user_obj, token)      # 返回元组赋值给(request.user,request.auth)
