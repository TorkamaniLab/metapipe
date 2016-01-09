""" A parser and other parser related classes. """

import pyparsing

try:
    from metapipe.grammar import Grammar
    from metapipe.models import Command, Input, Output, input_token
except ImportError:
    from grammar import Grammar
    from models import Command, Input, Output, input_token


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

        return [i for i in self._next_command()]
        
    def _next_command(self):
        """ Given the output of a parsed command, return a command object
        that represents that command.
        """
        def new_output(output_token, alias):
            try:
                output = Output(output_token.alias, command_alias=alias)
            except AttributeError:
                output = None
            return output

        for i, parsed_cmd in enumerate(self.commands):            
            input_sets, output_token = self._separate_in_out(parsed_cmd._in)
            paths = self._get_paths(parsed_cmd)

            if len(input_sets) == 0:
                alias = '{}.{}'.format(i+1, 0)
                command = Command(alias=alias, cmds=parsed_cmd, 
                    input=input_sets, output=new_output(output_token, alias), 
                    paths=paths)
                yield command
            
            skip_last = False 
            for j, input_files in enumerate(input_sets):
                if skip_last and j == len(input_sets) - 1: 
                    continue
                alias = '{}.{}'.format(i+1, j+1)
                command = Command(alias=alias, cmds=parsed_cmd, 
                    input=input_files, output=new_output(output_token, alias), 
                    paths=paths)
                    
                # If magic syntax, ignore next command or input.
                if command._or: 
                    skip_last = True
                if command._and: 
                    command.input = command.input[:-1]

                yield command
                       
    def _separate_in_out(self, filesets):
        """ Given a list of input and output filesets, return the input tokens
        and output token respectively.
        """
        if len(filesets) > 2:
            raise ValueError('Too many inputs/outputs.')

        input_sets, output_token = [], None
        for in_files in filesets:
            if self._is_output(in_files):
                output_token = self._get_output(in_files)
            else:
                input_sets = [self._get_input(in_set) for in_set in in_files]
        return input_sets, output_token

    def _get_paths(self, command):
        """ Given a command, return the paths that it requires. """
        return [path for cmd in command.command for path in self.paths 
            if path.alias in cmd.split()]
            
    def _get_input(self, filenames):
        """ Given a list of file aliases, return a list of matching 
        input file tokens. 
        """
        matches = []
        for f in self.files:
            if any(f.alias == filename for filename in filenames):
                matches.append(Input(f))
        
        known_aliases = { f.alias for f in self.files }
        for name in filenames:
            if name not in known_aliases:
                matches.append(Input(input_token(name, None)))
        return matches

    def _get_output(self, filenames):
        """ Given a list of file aliases, return a list of matching 
        output file tokens.
        """
        return Output(filenames[0][0])
        
    def _is_output(self, files):
        """ Determine if the given list is of output files. """
        try:
            return files[0][0][0] == 'o'
        except IndexError:
            return False
