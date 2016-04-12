""" A basic job model, and local job implementation.

author: Brian Schrader
since: 2016-01-04
"""

import os
from subprocess import Popen, PIPE


def call(args, stdout=PIPE, stderr=PIPE):
    """ Calls the given arguments in a seperate process
    and returns the contents of standard out.
    """
    p = Popen(args, stdout=stdout, stderr=stderr)
    out, err = p.communicate()

    try:
        return out.decode(sys.stdout.encoding), err.decode(sys.stdout.encoding)
    except Exception:
        return out, err


class Job(object):
    """ A template job class that just runs the given command script locally.
    To make your own custom jobs, subclass this Job and override the status methods, the submit method, and cmd property.

    Submitting a job cannot block execution. The submit call should return
    immediately so that other jobs can be executed, and tracked.
    """

    JOB_FILE_PATTERN = 'metapipe.{}.job'
    MAX_RETRY = 5

    def __init__(self, alias, command, depends_on=[]):
        """ Create an new job with the given name, and command. """
        self.command = command
        self.depends_on = depends_on
        self.alias = alias
        self.attempts = 0
        self.filename = self.JOB_FILE_PATTERN.format(self.alias)

    def __repr__(self):
        return '<Job: {}>'.format(self.cmd)

    def __cmp__(self, other):
        return cmp(self.alias, other.alias)

    def make(self):
        """ Evaluate the command, and write it to a file. """
        eval = self.command.eval()
        with open(self.filename, 'w') as f:
            f.write(eval)

    @property
    def should_retry(self):
        return self.attempts < self.MAX_RETRY

    # Override these...

    @property
    def cmd(self):
        """ Returns the command needed to submit the calculations.
        Normally, this would be just running the command, however if
        using a queue system, then this should return the command to
        submit the command to the queue.
        """
        pass

    def submit(self):
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

    def is_failed(self):
        """ Checks to see if the job has failed. This is usually if the job
        should not be resubmitted.
        """
        pass


