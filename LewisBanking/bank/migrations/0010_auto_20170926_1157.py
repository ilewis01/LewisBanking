# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0009_account_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='account_type',
            field=models.CharField(default=None, max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='history',
            name='user_id',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
