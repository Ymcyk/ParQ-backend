# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-25 10:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djroles.roles


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Driver',
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='wallet')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, djroles.roles.BaseRole),
        ),
    ]