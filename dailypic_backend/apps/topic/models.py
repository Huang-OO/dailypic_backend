from django.db import models
from dailypic_backend.utils.BaseModel import BaseModel


class Topic(BaseModel):
    text = models.TextField(null=True,
                            verbose_name='吐槽')

    objects = models.Manager()

    class Meta:
        db_table = 'tb_topic'
        verbose_name = '吐槽'
        verbose_name_plural = verbose_name