# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-12 16:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Dispenser', '0002_auto_20190812_1642'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datiraccolti',
            old_name='date',
            new_name='created_on',
        ),
    ]
