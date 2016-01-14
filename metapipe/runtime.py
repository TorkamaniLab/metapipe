""" The metapipe runtime.

author: Brian Schrader
since: 2015-01-13
"""

from queue import Queue


class Runtime(object):
    
    def __init__(self, command_templates, job_type='local'):
        
        self.job_type = job_type
        self.templates = command_templates
        self.queue = Queue()

    def get_job(command):
        """ Given a command and a type, contruct a job.
        :returns job:
        :rtype Job subclass:
        """
        if self.job_type == 'pbs':
            job = PBSJob(alias=cmd.alias, command=cmd)
        else:
            job = LocalJob(alias=cmd.alias, command=cmd)    
        return job
    
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
            
