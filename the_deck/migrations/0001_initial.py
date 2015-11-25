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
            name='HostSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
                ('adapter', models.IntegerField(default=0, choices=[(0, b'CHEF_CLIENT')])),
                ('query', models.CharField(max_length=512)),
            ],
            options={
                'verbose_name_plural': 'inventories',
            },
        ),
        migrations.CreateModel(
            name='StaticHost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
                ('fqdn', models.CharField(max_length=128)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
                ('run_command', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField()),
                ('task', models.ForeignKey(to='the_deck.Task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('level', models.CharField(default=b'INFO', max_length=5)),
                ('log', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='TaskRunner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('task_id', models.CharField(max_length=128)),
                ('state', models.IntegerField(default=0, choices=[(0, b'CREATED'), (100, b'PENDING'), (200, b'RUNNING'), (300, b'SUCCEEDED'), (400, b'FAILED')])),
                ('fail_as_group', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TaskRunResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('result', models.TextField()),
                ('is_error', models.BooleanField(default=False)),
                ('task', models.ForeignKey(to='the_deck.Task')),
                ('task_runner', models.ForeignKey(to='the_deck.TaskRunner')),
            ],
        ),
        migrations.CreateModel(
            name='TaskSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128)),
                ('remote_user', models.CharField(max_length=128)),
                ('hostsets', models.ManyToManyField(to='the_deck.HostSet')),
                ('tasks', models.ManyToManyField(to='the_deck.Task', through='the_deck.TaskList')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(max_length=128)),
                ('is_admin', models.BooleanField(default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='taskrunner',
            name='taskset',
            field=models.ForeignKey(to='the_deck.TaskSet'),
        ),
        migrations.AddField(
            model_name='taskrunner',
            name='user_profile',
            field=models.ForeignKey(to='the_deck.UserProfile'),
        ),
        migrations.AddField(
            model_name='tasklog',
            name='taskrunner',
            field=models.ForeignKey(to='the_deck.TaskRunner'),
        ),
        migrations.AddField(
            model_name='tasklist',
            name='taskset',
            field=models.ForeignKey(to='the_deck.TaskSet'),
        ),
        migrations.AddField(
            model_name='hostset',
            name='inventories',
            field=models.ManyToManyField(to='the_deck.Inventory'),
        ),
        migrations.AddField(
            model_name='hostset',
            name='static_hosts',
            field=models.ManyToManyField(to='the_deck.StaticHost'),
        ),
    ]
