# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_deck', '0012_auto_20160129_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskrunner',
            name='state',
            field=models.IntegerField(default=0, choices=[(0, b'CREATED'), (100, b'PENDING'), (300, b'CONNECTIONS_ESTABLISHED'), (400, b'ASSETS_PREPARED'), (500, b'COMMANDS_RUN'), (600, b'COMPLETE'), (700, b'FAILED'), (800, b'SUCCEEDED')]),
        ),
    ]
