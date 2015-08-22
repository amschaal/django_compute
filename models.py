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
from django.db.models.signals import post_save, post_init
from django_compute.utils import merge



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
#         job_params = copy.copy(self.default_params)
        job_params = merge(self.default_params,params)
        job = Job.objects.create(template=self,script_path=path,params=job_params,args=args)
        job.params['update_url']=job.update_url
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
    STATUS_TERMINATED = 'TERMINATED'
    STATUS_DONE = 'DONE'
    STATUSES = ((STATUS_QUEUED,'Queued'),(STATUS_STARTED,'Started'),(STATUS_FAILED,'Failed'),(STATUS_TERMINATED,'Terminated'),(STATUS_DONE,'Done'),)
    id = models.CharField(max_length=10,default=id_generator,primary_key=True)
    created = models.DateTimeField(auto_now=True)
    run_at = models.DateTimeField(blank=True,null=True)
    api_key = models.CharField(max_length=10,default=id_generator)
    job_id = models.CharField(max_length=15,blank=True,null=True)
    template = models.ForeignKey(JobTemplate)
    script_path = models.CharField(max_length=250)
    params = JSONField(default='{}')
    args = JSONField(blank=True,null=True)
    status = models.CharField(choices=STATUSES, max_length=10,blank=True,null=True)
    data = JSONField(default='{}')
    class Meta:
        ordering = ['-created']
    def __unicode__(self):
        return '%s: %s - %s (%s)'%(self.template.id,self.id,str(self.created),self.status)
    @property
    def update_url(self):
        return "http://127.0.0.1:8000" + reverse('update_job', kwargs={'job_id':self.id})+'?api_key=%s'%self.api_key
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

# def job_saved(sender,**kwargs):
#     job = kwargs['instance']
# post_save.connect(job_saved, sender=Job)