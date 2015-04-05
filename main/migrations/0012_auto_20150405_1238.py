# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_playlist_song'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=True, max_length=50, null=True, blank=True)),
                ('audio', models.ForeignKey(related_name='genres', default=True, blank=True, to='main.Audio', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Teg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=True, max_length=200, null=True, blank=True)),
                ('audio', models.ForeignKey(related_name='tegs', default=True, blank=True, to='main.Audio', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='playlist',
            name='song',
        ),
        migrations.AddField(
            model_name='playlist',
            name='audio',
            field=models.ManyToManyField(default=None, related_name='audios', null=True, to='main.Audio', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='like',
            name='playlist',
            field=models.ForeignKey(related_name='likes', default=None, blank=True, to='main.Playlist', null=True),
            preserve_default=True,
        ),
    ]
