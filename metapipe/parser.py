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

    def consume(self, cwd=None):
        """ Converts the lexer tokens into valid statements. This process
        also checks command syntax.
        """
        first_pass = Grammar.overall.parseString(self.string)
        lowered = { key.lower(): val for key, val in first_pass.iteritems() }

        self.commands = ['\n'.join(self._get('commands', lowered))]
        self.job_options = self._get('job_options', lowered)
        self.global_options = self._get('options', lowered)

        self.files = self._get('files', lowered)
        self.paths = self._get('paths', lowered)

        self.files = self._parse(self.files, Grammar.file, True)
        self.paths = self._parse(self.paths, Grammar.path, True)
        self.job_options = self._parse(self.job_options, Grammar.line)

        try:
            command_lines = self._parse(self.commands, Grammar.command_lines)[0]
        except IndexError:
            raise ValueError('Did you write any commands?')

        self.commands = []
        for command_line in command_lines:
            comments, command = command_line
            self.commands.append([comments.asList(),
                self._parse([''.join(command)], Grammar.command)])

        self.job_options = [opt.asList() for opt in self.job_options]

        self.paths = ctf.get_paths(self.paths)
        self.files = ctf.get_files(self.files)

        self.paths.reverse()
        self.files.reverse()
        self.commands.reverse()

        return ctf.get_command_templates(self.commands, self.files[:],
            self.paths[:], self.job_options)

    def _get(self, key, parser_result):
        """ Given a type and a dict of parser results, return
        the items as a list.
        """
        try:
            list_data = parser_result[key].asList()
            if any(isinstance(obj, str) for obj in list_data):
                txt_lines = [''.join(list_data)]
            else:
                txt_lines = [''.join(f) for f in list_data]
        except KeyError:
            txt_lines = []
        return txt_lines

    def _parse(self, lines, grammar, ignore_comments=False):
        """ Given a type and a list, parse it using the more detailed
        parse grammar.
        """
        results = []
        for c in lines:
            if c != '' and not (ignore_comments and c[0] == '#'):
                try:
                    results.append(grammar.parseString(c))
                except pyparsing.ParseException as e:
                    raise ValueError('Invalid syntax. Verify line {} is '
                        'correct.\n{}\n\n{}'.format(e.lineno, c, e))
        return results
