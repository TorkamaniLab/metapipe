""" A parser and lexer for pipeline (.mp) files. """


from collections import namedtuple


LexerResult = namedtuple('LexerResult', 'magic cmds files paths')
ParserResult = namedtuple('ParserResult', 'settings cmds')

File = namedtuple('File', 'filename alias number')

def lexer(text):
    """ Given a config string, return a list of commands for that pipeline. """
    magic = []
    cmds  = []
    files = []
    paths = []
    mode  = 'cmd'

    for line in text.split('\n'):
        line = line.strip()

        if line != '':
            if line[0:1] == '#{':       # Magic comments
                magic.append(line)
            elif line[0] == '#':
                pass

            elif line[0] == '>':        # Mode detection 
                if 'COMMANDS:' in line:
                    mode = 'cmd'
                elif 'FILES:' in line:
                    mode = 'file'
                elif 'PATHS:' in line:
                    mode = 'path'
                else:
                    quit('Invalid config file: '+line)
            else:
                if mode == 'cmd':
                    cmds.append(line)
                elif mode == 'file':
                    files.append(line)
                elif mode == 'path':
                    paths.append(line)
                else:
                    quit('Invalid config file.')

    return LexerResult(magic, cmds, files, paths)


def parser(lexerResult):
    """ Given the output of the lexer, parse the output and create the req
    commands. """
    magic = lexerResult.magic
    settings = parse_magic(magic) if len(magic) > 0 else DEFAULT_SETTINGS

    cmds = []
    # TODO: Finish

    return ParserResult(settings, cmds)

def parse_cmd(cmd, files, paths=[]):
    """ Given a command, the list of files, and the paths for the pipeline,
    construct the actual CLI command to run. """






    pass


def parse_file(file):
    """ Given a line containing a file definition/alias,
    return the file obj.
    """
    pass


def parse_magic(magics):
    """ Given the list of magic comments, return the full settings dict. """
    pass










