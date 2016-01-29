# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_deck', '0015_auto_20160129_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remotefile',
            name='permissions',
            field=models.CharField(default=b'644', max_length=4),
        ),
    ]
