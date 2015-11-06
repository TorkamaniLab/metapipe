""" A job model for submitting work to the queue.

author: Brian Schrader
since: 2015-08-27
"""


import os
from subprocess import Popen, PIPE


stdout = '/tmp/queuemanager.out'
stderr = '/tmp/queuemanager.err'
RETRY_ATTEMPTS = 2


def call(args, remote=None):
    """ Calls the given arguments in a seperate process
    and returns the contents of standard out.
    """
    err = open(stderr, 'w+')
    with open(stdout, 'w+') as f:
        p = Popen(args, stdout=f, stderr=err)
        p.communicate()
        f.seek(0)
        out = f.read()
    err.close()
    return out


class Job(object):

    def __init__(self, name, raw_cmd, input_files, output_files=[], depends_on=[], queue='work'):
        """ Create an new job with the given name, and command.
        If the job depends on another job, give the names of the jobs
        it depends on.
        If the job could exit erroniously, then provide a pattern
        found in the completion_file that would indicate completion.
            i.e. Upon completion the job prints 'Done!' to a log file
            include 'Done!' as the completion criteria.
        """
        self.depends_on = depends_on
        self.raw_cmd = raw_cmd
        self.name = name
        self.input_files = input_files
        self.output_files = output_files
        self.queue = queue
        self.id = None
        self.waiting = True     # The job has yet to be submitted.
        self.attempts = 0
        self.retry = RETRY_ATTEMPTS

        with open(stdout, 'w') as f:
            f.write('')

    def __repr__(self):
        return '<Job: {}>'.format(self.cmd)

    def submit(self):
        args = ['qsub'] + [self.job_cmd]
        self.attempts += 1
        out = call(args, remote=self.remote)
        self.waiting = False
        self.id = out[:out.index('.')]

    def grep_qstat(self, status_type='complete'):
        """ Greps qstat -e <job_id> for information from the queue.
        :paramsstatus_type: complete, queued, running, error, gone
        """
        args = ("qstat -e %s" % self.id).split()
        res = call(args)
        if res == '': return False
        res = res.split('\n')[2].split()[4]

        if status_type == 'complete' and res == 'C':
            return True
        elif status_type == 'error' and (res == 'E' or res == 'C'):
            return True
        elif status_type == 'running' and res == 'R':
            return True
        elif status_type == 'queued' and res == 'Q':
            return True
        elif status_type == 'gone' and 'unknown job id' in str(res).lower():
            return True
        else:
            return False

    def grep_status(self, status_type):
        """ Greps through the job's current status to see if
        it returned with the requested status.
        status_type: complete, error
        """
        args = ("qstat -f %s" % self.id).split()
        res = call(args)
        exit_status = [line for line in res.split('\n')
                if 'exit_status' in line]
        if len(exit_status) > 0:
            _, __, code = exit_status[0].split()
            if status_type == 'complete' and code == '0':
                return True
            elif status_type == 'error' and code != '0':
                return True
        return False

    @property
    def cmd(self):
        return self.raw_cmd.replace('{in}', ' '.join([f.filename for f in
            self.input_files]))

    @property
    def running(self):
        """ Checks to see if the job is running. """
        qstat = self.grep_qstat('running')
        if qstat:
            return True
        return False

    @property
    def queued(self):
        """ Checks to see if the job is queued. """
        qstat = self.grep_qstat('queued')
        if qstat:
            return True
        return False

    @property
    def complete(self):
        """ Checks the job's output or log file to determing if
        the completion criteria was met.
        """
        qstat = self.grep_qstat('complete')
        comp = self.grep_status('complete')
        if qstat and comp:
            return True
        return False

    @property
    def error(self):
        """ Checks to see if the job errored out. """
        qstat = self.grep_qstat('error')
        err = self.grep_status('error')
        if qstat and err:
            return True
        return False
