# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_deck', '0005_auto_20160119_1741'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chefinventory',
            options={'verbose_name_plural': 'chef inventories'},
        ),
        migrations.AddField(
            model_name='chefinventory',
            name='name',
            field=models.CharField(default='foo', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taskgroup',
            name='name',
            field=models.CharField(default='foo', max_length=128),
            preserve_default=False,
        ),
    ]
