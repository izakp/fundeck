# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicHosts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('adapter', models.CharField(max_length=128)),
                ('query_parameters', models.CharField(max_length=128, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='HostSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dynamic_hosts', models.ManyToManyField(to='the_deck.DynamicHosts')),
            ],
        ),
        migrations.CreateModel(
            name='StaticHost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ip', models.CharField(max_length=128)),
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
                ('task_runner', models.ForeignKey(to='the_deck.TaskRunner')),
            ],
        ),
        migrations.CreateModel(
            name='TaskSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('remote_user', models.CharField(max_length=128)),
                ('groups', models.ManyToManyField(to='the_deck.Group')),
                ('hostsets', models.ManyToManyField(to='the_deck.HostSet')),
                ('tasks', models.ManyToManyField(to='the_deck.Task')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=128)),
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
                ('user', models.OneToOneField(to='the_deck.User')),
            ],
        ),
        migrations.AddField(
            model_name='taskset',
            name='user_profiles',
            field=models.ManyToManyField(to='the_deck.UserProfile'),
        ),
        migrations.AddField(
            model_name='taskrunner',
            name='taskset',
            field=models.ForeignKey(to='the_deck.TaskSet'),
        ),
        migrations.AddField(
            model_name='taskrunner',
            name='user',
            field=models.OneToOneField(to='the_deck.User'),
        ),
        migrations.AddField(
            model_name='tasklog',
            name='taskrunner',
            field=models.ForeignKey(to='the_deck.TaskRunner'),
        ),
        migrations.AddField(
            model_name='hostset',
            name='static_hosts',
            field=models.ManyToManyField(to='the_deck.StaticHost'),
        ),
        migrations.AddField(
            model_name='group',
            name='user_profile',
            field=models.ManyToManyField(to='the_deck.UserProfile'),
        ),
    ]
