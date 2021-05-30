from django.db import models


class BaseModel(models.Model):
    """
    模型补充字段
    """
    CODE_STATUS = (
        (1, '使用'),
        (0, '未使用')
    )

    # 创建时间:
    create_time = models.DateTimeField(auto_now=True,
                                       verbose_name='创建时间')
    # 更新时间
    update_time = models.DateTimeField(auto_now=True,
                                       verbose_name='更新时间')
    # 是否使用
    code_status = models.IntegerField(default=1, choices=CODE_STATUS)

    class Meta:
        # 说明是抽象类(抽象类不会创建表)
        abstract = True
