from django.db import models
from jsonfield.fields import JSONField
from django_compute.exceptions import JobAlreadyRunException, JobTerminationException
import string
import random
import copy
from django.template.loader import render_to_string
from django.template.base import Template
from django.template.context import Context
import os
import stat
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, post_init, pre_save
from django_compute.utils import merge
from django.conf import settings


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
    def __unicode__(self):
        return self.id

class Job(models.Model):
    STATUS_QUEUED = 'QUEUED'
    STATUS_STARTED = 'STARTED'
    STATUS_FAILED = 'FAILED'
    STATUS_TERMINATED = 'TERMINATED'
    STATUS_DONE = 'DONE'
    STATUSES = ((STATUS_QUEUED,'Queued'),(STATUS_STARTED,'Started'),(STATUS_FAILED,'Failed'),(STATUS_TERMINATED,'Terminated'),(STATUS_DONE,'Done'),)
    
    id = models.CharField(max_length=10,default=id_generator,primary_key=True)
    parent = models.ForeignKey('self',blank=True,null=True,related_name='children')
    name = models.CharField(max_length=250,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now=True)
    run_at = models.DateTimeField(blank=True,null=True)
    api_key = models.CharField(max_length=10,default=id_generator)
    job_id = models.CharField(max_length=15,blank=True,null=True)
    template = models.ForeignKey(JobTemplate,blank=True,null=True)
    script_path = models.CharField(max_length=250)
    params = JSONField(default='{}')
    args = JSONField(blank=True,null=True)
    status = models.CharField(choices=STATUSES, max_length=10,blank=True,null=True)
    data = JSONField(default='{}')
    output_directory = models.CharField(max_length=100,null=True,blank=True)
    callback_id = models.CharField(max_length=30,blank=True,null=True)
    class Meta:
        ordering = ['-created']
    def __unicode__(self):
        return '%s: %s - %s (%s)'%(self.template.id,self.id,str(self.created),self.status)
    @property
    def update_url(self):
        return settings.SITE_URL + reverse('update_job', kwargs={'job_id':self.id})+'?api_key=%s'%self.api_key
    def get_params(self):
        return merge(self.template.default_params,self.params)
    def get_args(self):
        return self.args if self.args else self.template.default_args
    def run(self):
        if self.job_id:
            raise JobAlreadyRunException("This job has already been run.  Current status: '%s'" % self.status)
        self._engine.run()
    def terminate(self):
        if not self.job_id or self.status in [Job.STATUS_DONE,Job.STATUS_FAILED,Job.STATUS_TERMINATED]:
            raise JobTerminationException
        self._engine.terminate()

def post_job_init(sender,**kwargs):
    from django_compute.engines.base import JobEngineFactory
    job = kwargs['instance']
    job._engine = JobEngineFactory.create(job)
post_init.connect(post_job_init, sender=Job)

def job_saved(sender,**kwargs):
    job = kwargs['instance']
    try:
        if job.template:
            file = job.template.template
            file.open(mode='rb')
            template = Template(file.read())
            params = merge(job.get_params(),{'update_url':job.update_url})
            c = Context(params)
            rendered = template.render(c)
            script = open(job.script_path, 'w')
            script.write(rendered)
            script.close()
            st = os.stat(job.script_path)
            os.chmod(job.script_path, st.st_mode | 0111)
    except Exception, e:
        job.delete()
        raise e
    return job
post_save.connect(job_saved, sender=Job)

