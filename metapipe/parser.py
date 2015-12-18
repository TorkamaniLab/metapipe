""" A parser and other parser related classes. """

from __future__ import print_function

from pyparsing import originalTextFor

try:
    from metapipe.grammar import Grammar 	# Python3
except ImportError:
    from grammer import Grammar


class Parser(object):

    def __init__(self, string):
        self.string = string
        self.commands = []
        self.paths = []
        self.files = []

    def consume(self):
        """ Converts the lexer tokens into valid statements. This process
        also checks command syntax.
        """
        first_pass = Grammar.overall.parseString(self.string)
        lowered = { key.lower(): val for key, val in first_pass.iteritems() }
        
        txt_files = [''.join(f) for f in lowered['files'].asList()]
        txt_paths = [''.join(p) for p in lowered['paths'].asList()]
        txt_commands = [''.join(c) for c in lowered['commands'].asList()]
        
        self.commands = [Grammar.command.parseString(c) for c in txt_commands]
        self.files = [Grammar.file.parseString(f) for f in txt_files]
        self.paths = [Grammar.path.parseString(p) for p in txt_paths]
