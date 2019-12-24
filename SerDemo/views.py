from django.shortcuts import render
from django.views import View          # CBV：在视图里使用类处理请求
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Book, Publisher
import json


# 方式一：用.vlues 和 JsonResponse 实现序列化
# class BookView(View):
#     """
#     要返给前端的数据类型为json,要注意json不能直接将querySet序列化
#     """
#     def get(self, request):
#         # values(*field): 得到的不是对象，而是一个可迭代的字段序列
#         book_list = Book.objects.values('id', 'title', 'pub_time', 'publisher')   # book编码、标题、出版时间、出版社
#         # 将QuerySet对象转化为数组套字典
#         book_list = list(book_list)
#         ret = []
#         for book in book_list:   # 拼接处理foreignkey字段
#             publisher_id = book['publisher']
#             publisher_obj = Publisher.objects.filter(id=publisher_id).first()   # 拿到出版社对象
#             book['publisher'] = {
#                 'id': publisher_id,
#                 'title': publisher_obj.title
#             }
#             ret.append(book)
#
#         return JsonResponse(
#             ret,
#             safe=False,    # 要序列化非 dict 对象，必须设置 safe 参数为 False
#             json_dumps_params={"ensure_ascii": False}
#         )
"""
页面显示的数据列表如下所示：
[
    {
        id: 1,
        title: "python开发",
        pub_time: "2011-08-27",
        publisher: {
            id: 1,
            title: "人民日报社"
        }
    },
    ...
]
"""

# 方式二：基于django的序列化组件 serializers
# class BookView(View):
#     def get(self, request):
#         book_list = Book.objects.all()
#         ret = serializers.serialize('json', book_list)
#         return HttpResponse(ret)
"""
页面显示的序列化结果：
[
    {
        model: "SerDemo.book",
        pk: 1,
        fields: {
            title: "python开发",
            category: 1,
            pub_time: "2011-08-27",
            publisher: 1,
            author: [ ]
        }
    },
    ...
]
"""

# 方式三：基于rest_framework框架实现序列化（pip install djangorestframework）
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BookSerializer   # 自定义序列化类


# class BookView(APIView):
#     query_set = Book.objects.all()        # 将query_set抽离
#     serializer_class = BookSerializer     # 拿到序列化器
#
#     def get(self, request):
#         # 第一个图书对象
#         # book_obj = Book.objects.first()
#         # ret = BookSerializer(book_obj)
#
#         # book_list = Book.objects.all()
#         book_list = self.query_set
#         # ret = BookSerializer(book_list, many=True)    # 使用序列化器序列化
#         ret = self.serializer_class(book_list, many=True)
#         """
#         序列化的数据保存在ret.data中
#         """
#         return Response(ret.data)
#     """
#     得出来的结果会使用Django REST framework模板，在serializers.py中定制好序列化类后，显示效果如下所示：
#     HTTP 200 OK
#     Allow: GET, HEAD, OPTIONS
#     Content-Type: application/json
#     Vary: Accept
#
#     [
#         {
#             "id": 1,
#             "title": "python开发",
#             "category": "Python",
#             "pub_time": "2011-08-27",
#             "publisher": {
#                 "id": 1,
#                 "title": "人民日报社"
#             },
#             "author": [
#                 {
#                     "id": 1,
#                     "name": "朱荣"
#                 },
#                 {
#                     "id": 2,
#                     "name": "黄秋实"
#                 }
#             ]
#         },
#         {
#             "id": 2,
#             "title": "go开发",
#             "category": "Go",
#             "pub_time": "2015-09-30",
#             "publisher": {
#                 "id": 2,
#                 "title": "湖北日报社"
#             },
#             "author": [
#                 {
#                     "id": 2,
#                     "name": "黄秋实"
#                 }
#             ]
#         },
#         {
#             "id": 3,
#             "title": "Linux开发",
#             "category": "Linux",
#             "pub_time": "2008-08-27",
#             "publisher": {
#                 "id": 3,
#                 "title": "长江日报设"
#             },
#             "author": [
#                 {
#                     "id": 1,
#                     "name": "朱荣"
#                 },
#                 {
#                     "id": 3,
#                     "name": "朱芳"
#                 }
#             ]
#         }
#     ]
#     """
#
#     def post(self, request):
#         print(request.data)
#         serializer = BookSerializer(data=request.data)  # 序列化器校验前端传回来的数据
#         if serializer.is_valid():
#             serializer.save()   # 验证成功后保存数据库
#             # 因为ModelSerializer的create方法不支持source的用法。因此必须还自定义一个create方法。
#             return Response(serializer.validated_data)   # validated_data存放验证通过的数据
#         else:
#             return Response(serializer.errors)           # errors存放错误信息
#
#     '''
#     发送post请求接口设计
#     POST /books/list
#     {
#         "title": "nodejs的使用教程",
#         "w_category": "1",
#         "pub_time": "2018-10-27",
#         "publisher_id": 1,
#         "author_list": [1,2,3]
#     }
#     '''


