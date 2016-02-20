""" A parser and other parser related classes. """

import pyparsing

from .models import Command, Input, Output, Grammar
from .models import command_template_factory as ctf


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

        for c in txt_commands:
            try:
                self.commands.append(Grammar.command.parseString(c))
            except pyparsing.ParseException as e:
                raise ValueError('Invalid command. Verify line {} is '
                    'correct.\n{}'.format(e.lineno, c))

        for f in txt_files:
            try:
                self.files.append(Grammar.file.parseString(f))
            except pyparsing.ParseException as e:
                raise ValueError('Invalid file. Verify line {} is '
                    'correct.\n{}'.format(e.lineno, f))

        for p in txt_paths:
            try:
                self.paths.append(Grammar.path.parseString(p))
            except pyparsing.ParseException as e:
                raise ValueError('Invalid path. Verify line {} is '
                    'correct.\n{}'.format(e.lineno, p))

        self.paths = ctf.get_paths(self.paths)
        self.files = ctf.get_files(self.files)

        self.paths.reverse()
        self.files.reverse()
        self.commands.reverse()

        return ctf.get_command_templates(self.commands, self.files[:],
            self.paths[:])
