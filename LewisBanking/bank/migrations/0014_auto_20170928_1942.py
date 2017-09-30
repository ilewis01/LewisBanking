# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0013_auto_20170928_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='action',
            field=models.ForeignKey(default=None, blank=True, to='bank.Action', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='action',
            name='action',
            field=models.CharField(default=0, max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
    ]
