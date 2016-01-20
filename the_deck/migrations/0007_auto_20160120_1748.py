# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_deck', '0006_auto_20160119_1744'),
    ]

    operations = [
        migrations.CreateModel(
            name='RemoteFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('filename', models.CharField(unique=True, max_length=128)),
                ('content', models.TextField()),
                ('permissions', models.CharField(default=b'0644', max_length=4)),
            ],
        ),
        migrations.AddField(
            model_name='command',
            name='remote_files',
            field=models.ManyToManyField(to='the_deck.RemoteFile'),
        ),
    ]
