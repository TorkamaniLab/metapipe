""" The metapipe runtime.

author: Brian Schrader
since: 2015-01-13
"""

from time import sleep

from metapipe.models import JobTemplate


class Runtime(object):

    def __init__(self, command_templates, queue_type, job_types,
            job_type='local', sleep_time=1, max_jobs=10):
        self.complete_jobs = []
        self.queue = queue_type()
        self.sleep_time = sleep_time

        self.queue.MAX_CONCURRENT_JOBS = max_jobs

        job_templates = []
        for command_template in command_templates:
            self.add(command_template, job_types[job_type])

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
        while True:
            try:
                next(queue)
            except StopIteration:
                break

            iterations += 1
            sleep(self.sleep_time)
        return iterations
