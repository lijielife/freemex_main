# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150909_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='cash',
            field=models.FloatField(default=500000),
        ),
        migrations.AlterField(
            model_name='player',
            name='value_in_stocks',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='playertostock',
            name='price_bought_at',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='stock',
            name='price',
            field=models.FloatField(),
        ),
    ]
