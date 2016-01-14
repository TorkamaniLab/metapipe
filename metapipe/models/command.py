""" A command model that can be easily transformed into jobs.

author: Brian Schrader
since: 2015-12-21
"""


class Command(object):

    def __init__(self, alias, parts=[], dependencies=[]):
        self.parts = parts
        self.dependencies = dependencies
        
    def __repr__(self):
        return '<Command: {}>'.format(self.alias)
        
    def eval(self):
        """ Evaluate the given job and return a complete shell script to be run
        by the job manager.
        """
        eval = []
        for part in self.parts:
            try: 
                result = part.eval()
            except AttributeError:
                result = part
            eval.append(result)
        return ' '.join(eval)
