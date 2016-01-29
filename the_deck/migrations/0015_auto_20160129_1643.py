# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_deck', '0014_auto_20160129_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='fqdn',
            field=models.CharField(unique=True, max_length=512),
        ),
    ]
