# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 14:19
from __future__ import unicode_literals

from django.db import migrations, models
import map.models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0002_auto_20171202_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(help_text='Enter city', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(help_text='Enter country', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='house_no',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(help_text='Enter street', max_length=20, null=True),
        ),
    ]