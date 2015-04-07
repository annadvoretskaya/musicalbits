# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20150405_1238'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=True, max_length=200, null=True, blank=True)),
                ('audio', models.ForeignKey(related_name='tags', default=True, blank=True, to='main.Audio', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='teg',
            name='audio',
        ),
        migrations.DeleteModel(
            name='Teg',
        ),
        migrations.AlterField(
            model_name='playlist',
            name='audio',
            field=models.ManyToManyField(default=None, to='main.Audio', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='playlist',
            name='description',
            field=models.TextField(default=True, max_length=2000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
