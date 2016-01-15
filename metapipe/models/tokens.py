""" A set of tokens and convienence functions for input/output files. 

author: Brian Schrader
since: 2015-12-28
"""

from __future__ import print_function
from collections import namedtuple
import glob, re


file_pattern = 'metapipe.{}.output'


class PathToken(object):
    """ A model for a given path. """
    
    def __init__(self, alias, path):
        self.alias = alias
        self.path = path
        
    def __repr__(self):
        return '<Path {}: {}>'.format(self.alias, self.path)
    
    def __eq__(self, other):
        try:
            return (self.alias == other.alias or 
                self.path == other.path)
        except AttributeError:
            return False


class FileToken(object):
    """ An abc for input/output data classes. Provides various common 
    methods. 
    Warning: This class should not be used directly.
    """
    
    def __init__(self, alias, filename=''):
        self.alias = alias
        self.filename = filename
    
    def __eq__(self, other):
        try:
            return (self.alias == other.alias or 
                self.filename == other.filename)
        except AttributeError:
            return False
                

class Input(FileToken):
    """ A model of a single input to a given command. Input tokens can be 
    evaluated to obtain their actual filename(s).
    """
        
    def __init__(self, alias, filename='', and_or=''):
        super(Input, self).__init__(alias, filename)
        self.and_or = and_or

    def __repr__(self):
        eval = '?'
        try:
             eval = self.eval()
        except Exception:
            pass
        return '<Input: {}->[{}]{}>'.format(self.alias, eval, 
            ' _{}_'.format(self.and_or) if self.and_or else '')
    
    def eval(self):
        """ Evaluates the given input and returns a string containing the 
        actual filenames represented. If the input token represents multiple 
        independent files, then eval will return a list of all the files needed,
        otherwise it returns the filenames in a string.
        """
        if self.and_or == 'or':
            return self.files
        return ' '.join(self.files)
            
    @property         
    def files(self):
        """ Returns a list of all the files that match the given 
        input token.
        """
        try:
            return glob.glob(self.filename)
        except (AttributeError, TypeError):
            try:
                return glob.glob(self.alias)
            except (AttributeError, TypeError):
                return []
                
    @staticmethod  
    def from_string(string, _or=''):
        """ Parse a given string and turn it into an input token. """
        if _or:
            and_or = 'or'
        else:
            and_or = ''
        return Input(string, and_or=and_or)
        
        
class Output(FileToken):
    """ A model of a single output to a given command. Output tokens can be 
    evaluated to obtain their actual filename(s).
    """
    
    def __init__(self, alias, filename='', magic=''):
        super(Output, self).__init__(alias, filename)
        self.magic = self._clean_magic(magic)
        
    def __repr__(self):
        return '<Output: {}->[{}]{}>'.format(self.alias, self.eval(), 
            (' ' + self.magic) if self.magic else '')

    def eval(self):
        """ Returns a filename to be used for script output. """
        if self.magic:
            return ''
        if not self.filename:
            return file_pattern.format(self.alias)
        return self.filename
            
    def as_input(self):
        """ Returns an input token for the given output. """
        filename = self.filename if self.filename else self.magic
        return Input(self.alias, self.filename)
        
    def _clean_magic(self, magic):
        """ Given a magic string, remove the output tag designator. """
        if magic.lower() == 'o':
            return ''
        elif magic[:2].lower() == 'o:':
            return magic[2:]
        return magic

    @staticmethod  
    def from_string(string):
        """ Parse a given string and turn it into an output token. """
        return Output('', magic=string)
        
        
        
