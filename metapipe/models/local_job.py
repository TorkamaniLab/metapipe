import threading

from . import Job, call


LOCAL_LOG_FORMAT = '{}_{}'


class LocalJobCallThread(threading.Thread):
    """ A class that handles calling subprocesses in seperate threads. """

    def __init__(self, callable, *args, **kwargs):
        self.stdout = None
        self.stderr = None
        self.callable = callable
        self.args = args
        self.kwargs = kwargs
        threading.Thread.__init__(self)
        self.stdout = None
        self.stderr = None

    def run(self):
        self.stdout, self.stderr = self.callable(*self.args, **self.kwargs)


class LocalJob(Job):
    """ A subclass of job for local calculations. """

    def __init__(self, alias, command, depends_on=[], shell='bash'):
        super(LocalJob, self).__init__(alias, command, depends_on)
        self.shell = shell
        self._task = None
        self._err = False

    def __repr__(self):
        return '<LocalJob: {}>'.format(self.cmd)

    @property
    def cmd(self):
        return [self.shell, self.filename]

    def submit(self):
        self.make()
        self.attempts += 1
        self._task = LocalJobCallThread(call, self.cmd)
        self._task.start()

    def is_running(self):
        try:
            return self._task.is_alive()
        except AttributeError:
            return False

    def is_queued(self):
        """ Returns False since local jobs are not submitted to an
        external queue.
        """
        return False

    def is_complete(self):
        try:
            if not self._task.is_alive():
                self._task.join()
                self._write_log()
                return True
        except AttributeError:
            pass
        return False

    def is_error(self):
        """ Checks to see if the job errored out. """
        try:
            if self._task.is_alive():
                if len(self._task.stderr.readlines()) > 0:
                    self._task.join()
                    self._write_log()
                    return True
        except AttributeError:
            pass
        return False

    def is_fail(self):
        return not self.should_retry

    def _write_log(self):
        alias = Job.JOB_FILE_PATTERN.format(self.alias)
        outlog, errlog = (LOCAL_LOG_FORMAT.format(alias, 'stdout'),
            LOCAL_LOG_FORMAT.format(alias, 'stderr'))

        with open(outlog, 'w+') as f:
            f.write(str(self._task.stdout))
        with open(errlog, 'w+') as f:
            f.write(str(self._task.stderr))

