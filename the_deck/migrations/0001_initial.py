# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
                ('command', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
                ('fqdn', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='SshUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(unique=True, max_length=512)),
                ('private_key', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('command', models.TextField()),
                ('host', models.CharField(max_length=512)),
                ('username', models.CharField(max_length=512)),
                ('state', models.IntegerField(default=0, choices=[(0, b'CREATED'), (100, b'RUNNING'), (200, b'FAILED'), (300, b'SUCCEEDED')])),
                ('stdout', models.TextField(null=True, blank=True)),
                ('stderr', models.TextField(null=True, blank=True)),
                ('status', models.IntegerField(null=True, blank=True)),
                ('error', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TaskGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('command', models.ForeignKey(to='the_deck.Command')),
                ('hosts', models.ManyToManyField(to='the_deck.Host')),
                ('ssh_user', models.ForeignKey(to='the_deck.SshUser')),
            ],
        ),
        migrations.CreateModel(
            name='TaskRunner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('state', models.IntegerField(default=0, choices=[(0, b'CREATED'), (100, b'PENDING'), (200, b'RUNNING'), (300, b'FAILED'), (400, b'SUCCEEDED')])),
                ('task_group', models.ForeignKey(to='the_deck.TaskGroup')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='task_runner',
            field=models.ForeignKey(to='the_deck.TaskRunner'),
        ),
    ]
