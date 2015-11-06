""" A parser and lexer for pipeline (.mp) files. """


from collections import namedtuple
import re

from models.job import Job

LexerResult = namedtuple('LexerResult', 'magic cmds files paths')
ParserResult = namedtuple('ParserResult', 'settings cmds')

File = namedtuple('File', 'filename alias number')


def lexer(text):
    """ Given a config string, return a list of commands for that pipeline. """
    magic = []
    cmds = []
    files = []
    paths = []
    mode = 'cmd'
    for line in text.split('\n'):
        line = line.strip()
        if line != '':
            if line[0:1] == '#{':     # Magic comments
                magic.append(line)
            elif line[0] != '#':
                if 'COMMANDS:' in line:
                    mode = 'cmd'
                elif mode == 'cmd':
                    cmds.append(line)
                elif 'FILES:' in line:
                    mode = 'file'
                elif mode == 'file':
                    files.append(line)
                elif 'PATHS:' in line:
                    mode = 'path'
                elif mode == 'path':
                    paths.append(line)
                else:
                    quit('Invalid config file.')

    return LexerResult(magic, files, paths, cmds)


def parser(lexerResult):
    """ Given the output of the lexer, parse the output and create the req
    commands. """
    magic = lexerResult.magic
    settings = parse_magic(magic) if len(magic) > 0 else DEFAULT_SETTINGS

    jobs = []
    # TODO: Finish


    return ParserResult(settings, cmds)


def parse_job(cmd, jobs=[], files=[], paths=[]):
    """ Break down the grammar of the cmd and fill in the jobs. """
    breakout_cmds = _split_params(cmd)

    def matches(a, files):
        # TODO: Add fuzzy matching
        return [f for f in files if f.alias == a][0]

    for new_cmd, aliases, output_pattern in breakout_cmds:
        new_files = map(lambda a: matches(a, files), aliases)
        depends_on = []
        # Fix this. It's ugly.
        [depends_on.extend(map(lambda a: matches(a, files), job.output_files)) for job in
            jobs]

        jobs.append(Job(new_cmd, new_cmd, new_files, depends_on))

    return jobs


def parse_file(file):
    """ Given a line containing a file definition/alias,
    return the file obj.
    """
    pass


def parse_magic(magics):
    """ Given the list of magic comments, return the full settings dict. """
    pass


def _split_params(cmd):
    """ Given a command, return a list of the commands and
    param lists.

    example
    -------
    _split_params('some cmd --some flag {1,2,3||3,4,5||4,5,4}')
    Yield this: 1,2,3 and 3,4,5 and 4,5,4
    """
    pattern = r'[^\\]\{([^\}]*)}'
    sub_pattern = r'\{([^\}]*)}'

    m = re.findall(pattern, cmd)
    input = [match for match in m if match[0:2] != 'o:']
    output = [match for match in m if match[0:2] == 'o:']

    if len(input) > 1 or len(output) > 1:
        print 'Ambigious pattern.', m, input, output
        raise ValueError

    breakout_cmds, params = [], []
    if len(input) > 0:
        for match in input[0].split('||'):
            params = match.split(',')
            cmd = cmd.replace(input[0], 'in')

            cmd = cmd.replace(output[0], 'out') if len(output) > 0 else cmd
            breakout_cmds.append((cmd, params, output))
    else:
        breakout_cmds.append((cmd, params, output))

    return breakout_cmdsza


