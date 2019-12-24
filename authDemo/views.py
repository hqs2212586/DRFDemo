# -*- coding:utf-8 -*-
__author__ = 'Qiushi Huang'

import uuid      # UUID对象和生成函数
from .models import User
from utils.auth import MyAuth    # 认证
from utils.permission import MyPermission    # 权限
from utils.throttle import MyThrottle        # 频率
# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response


class DemoView(APIView):
    def get(self, request):
        return Response("认证demo~")


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        pwd = request.data.get("pwd")
        # 登录成功，生成token会将token给你返回
        token = uuid.uuid4()   # 通过随机数来生成UUID
        User.objects.create(username=username, pwd=pwd, token=token)
        return Response("创建用户成功")


class TestView(APIView):
    authentication_classes = [MyAuth, ]    # 局部认证
    # permission_classes = [MyPermission, ]  # 局部权限
    throttle_classes = [MyThrottle, ]

    def get(self, request):
        # 访问：GET /auth/test?token=98bc3edce82143f8ad638f9cad336807
        print(request.user)     # User object (1)
        print(request.auth)     # 98bc3edce82143f8ad638f9cad336807
        return Response("认证测试")