from . import Job, call


class PBSJob(Job):
    """ A job subclass for running tasks on a PBS queue. """

    def __init__(self, alias, command, depends_on=[], queue='work'):
        super(PBSJob, self).__init__(alias, command, depends_on)
        self.queue = queue
        self.id = None
        self.waiting = True     # The job has yet to be submitted.

    def submit(self):
        if self.attempts == 0:
            self.make()
        self.attempts += 1
        out, err = call(self.cmd)
        self.waiting = False
        self.id = out[:out.index('.')]

    @property
    def cmd(self):
        return ['qsub', self.filename]

    def is_running(self):
        """ Checks to see if the job is running. """
        qstat = self._grep_qstat('running')
        if qstat:
            return True
        return False

    def is_queued(self):
        """ Checks to see if the job is queued. """
        qstat = self._grep_qstat('queued')
        if qstat:
            return True
        return False

    def is_complete(self):
        """ Checks the job's output or log file to determing if
        the completion criteria was met.
        """
        qstat = self._grep_qstat('complete')
        comp = self._grep_status('complete')
        if qstat and comp:
            return True
        return False

    def is_fail(self):
        return not self.should_retry

    def is_error(self):
        """ Checks to see if the job errored out. """
        qstat = self._grep_qstat('error')
        err = self._grep_status('error')
        if qstat and err:
            return True
        return False

    def _grep_qstat(self, status_type='complete'):
        """ Greps qstat -e <job_id> for information from the queue.
        :paramsstatus_type: complete, queued, running, error, gone
        """
        args = "qstat -e {}".format(self.id).split()
        res, _ = call(args)
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

    def _grep_status(self, status_type):
        """ Greps through the job's current status to see if
        it returned with the requested status.
        status_type: complete, error
        """
        args = "qstat -f {}".format(self.id).split()
        res, _ = call(args)
        exit_status = [line for line in res.split('\n')
                if 'exit_status' in line]
        try:
            _, __, code = exit_status[0].split()
        except IndexError:
            code = None

        if status_type == 'complete' and code == '0':
            return True
        elif status_type == 'error' and code != '0':
            return True
        else:
            return False

