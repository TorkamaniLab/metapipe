""" Tests for the output of the command template factory. """

import sure

from .fixtures import *

from metapipe.parser import Parser
from metapipe.models import *


def test_multiple_inputs():
    parser = Parser(multiple_inputs)

    cmds = parser.consume()
    for i, part in enumerate(cmds[0].parts):
        multiple_input_vals[i].should.equal(part)


def test_multiple_outputs():
    parser = Parser(multiple_outputs)

    cmds = parser.consume()
    for i, part in enumerate(cmds[0].parts):
        multiple_output_vals[i].should.equal(part)


def test_full_sample_pipeline():
    parser = Parser(full_sample_pipeline)

    cmds = parser.consume()

    vals = [CommentToken(['#', ' Trimmomatic']), 'java', '-jar',
        PathToken('trimmomatic', 'Trimmomatic-0.35/trimmomatic-0.35.jar>'),
        'PE', [[Input('*R1_001.fastq.gz')]], [[Input('*R2_001.fastq.gz')]],
        Output('1', 'metapipe.1.output'), Output('1', 'metapipe.1.output'),
        Output('1', 'metapipe.1.output'), Output('1', 'metapipe.1.output'),
        PathToken('illuminaclip', 'ILLUMINACLIP:/gpfs/home/bhuvan/Programs/Trimmomatic-0.32/adapters/TruSeq3-PE.fa:2:30:10:2:true'),
        'LEADING:3', 'TRAILING:3'
    ]

    for i, part in enumerate(cmds[0].parts):
        vals[i].should.equal(part)


def test_another_sample_pipeline():
    parser = Parser(another_sample)

    cmds = parser.consume()


    vals = [CommentToken(['#', ' Trimmomatic']), 'java', '-jar',
        PathToken('trimmomatic', 'Trimmomatic-0.35/trimmomatic-0.35.jar>'),
        'PE', [[Input('1')]], [[Input('2')]],
        Output('1', 'metapipe.1.output'), Output('1', 'metapipe.1.output'),
        Output('1', 'metapipe.1.output'), Output('1', 'metapipe.1.output'),
        'ILLUMINACLIP:Trimmomatic-0.35/adapters/TruSeq3-PE.fa:2:30:10:2:true',
        'LEADING:3', 'TRAILING:3'
    ]

    for i, part in enumerate(cmds[0].parts):
        vals[i].should.equal(part)


def test_another_sample_pipeline_1():
    parser = Parser(another_sample)

    cmds = parser.consume()


    vals = [CommentToken(['#', ' Unzip the outputs from trimmomatic']),
        'gzip', '--stdout', '-d',
        [[Input('1.1-1')], [Input('1.1-3')]], '>',
        Output('2', 'metapipe.2.output')]

    for i, part in enumerate(cmds[1].parts):
        vals[i].should.equal(part)


def test_another_sample_pipeline_2():
    parser = Parser(another_sample)

    cmds = parser.consume()


    vals = [CommentToken(['#', ' Cutadapt']),
        CommentToken(['#', ' cutadapt needs unzipped fastq files']),
        PathToken('cutadapt', '~/.local/bin/cutadapt'), '--cut', '7', '-o',
        Output('3', 'metapipe.3.output'),
            [[Input('2.*')]]]

    for i, part in enumerate(cmds[2].parts):
        vals[i].should.equal(part)


def test_long_running_1():
    parser = Parser(long_running)

    cmds = parser.consume()


    vals = ['cat', [[Input('1', 'somefile.1')],
        [Input('2', 'somefile.2')], [Input('3', 'somefile.3')],
        [Input('4', 'somefile.4')]], '>',
        Output('1', 'metapipe.1.output'), '&&', 'sleep', '1']

    for i, part in enumerate(cmds[0].parts):
        vals[i].should.equal(part)


def test_long_running_2():
    parser = Parser(long_running)

    cmds = parser.consume()


    vals = ['cat', [[Input('1.1')], [Input('1.2')]], '&&', 'sleep', '1']

    for i, part in enumerate(cmds[1].parts):
        vals[i].should.equal(part)


def test_long_running_2_deps():
    parser = Parser(long_running)

    cmds = parser.consume()
    cmds[1]._dependencies.should.have.length_of(1)


def test_one_step_pipeline():
    parser = Parser(one_step_pipeline)
    cmds = parser.consume()

    vals = ['cut', 'somefile', '>', 'anotherfile']
    for i, part in enumerate(cmds[0].parts):
        vals[i].should.equal(part)


def test_one_step_pipeline():
    parser = Parser(one_step_pipeline)
    cmds = parser.consume()

    vals = ['cut', 'somefile', '>', 'anotherfile']
    for i, part in enumerate(cmds[0].parts):
        vals[i].should.equal(part)

