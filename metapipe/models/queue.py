""" A simple manager for a task queue.

The manager handles creating, submitting, and managing
running jobs, and can even resubmit jobs that have failed.

author: Brian Schrader
since: 2015-08-27
"""

import logging


class Queue(object):
    """ An abstract class for managing a queue of jobs. To use this class,
    subclass it and fill in the callbacks you need.
    """

    def __init__(self):
        self.queue = []
        self.running = []
        self.failed = []
        self.complete = []

    def __repr__(self):
        return '<Queue: jobs=%s>' % str(len(self.active_jobs))

    @property
    def is_empty(self):
        return len(self.active_jobs) == 0

    @property
    def active_jobs(self):
        """ Returns a list of all jobs submitted to the queue,
        or in progress.
        """
        return self.queue + self.running

    @property
    def all_jobs(self):
        """ Returns a list of all jobs submitted to the queue, complete,
        in-progess or failed.
        """
        return self.complete + self.failed + self.queue + self.running

    def ready(self, job):
        """ Determines if the job is ready to be sumitted to the
        queue. It checks if the job depends on any currently
        running or queued operations.
        """
        no_deps = len(job.depends_on) == 0
        all_complete = all(j.is_complete() for j in self.active_jobs
                if j.alias in job.depends_on)
        none_failed = not any(True for j in self.failed
                if j.alias in job.depends_on)
        return no_deps or (all_complete and none_failed)

    def locked(self):
        """ Determines if the queue is locked. """
        if len(self.failed) == 0:
            return False
        for fail in self.failed:
            for job in self.active_jobs:
                if fail.alias in job.depends_on:
                    return True

    def push(self, job):
        """ Push a job onto the queue. This does not submit the job. """
        self.queue.append(job)

    def tick(self):
        """ Submits all the given jobs in the queue and watches their
        progress as they proceed. This function yields at the end of
        each iteration of the queue.
        :raises RuntimeError: If queue is locked.
        """
        self.on_start()
        while not self.is_empty:
            cruft = []
            for job in self.queue:
                if not self.ready(job):
                    continue
                self.on_ready(job)
                try:
                    job.submit()
                except ValueError:
                    if job.should_retry:
                        self.on_error(job)
                        job.attempts += 1
                    else:
                        self.on_fail(job)
                        cruft.append(job)
                        self.failed.append(job)
                else:
                    self.running.append(job)
                    self.on_submit(job)
                    cruft.append(job)

            self.queue = [job for job in self.queue if job not in cruft]

            cruft = []
            for job in self.running:
                if job.is_running() or job.is_queued():
                    pass
                elif job.is_complete():
                    self.on_complete(job)
                    cruft.append(job)
                    self.complete.append(job)
                elif job.is_fail():
                    self.on_fail(job)
                    cruft.append(job)
                    self.failed.append(job)
                elif job.is_error():
                    self.on_error(job)
                    cruft.append(job)
                else:
                    pass
            self.running = [job for job in self.running if job not in cruft]

            if self.locked() and self.on_locked():
                raise RuntimeError
            self.on_tick()
            yield
        self.on_end()

    # Callbacks...

    def on_start(self):
        """ Called when the queue is starting up. """
        pass

    def on_end(self):
        """ Called when the queue is shutting down. """
        pass

    def on_locked(self):
        """ Called when the queue is locked and no jobs can proceed.
        If this callback returns True, then the queue will be restarted,
        else it will be terminated.
        """
        return True

    def on_tick(self):
        """ Called when a tick of the queue is complete. """
        pass

    def on_ready(self, job):
        """ Called when a job is ready to be submitted.
        :param job: The given job that is ready.
        """
        pass

    def on_submit(self, job):
        """ Called when a job has been submitted.
        :param job: The given job that has been submitted.
        """
        pass

    def on_complete(self, job):
        """ Called when a job has completed.
        :param job: The given job that has completed.
        """
        pass

    def on_error(self, job):
        """ Called when a job has errored. By default, the job
        is resubmitted until some max threshold is reached.
        :param job: The given job that has errored.
        """
        pass

    def on_fail(self, job):
        """ Called when a job has failed after multiple resubmissions. The
        given job will be removed from the queue.
        :param job: The given job that has errored.
        """
        pass


class JobQueue(Queue):
    """ A concrete subclass of the Queue. """

    def __init__(self):
        super(JobQueue, self).__init__()
        self.logger = logging.getLogger(__name__)

    def on_locked(self):
        print('The queue is locked. Please check the logs.')
        return True

    def on_complete(self, job):
        print('Complete: %s' % job.alias)

    def on_ready(self, job):
        print('Ready: %s' % job.alias)

    def on_error(self, job):
        print('Error: Job %s has failed, retrying (%s/%s)'
            % (job.alias, str(job.attempts), str(job.MAX_RETRY)))

    def on_fail(self, job):
        print('Error: Job %s has failed. Retried %s times.'
                % (job.alias, str(job.attempts)))


