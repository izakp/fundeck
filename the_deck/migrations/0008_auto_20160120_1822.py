# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_deck', '0007_auto_20160120_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='remote_files',
            field=models.ManyToManyField(to='the_deck.RemoteFile', null=True, blank=True),
        ),
    ]
