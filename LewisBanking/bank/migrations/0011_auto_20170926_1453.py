# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0010_auto_20170926_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='serializer',
            field=models.CharField(default=b'Account', max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='loan',
            name='serializer',
            field=models.CharField(default=b'Loan', max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
    ]
