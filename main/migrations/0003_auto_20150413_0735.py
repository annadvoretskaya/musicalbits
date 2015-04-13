# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150412_1240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='audio',
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
        migrations.AddField(
            model_name='audio',
            name='genre',
            field=models.CharField(default=None, max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
