# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_audio_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='user',
            field=models.ForeignKey(related_name='audio', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
