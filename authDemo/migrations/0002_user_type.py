# Generated by Django 2.2.1 on 2019-12-23 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authDemo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.IntegerField(choices=[(1, 'vip'), (2, 'vvip'), (3, '普通用户')], default=3),
        ),
    ]
