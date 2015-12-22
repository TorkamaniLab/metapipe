""" A parser and other parser related classes. """

try:
    from metapipe.grammar import Grammar
    from metapipe.models.command import Command
except ImportError:
    from grammar import Grammar
    from models.command import Command


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
        
        def matches_in(x, in_):
            for file in in_:
                if str(file) == str(x.alias):
                    return True
            return False

        final_commands =[]
        for i, command in enumerate(self.commands):
            for j, in_files in enumerate(command._in):
                input = filter(lambda x: matches_in(x, in_files), self.files)
                paths = filter(lambda x: any(True for cmd in command.command if x.alias in cmd.split()), self.paths)
                alias = '{}.{}'.format(i+1, j+1)
                final_commands.append(Command(alias, command, input, paths))

        return final_commands
