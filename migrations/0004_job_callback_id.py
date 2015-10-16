# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_compute', '0003_auto_20150821_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='callback_id',
            field=models.CharField(max_length=30, null=True, blank=True),
            preserve_default=True,
        ),
    ]
