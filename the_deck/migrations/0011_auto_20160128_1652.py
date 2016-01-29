# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_deck', '0010_auto_20160121_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='state',
            field=models.IntegerField(default=0, choices=[(0, b'CREATED'), (100, b'ESTABLISHING_CONNECTION'), (150, b'CONNECTION_ESTABLISHED'), (200, b'PREPARING_ASSETS'), (250, b'ASSETS_PREPARED'), (300, b'RUNNING_COMMAND'), (350, b'COMMAND_RUN'), (400, b'CLEANING_UP'), (500, b'COMPLETE'), (600, b'FAILED'), (700, b'SUCCEEDED')]),
        ),
    ]
