# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 16:42
from __future__ import unicode_literals

from django.db import migrations, models
import map.models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0004_auto_20171202_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='house_no',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]