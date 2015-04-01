# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20150401_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='title',
            field=models.CharField(default=True, max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
