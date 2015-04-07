# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20150405_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='like',
            name='playlist',
            field=models.ForeignKey(related_name='likes', default=None, to='main.Playlist'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(related_name='likes', default=None, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='playlist',
            name='description',
            field=models.TextField(default=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='playlist',
            name='name',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
    ]
