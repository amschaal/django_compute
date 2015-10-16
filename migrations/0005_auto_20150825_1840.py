# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('django_compute', '0004_job_callback_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='directories',
            field=jsonfield.fields.JSONField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='files',
            field=jsonfield.fields.JSONField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
