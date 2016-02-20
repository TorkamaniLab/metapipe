""" A template that evaluates to muliple jobs and places them back on the queue.
author: Brian Schrader
since: 2016-02-19
"""

from .job import Job


class JobTemplate(Job):

    def __init__(self, alias, command_template, depends_on, queue, job_class):
        super(JobTemplate, self).__init__(alias, command_template, depends_on)
        self.command_template = command_template
        self.queue = queue
        self.job_class = job_class
        self.jobs = []

    def __repr__(self):
        return '<JobTemplate: {}>'.format(self.alias)

    def submit(self):
        jobs = self._get_jobs_from_template(self.command_template, self.job_class)
        [self.queue.push(job) for job in jobs]
        self.jobs = jobs

    def is_running(self):
        if len(self.jobs) > 0:
            return any(job.is_running() for job in self.jobs)
        return False

    def is_queued(self):
        return False

    def is_complete(self):
        if len(self.jobs) > 0:
            return all(job.is_complete() for job in self.jobs)
        return False

    def is_error(self):
        if len(self.jobs) > 0:
            return all(job.is_error() for job in self.jobs)
        return False

    def is_fail(self):
        self.attempts > self.MAX_RETRY

    def _get_jobs_from_template(self, template, job_class):
        """ Given a template, a job class, construct jobs from
        the given template.
        """
        jobs = []
        for command in template.eval():
            alias = command.alias
            depends_on = [job.alias
                for job in self.queue.all_jobs
                    for deps in command.depends_on
                        if deps == job.alias]
            command.update_dependent_files([job.command
                for job in self.queue.all_jobs
                    if not isinstance(job, JobTemplate)])

            job = job_class(alias, command, depends_on)
            jobs.append(job)
        return jobs

