# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20150401_1848'),
    ]

    operations = [
        migrations.RenameField(
            model_name='audio',
            old_name='name',
            new_name='artist',
        ),
    ]
