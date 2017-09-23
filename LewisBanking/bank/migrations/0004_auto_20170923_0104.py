# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0003_auto_20170920_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='rate',
            field=models.DecimalField(default=0.0, max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='accounts',
            field=models.CharField(default=0, max_length=100000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
