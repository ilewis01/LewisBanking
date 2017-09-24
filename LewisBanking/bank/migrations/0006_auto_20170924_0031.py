# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0005_auto_20170923_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='total_interest',
            field=models.DecimalField(default=0.0, max_digits=15, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='loan',
            name='balance',
            field=models.DecimalField(default=0.0, max_digits=15, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='loan',
            name='loan_amount',
            field=models.DecimalField(default=0.0, max_digits=15, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='loan',
            name='rate',
            field=models.DecimalField(default=0.0, max_digits=15, decimal_places=2),
            preserve_default=True,
        ),
    ]
