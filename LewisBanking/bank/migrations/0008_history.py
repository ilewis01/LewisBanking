# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0007_loan_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account_number', models.CharField(default=None, max_length=8, null=True, blank=True)),
                ('description', models.CharField(default=None, max_length=200, null=True, blank=True)),
                ('balance', models.DecimalField(default=0.0, max_digits=15, decimal_places=2)),
                ('date', models.DateField(default=None, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
