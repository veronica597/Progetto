# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-12 17:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dispenser', '0005_auto_20190812_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datiraccolti',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
