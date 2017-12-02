# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 13:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
        ('sensors', '0002_sensordata'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sensors', to='map.Address'),
        ),
    ]
