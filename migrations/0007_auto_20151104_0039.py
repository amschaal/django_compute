# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_compute', '0006_auto_20150825_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='name',
            field=models.CharField(max_length=250, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='job',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='django_compute.Job', null=True),
            preserve_default=True,
        ),
    ]
