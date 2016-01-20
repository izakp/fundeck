# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_deck', '0008_auto_20160120_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remotefile',
            name='permissions',
            field=models.CharField(default=b'644', max_length=3),
        ),
    ]