# class BookEditView(APIView):
#     def get(self, request, id):
#         """查看单条数据"""
#         book_obj = Book.objects.filter(id=id).first()
#         ret = BookSerializer(book_obj)
#         return Response(ret.data)
#
#     '''
#     GET /books/retrieve/3
#     {
#         "id": 3,
#         "title": "Linux开发",
#         "category": "Linux",
#         "pub_time": "2008-08-27",
#         "publisher": {
#             "id": 3,
#             "title": "长江日报社"
#         },
#         "author": [
#             {
#                 "id": 1,
#                 "name": "阿萨德"
#             },
#             {
#                 "id": 3,
#                 "name": "阿斯达"
#             }
#         ]
#     }
#     '''
#
#     def put(self, request, id):
#         """更新操作"""
#         book_obj = Book.objects.filter(id=id).first()
#         serializer = BookSerializer(
#             book_obj,             # 待更新对象
#             data=request.data,    # 要更新的数据
#             partial=True          # 重点：进行部分验证和更新
#         )
#         if serializer.is_valid():
#             serializer.save()     # 保存
#             return Response(serializer.validated_data)   # 返回验证通过的数据
#             # return Response(serializers.data)    # 返回所有数据
#         else:
#             return Response(serializer.errors)      # 返回验证错误的数据
#
#     def delete(self, request, id):
#         """删除操作"""
#         book_obj = Book.objects.filter(id=id).first()
#         book_obj.delete()
#         return Response("")


"""升级：改写使用通用类，继承通用方法"""
# class GenericAPIView(APIView):
#     # 通用APIView模板类
#     query_set = None
#     serializer_class = None
#
#     def get_queryset(self):
#         return self.query_set
#
#     def get_serializer(self, *args, **kwargs):
#         return self.serializer_class(*args, **kwargs)   # 实例化,且接收所有的参数
#
#
# class BookView(GenericAPIView):
#     # 以方法的形式调用获取
#     query_set = Book.objects.all()
#     serializer_class = BookSerializer
#
#     def get(self, request):
#         book_list = self.get_queryset()
#         ret = self.get_serializer(book_list, many=True)
#         return Response(ret.data)
#
#     def post(self, request):
#         serializer = BookSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


"""再次升级mixins类改写视图"""
class GenericAPIView(APIView):
    # 通用APIView模板类
    query_set = None
    serializer_class = None

    def get_queryset(self):
        return self.query_set

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)   # 实例化,且接收所有的参数


class ListModelMixin(object):
    def list(self, request):
        queryset = self.get_queryset()
        ret = self.get_serializer(queryset, many=True)
        return Response(ret.data)


class CreateModelMixin(object):
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RetrieveModelMixin(object):
    def retrieve(self, request, id):   # 查看单条数据
        book_obj = self.get_queryset().filter(id=id).first()
        ret = self.get_serializer(book_obj)
        return Response(ret.data)


class UpdateModelMixin(object):
    def update(self, request, id):
        book_obj = self.get_queryset().filter(id=id).first()
        serializer = self.get_serializer(
            book_obj,  # 待更新对象
            data=request.data,  # 要更新的数据
            partial=True  # 重点：进行部分验证和更新
        )
        if serializer.is_valid():
            serializer.save()  # 保存
            return Response(serializer.validated_data)  # 返回验证通过的数据
            # return Response(serializers.data)    # 返回所有数据
        else:
            return Response(serializer.errors)  # 返回验证错误的数据


class DestroyModelMixin(object):
    def delete(self, request, id):
        book_obj = self.get_queryset().filter(id=id).first()
        book_obj.delete()
        return Response("")


# 二层封装
class ListCreateAPIView(GenericAPIView, ListModelMixin, CreateModelMixin):
    pass


class RetrieveUpdateDestroyAPIView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    pass


# class BookView(GenericAPIView, ListModelMixin, CreateModelMixin):   # 一层封装
class BookView(ListCreateAPIView):          # 使用二层封装
    query_set = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


# class BookEditView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):  # 一层封装
class BookEditView(RetrieveUpdateDestroyAPIView):     # 使用二层封装
    query_set = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, id):
        """查看单条数据"""
        return self.retrieve(request, id)

    def put(self, request, id):
        """更新操作"""
        return self.update(request, id)

    def delete(self, request, id):
        """删除操作"""
        return self.destroy(request, id)


from rest_framework.viewsets import ViewSetMixin

# class ModelViewSet(ViewSetMixin, GenericAPIView, ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
#     pass

from rest_framework.viewsets import ModelViewSet   # 使用框架

class BookModelViewSet(ModelViewSet):
    query_set = Book.objects.all()
    serializer_class = BookSerializer



from rest_framework import views       # APIView
from rest_framework import generics    # 公共通用视图类：GenericAPIView，及各种组合视图类CreateAPIView、ListAPIView、RetrieveAPIView等
from rest_framework import mixins      # 混合继承类：CreateModelMixin、ListModelMixin、RetrieveModelMixin、UpdateModelMixin、DestroyModelMixin
from rest_framework import viewsets    # 重写as_view: ViewSetMixin;其他类都是帮助去继承ViewSetMixin


from rest_framework import versioning
