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
    
    JOB_RETRY_ATTEMPTS = 2

    def __init__(self):
        self.queue = []
                    
    def __repr__(self):
        return '<Queue: jobs=%s>' % len(self.queue)
        
    def __iter__(self):
        return iter(self.queue)
        
    @property
    def is_empty(self):
        return len(self.queue) == 0

    def ready(self, job):
        """ Determines if the job is ready to be sumitted to the
        queue. It checks if the job depends on any currently
        running or queued operations.
        """
        all_complete = all(j.complete for j in self.queue
                if j.alias in job.depends_on)
        none_failed = not any(True for j in self.failed
                if j.name in job.depends_on)
        return all_complete and none_failed

    def locked(self):
        """ Determines if the queue is locked. """
        locked = all(True for j in self.queue
                if any(True for f in self.failed
                    if f in j.depends_on))
                    
    def clean(self):
        """ Clears old or complete jobs from the queue and puts complete
        jobs in the finished queue.
        """        
        self.queue = [job for job in self.queue 
            if (not self.ready(job)) or job.is_running()]

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
        while True:
            if len(self.queue) == 0:
                break
            for job in self.queue:
                if job.is_running() or job.is_queued():
                    pass
                elif job.is_complete():
                    self.on_complete(job)
                elif job.is_error():
                    self.on_error(job)
                elif self.ready(job):
                    self.on_ready(job)
                    job.submit()
                    self.on_submit(job)
                else:
                    pass
            self.clean()
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
        print('------- tick ---------')
    
    def on_ready(self, job):
        """ Called when a job is ready to be submitted. 
        :param job: The given job that is ready.
        """ 
        print('Ready: %s' % job.alias)
        
    def on_submit(self, job):
        """ Called when a job has been submitted. 
        :param job: The given job that has been submitted.
        """ 
        print('Submitted: %s' % job.alias)
        
    def on_complete(self, job):
        """ Called when a job has completed. 
        :param job: The given job that has completed.
        """ 
        print('Complete: %s' % job.alias)
        
    def on_error(self, job):
        """ Called when a job has errored. 
        :param job: The given job that has errored.
        """ 
        print('Error: %s' % job.alias)


class JobQueue(Queue):
    """ A concrete subclass of the Queue. """

    def __init__(self):
        super(JobQueue, self).__init__()
        self.failed = []
        self.complete = []
        self.logger = logging.getLogger(__name__)
    
    def on_locked(self):
        self.logger.log(('The queue is locked. Please check the logs. %s')
                % self.log_dir)
        return True
        
    def on_complete(self, job):
        self.complete.append(job)
        print('Complete: %s' % job.alias)

    def on_error(self, job):
        print('Error: %s' % job.alias)
        if job.attempts < job.MAX_RETRY:
            self.logger.log('Error: Job %s has failed, retrying (%s/%s)'
                    % (job.name, str(job.attempts), str(job.retry)))
            self.push(job)
        else:
            self.failed.append(job)
            self.logger.log('Error: Job %s has failed. Retried %s times.'
                    % (job.name, str(job.attempts)))
        
        
