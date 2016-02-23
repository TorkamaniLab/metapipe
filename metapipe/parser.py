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

        self.files = self._get('files', lowered, Grammar.file)
        self.paths = self._get('paths', lowered, Grammar.path)
        self.commands = self._get('commands', lowered, Grammar.command)

        self.paths = ctf.get_paths(self.paths)
        self.files = ctf.get_files(self.files)

        self.paths.reverse()
        self.files.reverse()
        self.commands.reverse()

        return ctf.get_command_templates(self.commands, self.files[:],
            self.paths[:])

    def _get(self, key, parser_result, grammar):
        """ Given a type and a dict of parser results, parse the overall results
        using the more detailed parse grammar.
        """
        try:
            txt_lines = [''.join(f) for f in parser_result[key].asList()]
        except KeyError:
            txt_lines = []

        results = []
        for c in txt_lines:
            try:
                results.append(grammar.parseString(c))
            except pyparsing.ParseException as e:
                raise ValueError('Invalid {}. Verify line {} is '
                    'correct.\n{}'.format(key, e.lineno, c))
        return results
