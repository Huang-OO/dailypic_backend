# Generated by Django 2.2.5 on 2021-06-05 06:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkImg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('code_status', models.IntegerField(choices=[(1, '使用'), (0, '未使用')], default=1)),
                ('first_category', models.IntegerField(verbose_name='一级分类')),
                ('second_category', models.IntegerField(verbose_name='二级分类')),
                ('url', models.CharField(max_length=255, verbose_name='图片')),
                ('describe', models.TextField(null=True, verbose_name='描述')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '作品',
                'verbose_name_plural': '作品',
                'db_table': 'tb_work_imgs',
            },
        ),
    ]
