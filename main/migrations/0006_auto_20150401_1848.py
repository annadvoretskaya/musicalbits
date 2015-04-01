# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_audio_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='author',
            field=models.CharField(default=True, max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='audio',
            name='name',
            field=models.CharField(default=True, max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
