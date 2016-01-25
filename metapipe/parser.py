""" A parser and other parser related classes. """

import pyparsing

try:
    from models import Command, Input, Output, Grammar
    import models.command_template_factory as ctf
except ImportError:
    from metapipe.models import Command, Input, Output, Grammar
    import metapipe.models.command_template_factory as ctf


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
        grammar = Grammar.overall
        grammar.ignore(Grammar.comment)
        first_pass = grammar.parseString(self.string)
        lowered = { key.lower(): val for key, val in first_pass.iteritems() }

        try:
            txt_files = [''.join(f) for f in lowered['files'].asList()]
        except KeyError:
            txt_files = []
        try:
            txt_paths = [''.join(p) for p in lowered['paths'].asList()]
        except KeyError:
            txt_paths = []
        try:
            txt_commands = [''.join(c) for c in lowered['commands'].asList()]
        except KeyError:
            txt_commands = []
        
        try:
            self.commands = [Grammar.command.parseString(c) 
                for c in txt_commands]
        except pyparsing.ParseException:
            raise ValueError('Invalid command.')
        try:
            self.files = [Grammar.file.parseString(f) 
                for f in txt_files]
        except pyparsing.ParseException:
            raise ValueError('Invalid file.')
        try:
            self.paths = [Grammar.path.parseString(p) 
                for p in txt_paths]
        except pyparsing.ParseException:
            raise ValueError('Invalid path.')

        self.paths = ctf.get_paths(self.paths)
        self.files = ctf.get_files(self.files)
        
        self.paths.reverse()
        self.files.reverse()
        self.commands.reverse()
        
        return ctf.get_command_templates(self.commands, self.files[:], 
            self.paths[:])
