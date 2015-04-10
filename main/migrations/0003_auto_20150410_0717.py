# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_audio_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='artist',
            field=models.CharField(default=None, max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='audio',
            name='title',
            field=models.CharField(default=None, max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='genre',
            name='audio',
            field=models.ForeignKey(related_name='genres', default=None, blank=True, to='main.Audio', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='playlist',
            name='description',
            field=models.TextField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tag',
            name='audio',
            field=models.ForeignKey(related_name='tags', default=None, blank=True, to='main.Audio', null=True),
            preserve_default=True,
        ),
    ]
