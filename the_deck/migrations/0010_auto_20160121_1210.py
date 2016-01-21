# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_deck', '0009_auto_20160120_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='sshuser',
            name='name',
            field=models.CharField(default='User', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='command',
            name='remote_files',
            field=models.ManyToManyField(to='the_deck.RemoteFile', blank=True),
        ),
        migrations.AlterField(
            model_name='remotefile',
            name='filename',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='sshuser',
            name='username',
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name='taskgroup',
            name='chef_inventories',
            field=models.ManyToManyField(to='the_deck.ChefInventory', blank=True),
        ),
        migrations.AlterField(
            model_name='taskgroup',
            name='hosts',
            field=models.ManyToManyField(to='the_deck.Host', blank=True),
        ),
    ]
