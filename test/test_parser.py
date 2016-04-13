""" Tests for the overall parser. """

from __future__ import print_function

import sure

from metapipe.parser import Parser
from metapipe.models import Input, Output

from .fixtures import *


def test_no_paths():
    parser = Parser(no_paths)
    res = parser.consume()

    parser.paths.should.have.length_of(0)


def test_no_files():
    parser = Parser(no_files)
    res = parser.consume()

    parser.files.should.have.length_of(0)


def test_no_cmds():
    parser = Parser(no_cmds)
    res = parser.consume.when.called.should.throw(ValueError)


def test_consume_paths():
    parser = Parser(overall)
    res = parser.consume()

    parser.paths[0].alias.should.equal('python')
    parser.paths[0].path.should.equal('/usr/bin/python')
    parser.paths[1].alias.should.equal('bash')
    parser.paths[1].path.should.equal('/usr/bin/bash')
    parser.paths[2].alias.should.equal('rb')
    parser.paths[2].path.should.equal('/usr/bin/ruby')


def test_consume_files():
    parser = Parser(overall)
    res = parser.consume()

    parser.files[0].alias.should.equal('1')
    parser.files[0].filename.should.equal('somefile.1')
    parser.files[1].alias.should.equal('2')
    parser.files[1].filename.should.equal('somefile.2')


def test_consume_commands_1():
    parser = Parser(overall)
    res = parser.consume()

    res[0].alias.should.equal('1')
    res[0].parts[4].should.equal(parser.paths[0])
    res[0].parts[5].should.equal('somescript.py')
    res[0].parts[6].should.equal('-i')
    res[0].parts[7][0][0].should.equal(Input('1', filename='somefile.1'))
    res[0].parts[7][0][1].should.equal(Input('2', filename='somefile.2'))
    res[0].parts[7][0][2].should.equal(Input('3', filename='somefile.3'))
    res[0].parts[7][1][0].should.equal(Input('4', filename='somefile.4'))
    res[0].parts[7][1][1].should.equal(Input('5', filename='somefile.5'))
    res[0].parts[7][1][2].should.equal(Input('6', filename='somefile.6'))
    res[0].parts[8].should.equal('-o')
    res[0].parts[9].should.equal(Output('1'))
    res[0].parts[10].should.equal('-fgh')
    res[0].parts[11].should.equal('somefile.txt')
    res[0]._dependencies.should.have.length_of(0)


def test_consume_commands_2():
    parser = Parser(overall)
    res = parser.consume()

    res[1].alias.should.equal('2')
    res[1].parts[4].should.equal(parser.paths[1])
    res[1].parts[5].should.equal('somescript.sh')
    res[1].parts[6].should.equal('-i')
    res[1].parts[7][0][0].should.equal(Input('1.1'))
    res[1].parts[7][1][0].should.equal(Input('1.2'))
    res[1].parts[8].should.equal('-o')
    res[1].parts[9].should.equal(Output('1'))
    res[1].parts[10].should.equal('-fgh')
    res[1].parts[11].should.equal('somefile.txt')
    res[1]._dependencies.should.have.length_of(1)
    res[1]._dependencies[0].alias.should.equal('1')


def test_consume_commands_3():
    parser = Parser(overall)
    res = parser.consume()

    res[2].alias.should.equal('3')
    res[2].parts[4].should.equal(parser.paths[2])
    res[2].parts[5].should.equal('somescript.rb')
    res[2].parts[6].should.equal('-i')
    res[2].parts[7][0][0].should.equal(Input('2.1'))
    res[2].parts[7][1][0].should.equal(Input('2.2'))
    res[2].parts[7][2][0].should.equal(Input('1.1'))
    res[2].parts[7][2][1].should.equal(Input('1.2'))
    res[2].parts[8].should.equal('>>')
    res[2].parts[9].should.equal('somefile')
    res[2]._dependencies.should.have.length_of(2)

    aliases = [dep.alias for dep in res[2]._dependencies]
    aliases.should.contain('2')
    aliases.should.contain('1')


