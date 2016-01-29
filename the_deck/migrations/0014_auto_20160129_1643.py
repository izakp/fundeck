# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_deck', '0013_auto_20160129_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='command',
            field=models.CharField(max_length=2048),
        ),
    ]
