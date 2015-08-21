from django.db import models
from jsonfield.fields import JSONField
from django_compute.exceptions import JobAlreadyRunException
from django_compute.engines.local import LocalJobEngine
import string
import random
import copy
from django.template.loader import render_to_string
from django.template.base import Template
from django.template.context import Context
import os
import stat


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class JobTemplate(models.Model):
    ENGINE_SGE = 'SGE'
    ENGINE_SLURM = 'SLURM'
    ENGINE_LOCAL = 'local'
    ENGINES = ((ENGINE_LOCAL,'Local'),(ENGINE_SGE, 'SGE'),(ENGINE_SLURM,'SLURM'))
    id = models.CharField(max_length=25,primary_key=True)
    description = models.TextField(null=True,blank=True)
    engine = models.CharField(choices=ENGINES,max_length=10)
    template = models.FileField(upload_to='job_templates')
    default_params = JSONField(default='{}')
    default_args = JSONField(blank=True,null=True)
    def create_script(self,job):
        file = self.template
        file.open(mode='rb')
        template = Template(file.read())
        c = Context(job.params)
        rendered = template.render(c)
        script = open(job.script_path, 'w')
        script.write(rendered)
        script.close()
        st = os.stat(job.script_path)
        os.chmod(job.script_path, st.st_mode | 0111)
    def create_job(self,path,params={},args=None):
        if not args:
            args = self.default_args if self.default_args else []
        job_params = copy.copy(self.default_params)
        job_params.update(params)
        job = Job.objects.create(template=self,script_path=path,params=job_params,args=args)
        job.params['jobid']=job.id
        job.params['api_key']=job.api_key
        job.save()
        try:
            self.create_script(job)
        except Exception, e:
            job.delete()
            raise e
        return job
#         job = Job.objects.create(template=self,)
    
class Job(models.Model):
    STATUS_QUEUED = 'QUEUED'
    STATUS_STARTED = 'STARTED'
    STATUS_FAILED = 'FAILED'
    STATUS_DONE = 'DONE'
    STATUSES = ((STATUS_QUEUED,'Queued'),(STATUS_STARTED,'Started'),(STATUS_FAILED,'Failed'),(STATUS_DONE,'Done'),)
    id = models.CharField(max_length=10,default=id_generator,primary_key=True)
    api_key = models.CharField(max_length=10,default=id_generator)
    job_id = models.CharField(max_length=15,blank=True,null=True)
    template = models.ForeignKey(JobTemplate)
    script_path = models.CharField(max_length=250)
    params = JSONField(default='{}')
    args = JSONField(blank=True,null=True)
    status = models.CharField(choices=STATUSES, max_length=10,blank=True,null=True)
    data = JSONField(default='{}')
    def run(self):
        if self.status:
            raise JobAlreadyRunException("This job has already been run.  Current status: '%s'" % self.status)
        if self.template.engine == JobTemplate.ENGINE_LOCAL:
            engine = LocalJobEngine()
            engine.run(self,args=self.args)
