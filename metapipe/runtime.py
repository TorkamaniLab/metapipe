""" The metapipe runtime.

author: Brian Schrader
since: 2015-01-13
"""

from time import sleep

from models import Queue


class Runtime(object):
    
    def __init__(self, command_templates, job_type='local', job_types):
        
        self.job_types = job_types
        self.job_type = job_type
        self.templates = command_templates
        self.queue = Queue()

    def get_job(command):
        """ Given a command and a type, contruct a job.
        :returns job:
        :rtype Job subclass:
        """
        job_constructor = self.job_types[self.job_type]
        return job_constructor(alias=cmd.alias, command=cmd)
    
    def run(self):
        """ Begins the runtime execution. """
        while True:
            new_jobs = []
            
            # Get new jobs.
            
            self.queue.push(new_jobs)
            try:
                self.queue.tick()
            except StopIteration:
                break
            sleep(0.5)
            
