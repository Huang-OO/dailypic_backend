# Generated by Django 2.2.5 on 2021-06-03 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sign',
            field=models.CharField(max_length=255, null=True, verbose_name='个性签名'),
        ),
    ]
