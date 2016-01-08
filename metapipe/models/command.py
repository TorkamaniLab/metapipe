""" A command model that can be easily transformed into jobs.

author: Brian Schrader
since: 2015-12-21
"""

from __future__ import print_function


path_frmt = ' {} '


class Command(object):

    def __init__(self, alias, cmds=[], paths=[], input=[], output=None):
        self.cmds = cmds
        self.alias = alias
        self.paths = paths
        self.input = input
        self.output = output
        
        self.deps = None
        
    def __repr__(self):
        return '<Command: {}>'.format(self.alias)
        
    @property
    def _or(self):
        return len(self.cmds._or) > 0

    @property
    def _and(self):
        return len(self.cmds._in[0][0]._and) > 0

    def find_dependencies(self, all_commands):
        """ Given a list of all the commands to be executed, determine which 
        jobs the given job depends on.
        """
        self.deps = []
        for command in all_commands:
            for i in range(len(self.input)):
                input = self.input[i]
                if (input.matches_output(command.output) 
                        or input.matches_command(command.alias)):
                    self.deps.append(command)
                    self.input.append(command.output.as_input())
        return self.deps
        
    def eval(self):
        """ Evaluate the given job and return a complete shell script to be run
        by the job manager.
        """
        if self.deps is None:
            raise ValueError(
                'Dependencies must be calculated before command can be evaluated.')
        eval = []
        for c in list(self.cmds):
            if not isinstance(c, str):
                for alias in c:
                    token = self._eval_alias(alias)
                    if token is not None:
                        eval.append(token.eval())
            else:
                eval.append(c)
        return self._eval_paths(' '.join(str(c) for c in eval))
        
    def _eval_paths(self, commands):
        """ Given a command string, replace the paths. """
        new_commands = []
        if len(self.paths) == 0:
            return commands

        for part in commands.split():
            for path in self.paths:
                if path.alias == part:
                    new_commands.append(path.path)
                else:
                    new_commands.append(part)
        return ' '.join(new_commands)
        
    def _eval_alias(self, alias):
        """ Given an alias, find the input/output token that 
        cooresponds. 
        """
        token = None
        for i in self.input:
            if i.alias == alias:
                token = i
            else:
                for dep in self.deps:
                    if alias == dep.output.alias:
                         token = dep.output
                    elif alias == dep.output.filename:
                        token = dep.output
        if alias.startswith('o'):
            token = self.output  
                                               
        return token

