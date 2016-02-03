""" The metapipe runtime.

author: Brian Schrader
since: 2015-01-13
"""

from time import sleep

from metapipe.models import JobQueue


class Runtime(object):
    
    def __init__(self, command_templates, job_types, job_type='local', sleep_time=1):
        
        self.job_types = job_types
        self.job_type = job_type
        self.templates = command_templates
        self.prev_commands = []
        self.queue = JobQueue()
        self.sleep_time = sleep_time

    @property
    def is_empty(self):
        return len(self.templates) == 0
        
    @property
    def should_stop(self):
        if self.queue.locked() and self.is_empty:
            return True
        elif self.queue.is_empty and self.is_empty:
            return True
        else:
            return False
  
    def run(self):
        """ Begins the runtime execution. """
        iterations = 0
        queue = self.queue.tick()        
        while True:
            new_commands = self._get_new_commands()
            for command in new_commands:
                command.update_dependent_files(self.prev_commands)
                self.prev_commands.append(command)
            
            new_jobs = []
            for command in new_commands:        
                new_jobs.append(self._get_job(command))
            
            [self.queue.push(job) for job in new_jobs]
            
            try:
                next(queue)
            except StopIteration:
                pass
            
            if self.should_stop:
                break
            else:
                iterations += 1
                sleep(self.sleep_time)
            
        return iterations
            
    # Private Methods
            
    def _get_job(self, command):
        """ Given a command and a type, contruct a job.
        :returns job:
        :rtype Job subclass:
        """
        job_constructor = self.job_types[self.job_type]
        job = job_constructor(alias=command.alias, command=command)
        return job
        
    def _ready(self, command_template):
        """ Check if the template's dependencies are resolved and return if
        the template is ready to be evaluated. 
        """
        if len(command_template.dependencies) == 0:
            return True
        else: 
            return not any(True for dep in command_template.dependencies
                if dep in self.templates)
                    
    def _get_new_commands(self):
        """ Returns a list of new commands to be run, and removes them from
        the global pending list.
        """
        new_commands, not_ready = [], []
        for template in self.templates:
            if self._ready(template):
                new_commands.extend(template.eval())
            else:
                not_ready.append(template)
        self.templates = not_ready
        return new_commands
