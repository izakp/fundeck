# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_deck', '0011_auto_20160128_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskrunner',
            name='state',
            field=models.IntegerField(default=0, choices=[(0, b'CREATED'), (100, b'PENDING'), (200, b'CONNECTIONS_ESTABLISHED'), (300, b'ASSETS_PREPARED'), (400, b'COMMANDS_RUN'), (500, b'COMPLETE'), (600, b'FAILED'), (700, b'SUCCEEDED')]),
        ),
    ]
