# -*- coding:utf-8 -*-
__author__ = 'Qiushi Huang'

# 针对models设计和声明序列化类
from rest_framework import serializers
from .models import Book, Publisher


class PublisherSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=32)


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=32)


def my_validate(value):
    # 自定义验证器
    if "fuck" in value.lower():
        raise serializers.ValidationError("不能含有敏感信息")
    else:
        return value

"""
class BookSerializer(serializers.Serializer):
    '''Book序列化类，注意与models对应'''
    id = serializers.IntegerField(required=False)   # required=False设置该字段无需校验
    title = serializers.CharField(max_length=32, validators=[my_validate])   # 添加自定义验证器

    # ChoiceField字段处理
    CHOICES = ((1, "Python"), (2, "Go"), (3, "Linux"))
    # choice字段配置source参数，显示对应名，read_only设置只读，只在序列化时使用
    category = serializers.ChoiceField(choices=CHOICES, source='get_category_display', read_only=True)  # 图书的类别
    # write_only设置只写，只反序列化时使用
    w_category = serializers.ChoiceField(choices=CHOICES, write_only=True)

    pub_time = serializers.DateField( )

    # 当序列化与反序列化的类型不同时，需要分别生成read_only和write_only两个字段
    # 外键字段处理
    publisher = PublisherSerializer(read_only=True)
    publisher_id = serializers.IntegerField(write_only=True)

    # 多对多字段处理（通过many字段与ForeignKey区分）
    author = AuthorSerializer(many=True, read_only=True)
    author_list = serializers.ListField(write_only=True)

    def create(self, validated_data):
        # 重写save中的create方法
        book_obj = Book.objects.create(
            title = validated_data['title'],
            category=validated_data['w_category'],   # 注意取反序列化字段
            pub_time=validated_data['pub_time'],
            publisher_id=validated_data['publisher_id']
        )
        book_obj.author.add(*validated_data['author_list'])   # 添加多对多
        return book_obj

    def update(self, instance, validated_data):
        # 判断对应项是否更新，如果更新则替换
        instance.title = validated_data.get('title', instance.title)
        instance.category = validated_data.get('category', instance.category)
        instance.pub_time = validated_data.get('pub_time', instance.pub_time)
        instance.publisher_id = validated_data.get('publisher_id', instance.publisher_id)

        if validated_data.get("author_list"):
            instance.author.set(validated_data["author_list"])
        instance.save()   # 保存
        return instance

    def validated_title(self, value):     # 对字段进行验证：校验title字段
        if "python" not in value.lower():    # 如果python不在value字段中
            raise serializers.ValidationError("标题必须含有python")     # 自定义错误信息
        return value

    def validate(self, attrs):   # 对多个字段进行比较验证
        # 执行更新操作：{"w_category": 1,"publisher_id": 1}
        # 注意JSON中，标准语法中，不支持单引号，属性或者属性值，都必须是双引号括起来
        if attrs['w_category'] == 1 and attrs['publisher_id'] == 1:     # 联合校验分类和标题
            return attrs
        else:
            raise serializers.ValidationError('分类以及出版社不符合要求')   # 抛出异常
"""

class BookSerializer(serializers.ModelSerializer):
    # SerializerMethodField的使用,获取显示外联字段
    category_display = serializers.SerializerMethodField(read_only=True)   # 重新定义，避免重写，影响反序列化
    publisher_info = serializers.SerializerMethodField(read_only=True)
    authors = serializers.SerializerMethodField(read_only=True)

    def get_category_display(self, obj):
        return obj.get_category_display()  # ORM方法获取中文

    def get_authors(self, obj):
        authors_query_set = obj.author.all()   # 拿到所有作者信息
        return [
            {"id": authors_obj.id, "name": authors_obj.name} for authors_obj in authors_query_set]   # 列表推导式

    def get_publisher_info(self, obj):
        # obj是我们序列化的每个Book对象
        publisher_obj = obj.publisher   # 正向查询
        return {'id': publisher_obj.id}

    class Meta:
        model = Book         # 与Book表对应
        fields = "__all__"
        extra_kwargs = {
            "category": {"write_only": True},   # 避免直接改写
            "publisher": {"write_only": True},
            "author": {"write_only": True}
        }