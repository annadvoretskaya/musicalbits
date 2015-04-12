# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='audioconnection',
            options={'ordering': ('number',)},
        ),
        migrations.AddField(
            model_name='playlist',
            name='description_html',
            field=models.TextField(default=None, editable=False),
            preserve_default=False,
        ),
    ]
