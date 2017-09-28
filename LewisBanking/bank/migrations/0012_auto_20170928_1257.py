# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0011_auto_20170926_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.DecimalField(default=0.0, max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='history',
            name='balance',
            field=models.DecimalField(default=0.0, max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='loan',
            name='balance',
            field=models.DecimalField(default=0.0, max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='loan',
            name='loan_amount',
            field=models.DecimalField(default=0.0, max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='loan',
            name='payment',
            field=models.DecimalField(default=0.0, max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='loan',
            name='rate',
            field=models.DecimalField(default=0.0, max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='loan',
            name='total_interest',
            field=models.DecimalField(default=0.0, max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
    ]
