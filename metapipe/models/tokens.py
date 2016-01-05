""" A set of tokens and convienence functions for input/output files. 

author: Brian Schrader
since: 2015-12-28
"""

from __future__ import print_function
from collections import namedtuple
import glob, re


file_pattern = 'metapipe.{}.output'
input_token = namedtuple('token', 'alias filename')


class Token(object):
    """ An abc for input/output data classes. Provides various common 
    methods. 
    Warning: This class should not be used directly.
    """
    pass
                

class Input(Token):
    """ A model of a single input to a given command. Input tokens can be 
    evaluated to obtain their actual filename(s).
    """
    
    def __init__(self, file_parse_result):
        self.alias = file_parse_result.alias
        self.filename = file_parse_result.filename
        
    def __repr__(self):
        eval = '?'
        try:
             eval = self.eval()
        except Exception:
            pass
        return '<Input: {}->[{}]>'.format(self.alias, eval)
    
    def matches_output(self, output):
        """ Given an output token, determine if the output references this 
        input. 
        """
        try:
            return (self.alias == output.filename) 
        except AttributeError:
            return False
                                    
    def matches_command(self, command_alias):
        """ Given a command alias, determine if the input is dependent 
        on it. 
        """
        return command_alias == self._alias_step_marker
        
    def eval(self):
        """ Evaluates the given input and returns a string containing the 
        actual filenames represented.
        """ 
        try:
            return ' '.join(glob.glob(self.filename))
        except AttributeError:
            try:
                return ' '.join(glob.glob(self.alias))
            except AttributeError:
                raise ValueError('No such file found for pattern %s or %s' % (
                    self.filename, self.alias))
    
    @property
    def _alias_step_marker(self):
        """ Return the section of the input alias that cooresponds to the 
        command alias step.
        """
        try:
            return '.'.join(self.alias.split('.')[1:])
        except IndexError:
            return None
    
    
class Output(Token):
    """ A model of a single output to a given command. Output tokens can be 
    evaluated to obtain their actual filename(s).
    """

    def __init__(self, file_parse_result, command_alias=''):
        self.alias = file_parse_result
        self.filename = command_alias
        
    def __repr__(self):
        return '<Output: {}->[{}]>'.format(self.alias, self.eval())

    def eval(self):
        """ Returns a filename to be used for script output. """
        return file_pattern.format(self.filename)
            
    def as_input(self):
        """ Returns an input token for the given output. """
        return Input(self)
