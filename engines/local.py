from django_compute.engines.base import BaseJobEngine
import subprocess, os, signal
from django_compute.exceptions import JobTerminationException

class LocalJobEngine(BaseJobEngine):
    def run(self, args=[]):
        p = subprocess.Popen([self.job.script_path]+args)
        self.job.job_id = p.pid
        self.job.save()
        BaseJobEngine.run(self)
    def terminate(self):
        if self.job.job_id:
            print "Kill "+str(self.job.job_id)
            os.kill(int(self.job.job_id), signal.SIGKILL)
            BaseJobEngine.terminate(self)
        else:
            raise JobTerminationException
