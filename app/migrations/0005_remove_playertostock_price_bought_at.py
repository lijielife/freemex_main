# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20160119_0708'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playertostock',
            name='price_bought_at',
        ),
    ]
