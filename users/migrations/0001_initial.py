# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-25 00:22
from __future__ import unicode_literals

import django.contrib.auth.models
from django.db import migrations
import djroles.roles


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user', djroles.roles.BaseRole),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Officer',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user', djroles.roles.BaseRole),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
