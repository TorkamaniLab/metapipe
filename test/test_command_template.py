""" Tests for the output of the command template. """

import sure

from .fixtures import *

from metapipe.parser import Parser
from metapipe.models import *


def test_eval_1():
    parser = Parser(overall)

    templates = parser.consume()

    vals = [CommentToken(['#PBS_O_WORKDIR=~/someuser']),
        CommentToken(['set -e;']),
        CommentToken(['module load python']),
        CommentToken(['# do something']),
        PathToken('python', '/usr/bin/python'), 'somescript.py', '-i',
        Input('1', 'somefile.1'),
        Input('2', 'somefile.2'),
        Input('3', 'somefile.3'),
        '-o', Output('1.1', 'metapipe.1.1.output'),
        '-fgh', 'somefile.txt']
    cmd = templates[0].eval()[0]
    for i, part in enumerate(cmd.parts):
        vals[i].should.equal(part)


def test_eval_2():
    parser = Parser(overall)
    templates = parser.consume()

    vals = [CommentToken(['#PBS_O_WORKDIR=~/someuser']),
        CommentToken(['set -e;']),
        CommentToken(['module load python']),
        CommentToken(['# do something']),
        PathToken('python', '/usr/bin/python'), 'somescript.py', '-i',
        Input('4', 'somefile.4'),
        Input('5', 'somefile.5'),
        Input('6', 'somefile.6'),
        '-o', Output('1.2', 'metapipe.1.2.output'),
        '-fgh', 'somefile.txt']
    cmd = templates[0].eval()[1]
    for i, part in enumerate(cmd.parts):
        vals[i].should.equal(part)


def test_eval_multiple_inputs1():
    parser = Parser(multiple_inputs)

    templates = parser.consume()

    vals = ['bash', 'somescript',
        Input('1', 'somefile.1'), '--conf',
        Input('4', 'somefile.4'),
        '>', Output('1.1', 'metapipe.1.1.output')]
    cmd = templates[0].eval()[0]
    for i, part in enumerate(cmd.parts):
        vals[i].should.equal(part)


def test_eval_multiple_inputs2():
    parser = Parser(multiple_inputs)

    templates = parser.consume()

    vals = ['bash', 'somescript',
        Input('2', 'somefile.2'), '--conf',
        Input('5', 'somefile.5'),
        '>', Output('1.2', 'metapipe.1.2.output')]
    cmd = templates[0].eval()[1]
    for i, part in enumerate(cmd.parts):
        vals[i].should.equal(part)


def test_eval_multiple_inputs3():
    parser = Parser(multiple_inputs)

    templates = parser.consume()

    vals = ['bash', 'somescript',
        Input('3', 'somefile.3'), '--conf',
        Input('6', 'somefile.6'),
        '>', Output('1.3', 'metapipe.1.3.output')]
    cmd = templates[0].eval()[2]
    for i, part in enumerate(cmd.parts):
        vals[i].should.equal(part)


def test_eval_multiple_inputs4():
    parser = Parser(multiple_inputs)

    templates = parser.consume()

    vals = ['python', 'somescript.py',
        Input('1', 'somefile.1'),
        Input('2', 'somefile.2'),
        Input('3', 'somefile.3'), '--conf',
        Input('4', 'somefile.4'),
        Input('5', 'somefile.5'),
        Input('6', 'somefile.6'),
        '>', Output('2.1', 'metapipe.2.1.output')]
    cmd = templates[1].eval()[0]
    for i, part in enumerate(cmd.parts):
        vals[i].should.equal(part)


def test_eval_magic_input():
    parser = Parser(magic_inputs)

    templates = parser.consume()

    vals = ['bash', 'somescript',
        Input('*.counts', 'somefile.1'),
        '>', Output('1.1', 'metapipe.1.1.output')]
    cmd = templates[0].eval()[0]
    for i, part in enumerate(cmd.parts):
        vals[i].should.equal(part)


