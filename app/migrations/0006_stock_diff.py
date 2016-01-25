# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_playertostock_price_bought_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='diff',
            field=models.FloatField(default=0),
        ),
    ]
