""" The metapipe runtime.

author: Brian Schrader
since: 2015-01-13
"""

from time import sleep

from metapipe.models import JobQueue, JobTemplate


class Runtime(object):

    def __init__(self, command_templates, job_types, job_type='local', sleep_time=1):
        self.complete_jobs = []
        self.queue = JobQueue()
        self.sleep_time = sleep_time

        job_templates = []
        for command_template in command_templates:
            self.add(command_template, job_types[job_type])

    @property
    def should_stop(self):
        if self.queue.locked():
            return True
        elif self.queue.is_empty:
            return True
        else:
            return False

    def add(self, command_template, job_class):
        """ Given a command template, add it as a job to the queue. """
        job = JobTemplate(command_template.alias,
            command_template=command_template,
            depends_on=command_template.depends_on, queue=self.queue,
            job_class=job_class)
        self.queue.push(job)

    def run(self):
        """ Begins the runtime execution. """
        iterations = 0
        queue = self.queue.tick()
        while not self.should_stop:
            try:
                next(queue)
            except StopIteration:
                pass

            iterations += 1
            sleep(self.sleep_time)
        return iterations
