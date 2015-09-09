# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerToStock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=0)),
                ('price_bought_at', models.IntegerField()),
            ],
            options={
                'db_table': 'playertostock',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
            ],
            options={
                'db_table': 'stock',
            },
        ),
        migrations.AddField(
            model_name='player',
            name='cash',
            field=models.IntegerField(default=500000),
        ),
        migrations.AddField(
            model_name='player',
            name='email',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='player',
            name='value_in_stocks',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playertostock',
            name='player',
            field=models.ForeignKey(to='app.Player'),
        ),
        migrations.AddField(
            model_name='playertostock',
            name='stock',
            field=models.ForeignKey(to='app.Stock'),
        ),
    ]
