from django_compute.engines.base import BaseEngine
import subprocess 

class LocalJobEngine(BaseEngine):
    def run(self, job, args=[]):
        BaseEngine.run(self, job)
        subprocess.Popen([job.script_path]+args)
        
    