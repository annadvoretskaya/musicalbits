# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20150401_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='path',
            field=models.CharField(default=True, max_length=1000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
