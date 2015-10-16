# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_compute', '0005_auto_20150825_1840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='directories',
        ),
        migrations.RemoveField(
            model_name='job',
            name='files',
        ),
        migrations.AddField(
            model_name='job',
            name='output_directory',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