def test_multiple_outputs():
    parser = Parser(multiple_outputs)

    templates = parser.consume()

    vals = ['bash', 'somescript',
        Input('1', 'somefile.1'), '--log',
        Output('1.1-1', 'metapipe.1.1-1.output'), '-r',
        Output('1.1-2', 'metapipe.1.1-2.output')]

    cmd = templates[0].eval()[0]
    for i, part in enumerate(cmd.parts):
        vals[i].should.equal(part)



def test_another_sample_pipeline():
    parser = Parser(another_sample)

    templates = parser.consume()


    vals = [CommentToken(['#', ' Trimmomatic']),'java', '-jar',
        PathToken('trimmomatic', 'Trimmomatic-0.35/trimmomatic-0.35.jar>'),
        'PE', Input('1'), Input('2'),
        Output('1.1-1', 'metapipe.1.output'), Output('1.1-2', 'metapipe.1.output'),
        Output('1.1-3', 'metapipe.1.output'), Output('1.1-4', 'metapipe.1.output'),
        'ILLUMINACLIP:Trimmomatic-0.35/adapters/TruSeq3-PE.fa:2:30:10:2:true',
        'LEADING:3', 'TRAILING:3'
    ]

    cmd = templates[0].eval()[0]
    for i, part in enumerate(cmd.parts):
        vals[i].should.equal(part)


def test_another_sample_pipeline_1():
    parser = Parser(another_sample)

    templates = parser.consume()


    vals = [CommentToken(['#', ' Unzip the outputs from trimmomatic']),
        'gzip', '--stdout', '-d',
        Input('1.1-1'), '>',
        Output('2.1', 'metapipe.2.1.output')]

    cmd = templates[1].eval()[0]
    for i, part in enumerate(cmd.parts):
        vals[i].should.equal(part)


def test_another_sample_pipeline_2():
    parser = Parser(another_sample)

    templates = parser.consume()


    vals = [CommentToken(['#', ' Cutadapt']),
        CommentToken(['#', ' cutadapt needs unzipped fastq files']),
        PathToken('cutadapt', '~/.local/bin/cutadapt'), '--cut', '7',
        '-o', Output('3.1', 'metapipe.3.1.output'), Input('2.*')]

    cmd = templates[2].eval()[0]
    for i, part in enumerate(cmd.parts):
        vals[i].should.equal(part)


def test_long_running_1():
    parser = Parser(long_running)

    templates = parser.consume()


    vals = ['cat', Input('1', 'somefile.1'), '>',
        Output('1.1', 'metapipe.1.1.output'), '&&', 'sleep', '1']

    cmd = templates[0].eval()[0]
    for i, part in enumerate(cmd.parts):
        vals[i].should.equal(part)


def test_long_running_2():
    parser = Parser(long_running)

    templates = parser.consume()


    vals = ['cat', Input('1.1', 'metapipe.1.1.output'), '&&', 'sleep', '1']

    cmd = templates[1].eval()[0]
    for i, part in enumerate(cmd.parts):
        vals[i].should.equal(part)


def test_output_file_name():
    parser = Parser(full_output_file_name)

    templates = parser.consume()


    vals = ['gzip', '--stdout', Input('1', 'somefile.1'), '>',
        Output('1.1', 'metapipe.1.1.output.gz')]

    cmd = templates[0].eval()[0]
    for i, part in enumerate(cmd.parts):
        vals[i].should.equal(part)

def test_magical_glob():
    parser = Parser(magical_glob)
    templates = parser.consume()

    vals = ['cat', Input('1.*', ''), '>',
        Output('2.1', 'mp.2.1.output')]

    cmd = templates[1].eval()[0]
    for i, part in enumerate(cmd.parts):
        vals[i].should.equal(part)

def test_magical_glob():
    parser = Parser(magical_glob2)
    templates = parser.consume()

    vals = ['cat', Input('1.*', ''), '>',
        Output('2.1', 'mp.2.1.output')]

    cmd = templates[1].eval()[0]
    for i, part in enumerate(cmd.parts):
        vals[i].should.equal(part)
