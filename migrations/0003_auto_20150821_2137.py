# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_compute', '0002_job_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='job',
            name='run_at',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'QUEUED', b'Queued'), (b'STARTED', b'Started'), (b'FAILED', b'Failed'), (b'TERMINATED', b'Terminated'), (b'DONE', b'Done')]),
            preserve_default=True,
        ),
    ]
