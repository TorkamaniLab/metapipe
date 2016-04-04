""" A pipeline that generates analysis pipelines.

author: Brian Schrader
since: 2015-12-22
"""

from __future__ import print_function

import argparse, pickle, os, sys

import pyparsing

from .parser import Parser
from .models import Command, LocalJob, PBSJob, \
    HtmlReportingJobQueue, TextReportingJobQueue
from .runtime import Runtime
from .template import make_script


__version__ = '1.2'


PIPELINE_ALIAS = "metapipe.queue.job"

JOB_TYPES = {
    'local': LocalJob,
    'pbs': PBSJob
}

QUEUE_TYPES = {
    'text': TextReportingJobQueue,
    'html': HtmlReportingJobQueue
}


def main():
    """ Parses the command-line args, and calls run. """
    parser = argparse.ArgumentParser(
        description='A pipeline that generates analysis pipelines.')
    parser.add_argument('input', nargs='?',
                   help='A valid metapipe configuration file.')
    parser.add_argument('-o', '--output',
                   help='An output destination. If none is provided, the '
                   'results will be printed to stdout.',
                   default=sys.stdout)
    parser.add_argument('-t', '--temp',
                   help='A desired metapipe binary file. This is used to store '
                   'temp data between generation and execution. '
                   '(Default: "%(default)s")', default='.metapipe')
    parser.add_argument('-s', '--shell',
                   help='The path to the shell to be used when executing the '
                   'pipeline. (Default: "%(default)s)"',
                   default='/bin/bash')
    parser.add_argument('-r', '--run',
                   help='Run the pipeline as soon as it\'s ready.',
                   action='store_true')
    parser.add_argument('-j', '--job-type',
                   help='The destination for calculations (i.e. local, a PBS '
                   'queue on a cluster, etc).\nOptions: {}. '
                   '(Default: "%(default)s)"'.format(JOB_TYPES.keys()),
                   default='local')
    parser.add_argument('--report-type',
                   help='The output report type. By default metapipe will '
                   'print updates to the console. \nOptions: {}. '
                   '(Default: "%(default)s)"'.format(QUEUE_TYPES.keys()),
                   default='text')
    parser.add_argument('-v','--version',
                    help='Displays the current version of the application.',
                    action='store_true')
    args = parser.parse_args()

    if args.version:
        print('Version: {}'.format(__version__))
        sys.exit(0)

    try:
        with open(args.input) as f:
            config = f.read()
    except IOError:
        print('No valid config file found.')
        return -1

    run(config, args.output, args.job_type, args.report_type, args.shell,
        args.temp, args.run)


def run(config, output=sys.stdout, job_type='local', report_type='text', shell='/bin/bash',
        temp='.metapipe', run_now=False):
    """ Create the metapipe based on the provided input. """
    parser = Parser(config)
    try:
        command_templates = parser.consume()
    except ValueError as e:
        raise SyntaxError('Invalid config file. \n%s' % e)

    queue_type = QUEUE_TYPES[report_type]
    pipeline = Runtime(command_templates, queue_type, JOB_TYPES, job_type)

    with open(args.temp, 'wb') as f:
        pickle.dump(pipeline, f, 2)
    script = make_script(temp=os.path.abspath(temp), shell=shell)

    if args.run:
        output = output if output != sys.stdout else PIPELINE_ALIAS
        submit_job = make_submit_job(shell, output, job_type)
        submit_job.submit()

    try:
        f = open(output, 'w')
        output = f
    except TypeError:
        pass

    output.write(script)
    f.close()


def make_submit_job(shell, output, job_type):
    """ Preps the metapipe main job to be submitted. """
    run_cmd = [shell, output]
    submit_command = Command(alias=PIPELINE_ALIAS, cmds=run_cmd)
    submit_job = get_job(submit_command, job_type)
    submit_job.make()
    return submit_job


if __name__ == '__main__':
    main()
