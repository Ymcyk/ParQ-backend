# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-26 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Name'),
        ),
    ]
