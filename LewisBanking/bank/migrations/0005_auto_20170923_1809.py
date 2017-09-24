# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0004_auto_20170923_0104'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loan',
            old_name='loan_id',
            new_name='account_number',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='is_superUser',
            new_name='is_active',
        ),
        migrations.AddField(
            model_name='loan',
            name='balance',
            field=models.DecimalField(default=0.0, max_digits=10, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loan',
            name='end_date',
            field=models.DateField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loan',
            name='start_date',
            field=models.DateField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
