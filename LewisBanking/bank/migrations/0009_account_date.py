# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0008_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='date',
            field=models.DateField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
