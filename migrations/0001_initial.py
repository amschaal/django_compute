# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django_compute.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.CharField(default=django_compute.models.id_generator, max_length=10, serialize=False, primary_key=True)),
                ('api_key', models.CharField(default=django_compute.models.id_generator, max_length=10)),
                ('job_id', models.CharField(max_length=15, null=True, blank=True)),
                ('script_path', models.CharField(max_length=250)),
                ('params', jsonfield.fields.JSONField(default=b'{}')),
                ('args', jsonfield.fields.JSONField(null=True, blank=True)),
                ('status', models.CharField(blank=True, max_length=10, null=True, choices=[(b'QUEUED', b'Queued'), (b'STARTED', b'Started'), (b'FAILED', b'Failed'), (b'DONE', b'Done')])),
                ('data', jsonfield.fields.JSONField(default=b'{}')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JobTemplate',
            fields=[
                ('id', models.CharField(max_length=25, serialize=False, primary_key=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('engine', models.CharField(max_length=10, choices=[(b'local', b'Local'), (b'SGE', b'SGE'), (b'SLURM', b'SLURM')])),
                ('template', models.FileField(upload_to=b'job_templates')),
                ('default_params', jsonfield.fields.JSONField(default=b'{}')),
                ('default_args', jsonfield.fields.JSONField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='job',
            name='template',
            field=models.ForeignKey(to='django_compute.JobTemplate'),
            preserve_default=True,
        ),
    ]
