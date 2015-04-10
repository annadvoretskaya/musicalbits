# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='last_updated',
            field=models.DateTimeField(default=None, auto_now=True),
            preserve_default=True,
        ),
    ]
