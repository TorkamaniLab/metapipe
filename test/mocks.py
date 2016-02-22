""" A series of mocks for metapipe. """

from metapipe.models import Job


class MockJob(Job):

    def __init__(self, alias, command, depends_on=[]):
        super(MockJob, self).__init__(alias, command, depends_on)
        self._submitted = False
        self._done = False
        self._step = 0

    def __repr__(self):
        return '<MockJob: {}>'.format(self.alias)

    def submit(self):
        self._step += 1

    def is_running(self):
        self._step += 1
        return self._step > 1 and self._step < 10

    def is_queued(self):
        return False

    def is_complete(self):
        return self._step > 10

    def is_fail(self):
        return False
