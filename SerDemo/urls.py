from django.urls import path, include
from .views import BookView, BookEditView, BookModelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()   # 路由实例化

# 第一个参数是路由匹配规则，这里的路由是分发下来的，因此可以不做设置；第二个参数是视图
router.register(r"$", BookModelViewSet, basename='codes')


urlpatterns = [
    # path('list', BookView.as_view()),   # 查看所有的图书
    # 注意url中参数命名方式，2.0之前的写法：'retrieve/(?P<id>\d+)'
    # 2.0之后的写法：<>内声明类型，冒号后面跟着关键字参数
    # path('retrieve/<int:id>', BookEditView.as_view())   # 单条数据查看

    # path('list', BookModelViewSet.as_view({"get": "list", "post": "create"})),
    # path('retrieve/<int:id>', BookModelViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}))
]

urlpatterns += router.urls    # router.urls是自动生成带参数的路由