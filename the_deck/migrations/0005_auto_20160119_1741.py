# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('the_deck', '0004_auto_20160119_1649'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChefInventory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('server_url', models.CharField(max_length=512)),
                ('pem_data', models.TextField()),
                ('username', models.CharField(max_length=512)),
                ('query', models.CharField(max_length=512)),
            ],
        ),
        migrations.AddField(
            model_name='taskgroup',
            name='chef_inventories',
            field=models.ManyToManyField(to='the_deck.ChefInventory'),
        ),
    ]