def test_consume_commands_4():
    parser = Parser(overall)
    res = parser.consume()

    res[3].alias.should.equal('4')
    res[3].parts[4].should.equal('cut')
    res[3].parts[5].should.equal('-f')
    res[3].parts[6].should.equal('*.counts')
    res[3].parts[7][0].should.equal('>')
    res[3].parts[8].should.equal('something.file')
    res[3]._dependencies.should.have.length_of(0)


def test_consume_commands_5():
    parser = Parser(overall)
    res = parser.consume()

    res[4].alias.should.equal('5')
    res[4].parts[4].should.equal('paste')
    res[4].parts[5].should.equal('*.counts')
    res[4].parts[6].should.equal('>')
    res[4].parts[9].should.equal(Output('', magic='some.file'))
    res[4]._dependencies.should.have.length_of(0)


def test_consume_commands_6():
    parser = Parser(overall)
    res = parser.consume()
    print(res[5].parts)
    res[5].alias.should.equal('6')
    res[5].parts[4].should.equal('./somescript')
    res[5].parts[5][0][0].should.equal(Input('1', 'somefile.1'))
    res[5].parts[5][0][1].should.equal(Input('2', 'somefile.2'))
    res[5].parts[5][0][2].should.equal(Input('3', 'somefile.3'))
    res[5].parts[5][1][0].should.equal(Input('4', '*.counts'))
    res[5]._dependencies.should.have.length_of(0)


def test_consume_commands_7():
    parser = Parser(overall)
    res = parser.consume()

    res[6].alias.should.equal('7')
    res[6].parts[4].should.equal(parser.paths[2])
    res[6].parts[5].should.equal('somescript.rb')
    res[6].parts[6].should.equal('-i')
    res[6].parts[7][0][0].should.equal(Input('*.counts',
                                        '*.counts'))
    res[6].parts.should.have.length_of(8)
    res[6]._dependencies.should.have.length_of(0)


def test_consume_commands_8():
    parser = Parser(overall)
    res = parser.consume()

    res[7].alias.should.equal('8')
    res[7].parts[4].should.equal(parser.paths[0])
    res[7].parts[5].should.equal('somescript.py')
    res[7].parts[6].should.equal('-i')
    res[7].parts[7][0][0].should.equal(Input('*.counts',
                                filename='*.counts'))
    res[7].parts[9].should.equal(Output('', magic='*.bam'))
    res[7]._dependencies.should.have.length_of(0)


def test_consume_commands_9():
    parser = Parser(overall)
    res = parser.consume()

    res[8].alias.should.equal('9')
    res[8].parts[4].should.equal('cat')
    res[8].parts[5][0][0].should.equal(Input('*.bam',
                                filename='*.bam'))
    res[8]._dependencies.should.have.length_of(1)


def test_consume_full_sample_pipeline():
    parser = Parser(full_sample_pipeline)
    res = parser.consume()

    res[0].alias.should.equal('1')
    res[0].parts[0].should.equal(CommentToken(['#', ' Trimmomatic']))
    res[0].parts[1].should.equal('java')


def test_consume_multiple_inputs():
    parser = Parser(multiple_inputs)
    res = parser.consume()

    res[0].alias.should.equal('1')
    res[0].parts[0].should.equal('bash')
    res[0].parts[2][0][0].should.equal(Input('1',
                                filename='somefile.1'))
    res[0].parts[2][1][0].should.equal(Input('2',
                                filename='somefile.2'))
    res[0].parts[2][2][0].should.equal(Input('3',
                                filename='somefile.3'))
    res[0].parts[4][0][0].should.equal(Input('4',
                                filename='somefile.4'))
    res[0].parts[4][1][0].should.equal(Input('5',
                                filename='somefile.5'))
    res[0].parts[4][2][0].should.equal(Input('6',
                                filename='somefile.6'))
    res[0]._dependencies.should.have.length_of(0)


def test_consume_global_opts():
    parser = Parser(overall)
    res = parser.consume()
    print(parser.global_options)
    parser.global_options.should.have.length_of(2)
