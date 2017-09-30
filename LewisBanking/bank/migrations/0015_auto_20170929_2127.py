# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0014_auto_20170928_1942'),
    ]

    operations = [
        migrations.RenameField(
            model_name='history',
            old_name='balance',
            new_name='b_balance',
        ),
        migrations.AddField(
            model_name='history',
            name='e_balance',
            field=models.DecimalField(default=0.0, max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
    ]
