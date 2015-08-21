from django_compute.models import JobTemplate
from django_compute.exceptions import JobTypeException

class BaseJobEngine:
    def __init__(self,job):
        self.job = job
    def run(self,job):
        raise NotImplementedError('Run method not implemented for this job engine.')
    def terminate(self,job):
        raise NotImplementedError('Terminate method not implemented for this job engine.')
    
class JobEngineFactory:
    @staticmethod
    def create(job):
        if job.template.engine == JobTemplate.ENGINE_LOCAL:
            from django_compute.engines.local import LocalJobEngine
            return LocalJobEngine(job)
        raise JobTypeException