# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20150405_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='song',
            field=models.ManyToManyField(default=None, related_name='songs', null=True, to='main.Audio', blank=True),
            preserve_default=True,
        ),
    ]
