""" A command model that lazily evaluates itself into jobs for the queue.

author: Brian Schrader
since: 2015-08-27
"""


from job import Job


class Command(Job):
    """
    """
    def __init__(self, name, job_cmd, input_files, output_files=[], depends_on=[], queue='work'):
        self.depends_on = depends_
        self.job_cmd = job_cmd
        self.name = name
        self.input_files = input_files
        self.output_files = output_files
        self.queue = queue
        self.id = None
        self.waiting = True     # The job has yet to be submitted.
        self.attempts = 0
        self.retry = RETRY_ATTEMPTS

        super()._init__()

    def __repr__(self):
        return '<Command: {}>'.format(self.cmd)

    def submit(self):
        for a in super().submit(): pass

    @property
    def cmd(self):
        return make_cmd()



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

    return breakout_cmds




