""" A series of mocks for metapipe. """

from metapipe.models import Job


class MockJob(Job):
    
    def __init__(self, alias, command, depends_on=[]):
        super(MockJob, self).__init__(alias, command, depends_on=[])
        self._submitted = False        
        self._done = False        

    def __repr__(self):
        return '<MockJob: {}>'.format(self.cmd)

    def make(self):
        # Nulled
        pass

    def submit(self):
        self._submitted = True
        
    def is_running(self):
        if self._submitted:
            self._done = True
            self._submitted = False
            return True
        return False

    def is_queued(self):
        return False
        
    def is_complete(self):
        return self._done

    def is_error(self):
        return False
