# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_deck', '0002_taskgroup_running'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='time',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=10, blank=True),
        ),
    ]
