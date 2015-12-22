""" A command model that can be easily transformed into jobs.

author: Brian Schrader
since: 2015-12-21
"""

import pickle


class Command(object):

    def __init__(self, alias, cmds=[], files=[], paths=[]):
        self.cmds = cmds
        self.alias = alias
        self.file_list = files        
        self.paths = paths

    def __repr__(self):
        return '<Command: {}>'.format(self.alias)

    def dependencies(self, all_commands):
        """ Given a list of all the commands to be executed, determine which 
        jobs the given job depends on.
        """
        pass
        
    def eval(self):
        """ Evaluate the given job and return a complete shell script to be run
        by the job manager.
        """
        pass  
