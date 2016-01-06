""" A basic job model, and local job implementation.

author: Brian Schrader
since: 2016-01-04
"""

import os
from subprocess import Popen, PIPE


stdout = '/tmp/queuemanager.out'
stderr = '/tmp/queuemanager.err'


def call(args):
    """ Calls the given arguments in a seperate process
    and returns the contents of standard out.
    """
    with open(stdout, 'w+') as f1, open(stderr, 'w+') as f2:
        p = Popen(args, stdout=f1, stderr=f2)
        p.communicate()
        f1.seek(0)
        out = f1.read()
    return out


class Job(object):
    """ A template job class that just runs the given command script locally.
    To make your own custom jobs, subclass this Job and override the status methods, the submit method, and cmd property.
    """
    
    JOB_FILE_PATTERN = 'metapipe.{}.job'
    
    def __init__(self, alias, job_cmd, depends_on=[]):
        """ Create an new job with the given name, and command. """
        self.job_cmd = job_cmd
        self.depends_on = depends_on
        self.alias = alias
        self.attempts = 0
        self.filename = JOB_FILE_PATTERN.format(self.alias)

    def __repr__(self):
        return '<Job: {}>'.format(self.cmd)

    def make(self):
        """ Evaluate the command, and write it to a file. """
        with open(self.filename, 'w') as f:
            f.write(self.cmd.eval())
            
    # Override these...

    @property
    def cmd(self):
        """ Returns the command needed to submit the calculations. 
        Normally, this would be just running the command, however if 
        using a queue system, then this should return the command to 
        submit the command to the queue.
        """
        pass

    def submit(self, job):
        """ Submits the job to be run. If an external queue system is used,
        this method submits itself to that queue. Else it runs the job itself.
        :see: call
        """
        pass
        
    def is_running(self):
        """ Returns whether the job is running or not. """
        pass

    def is_queued(self):
        """ Returns whether the job is queued or not. 
        This function is only used if jobs are submitted to an external queue.
        """
        pass
        
    def is_complete(self):
        """ Returns whether the job is complete or not. """
        pass

    def is_error(self):
        """ Checks to see if the job errored out. """
        pass
        

class LocalJob(Job):
    """ A subclass of job for local calculations. """
    
    def __init__(self, alias, cmd, depends_on=[], shell='bash')
        super().__init__(alias, cmd, depends_on)
        self.shell = shell
        
        self._running = False
    
    @property
    def cmd(self):
        return [shell, self.filename]

    def submit(self, job):
        self._running = True
        call(self.cmd)
        
    def is_running(self):
        return self._running

    def is_queued(self):
        """ Returns False since local jobs are not submitted to an 
        external queue.
        """
        return False
            
    def is_complete(self):
        """ Returns whether the job is complete or not. """
        pass

    def is_error(self):
        """ Checks to see if the job errored out. """
        pass
        





