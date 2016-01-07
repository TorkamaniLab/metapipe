import subprocess

import gevent

from job import Job, call


class LocalJob(Job):
    """ A subclass of job for local calculations. """
    
    def __init__(self, alias, command, depends_on=[], shell='bash'):
        super(LocalJob, self).__init__(alias, command, depends_on)
        self.shell = shell
        
        self._task = None
    
    @property
    def cmd(self):
        return [self.shell, self.filename]

    def submit(self):
        self.make()
        self._task = gevent.spawn(call, self.cmd)
        
    def is_running(self):
        try:
            if not self._task.ready():
                return True
        except AttributeError:
            pass
        return False
                
    def is_queued(self):
        """ Returns False since local jobs are not submitted to an 
        external queue.
        """
        return False
            
    def is_complete(self):
        try:
            return self._task.successful()
        except AttributeError:
            return False
                    
    def is_error(self):
        """ Checks to see if the job errored out. """
        try:
            if self._task.successful():
                try:
                    stdout, stderr = self._task.get(block=False)
                except gevent.Timeout:
                    return False    
        
                if len(stderr.readlines()) > 0:
                    return True
        except AttributeError:
            pass
        return False
