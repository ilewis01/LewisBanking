# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0006_auto_20170924_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='payment',
            field=models.DecimalField(default=0.0, max_digits=15, decimal_places=2),
            preserve_default=True,
        ),
    ]
