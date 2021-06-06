from django.db import models
from dailypic_backend.utils.BaseModel import BaseModel
from users.models import User


class WorkImg(BaseModel):
    """
    图片模型
    """
    first_category = models.IntegerField(verbose_name='一级分类')
    second_category = models.IntegerField(verbose_name='二级分类')
    user = models.ForeignKey(User,
                             on_delete=models.PROTECT,
                             verbose_name='用户',
                             related_name="users")
    url = models.CharField(max_length=255,
                           verbose_name='图片')
    describe = models.TextField(null=True,
                                verbose_name='描述')

    objects = models.Manager()

    # 对当前表进行相关设置
    class Meta:
        db_table = 'tb_work_imgs'
        verbose_name = '作品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.url


class WorkCollection(BaseModel):
    """
    收藏模型
    """
    user_id = models.IntegerField(verbose_name='收藏者id')
    work = models.ForeignKey(WorkImg,
                             on_delete=models.PROTECT,
                             verbose_name='收藏作品')

    objects = models.Manager()

    # 对当前表进行相关设置
    class Meta:
        db_table = 'tb_work_collections'
        verbose_name = '作品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.work
