# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('django_compute', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 21, 17, 14, 52, 103449, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
