""" Tests for the overall parser. """

from __future__ import print_function

import sure

from metapipe.parser import Parser
from metapipe.models import Input, Output

from .fixtures import *


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
    parser.files[0].filename.should.equal('test/files/somefile.1')
    parser.files[1].alias.should.equal('2')
    parser.files[1].filename.should.equal('test/files/somefile.2')
  
    
def test_consume_commands_1():
    parser = Parser(overall)
    res = parser.consume()
        
    res[0].alias.should.equal('1')
    res[0].parts[0].should.equal(parser.paths[0])
    res[0].parts[1].should.equal('somescript.py')
    res[0].parts[2].should.equal('-i')
    res[0].parts[3][0].should.equal(Input('1', filename='somefile.1'))
    res[0].parts[3][1].should.equal(Input('2', filename='somefile.2'))
    res[0].parts[3][2].should.equal(Input('3', filename='somefile.3'))
    res[0].parts[4][0].should.equal(Input('4', filename='somefile.4'))
    res[0].parts[4][1].should.equal(Input('5', filename='somefile.5'))
    res[0].parts[4][2].should.equal(Input('6', filename='somefile.6'))
    res[0].parts[5].should.equal('-o')
    res[0].parts[6].should.equal(Output('1'))
    res[0].parts[7].should.equal('-fgh')
    res[0].parts[8].should.equal('somefile.txt')
    res[0].dependencies.should.have.length_of(0)


def test_consume_commands_2():
    parser = Parser(overall)
    res = parser.consume()
        
    res[1].alias.should.equal('2')
    res[1].parts[0].should.equal(parser.paths[1])
    res[1].parts[1].should.equal('somescript.sh')
    res[1].parts[2].should.equal('-i')
    res[1].parts[3][0].should.equal(Input('1.1'))
    res[1].parts[4][0].should.equal(Input('1.2'))
    res[1].parts[5].should.equal('-o')
    res[1].parts[6].should.equal(Output('1'))
    res[1].parts[7].should.equal('-fgh')
    res[1].parts[8].should.equal('somefile.txt')
    res[1].dependencies.should.have.length_of(1)
    res[1].dependencies[0].alias.should.equal('1')


def test_consume_commands_3():
    parser = Parser(overall)
    res = parser.consume()
        
    res[2].alias.should.equal('3')
    res[2].parts[0].should.equal(parser.paths[2])
    res[2].parts[1].should.equal('somescript.rb')
    res[2].parts[2].should.equal('-i')
    res[2].parts[3][0].should.equal(Input('2.1'))
    res[2].parts[4][0].should.equal(Input('2.2'))
    res[2].parts[5][0].should.equal(Input('1.1'))
    res[2].parts[5][1].should.equal(Input('1.2'))
    res[2].parts[6].should.equal('>>')
    res[2].parts[7].should.equal('somefile')
    res[2].dependencies.should.have.length_of(2)
    res[2].dependencies[0].alias.should.equal('2')
    res[2].dependencies[1].alias.should.equal('1')


def test_consume_commands_4():
    parser = Parser(overall)
    res = parser.consume()
        
    print(res[3].parts)
    res[3].alias.should.equal('4')
    res[3].parts[0].should.equal('cut')
    res[3].parts[1].should.equal('-f')
    res[3].parts[2].should.equal('*.counts')
    res[3].parts[3][0].should.equal('>')
    res[3].parts[4].should.equal('something.file')
    res[3].dependencies.should.have.length_of(0)


def test_consume_commands_5():
    parser = Parser(overall)
    res = parser.consume()
        
    print(res[4].parts)
    res[4].alias.should.equal('5')
    res[4].parts[0].should.equal('paste')
    res[4].parts[1].should.equal('*.counts')
    res[4].parts[2].should.equal('>')
    res[4].parts[3].should.equal(Output('', magic='some.file'))
    res[4].dependencies.should.have.length_of(0)

    
def test_consume_commands_6():
    parser = Parser(overall)
    res = parser.consume()
        
    print(res[5].parts)
    res[5].alias.should.equal('6')
    res[5].parts[0].should.equal('./somescript')
    res[5].parts[1][0].should.equal(Input('1', 'test/files/somefile.1'))
    res[5].parts[1][1].should.equal(Input('2', 'test/files/somefile.2'))
    res[5].parts[1][2].should.equal(Input('3', 'test/files/somefile.3'))
    res[5].parts[2][0].should.equal(Input('4', 'test/files/*.counts'))
    res[5].dependencies.should.have.length_of(0)


def test_consume_commands_7():
    parser = Parser(overall)
    res = parser.consume()
        
    print(res[6].parts)
    res[6].alias.should.equal('7')
    res[6].parts[0].should.equal(parser.paths[2])
    res[6].parts[1].should.equal('somescript.rb')
    res[6].parts[2].should.equal('-i')
    res[6].parts[3][0].should.equal(Input('test/files/*.counts',         
                                        'test/files/*.counts'))
    res[6].parts.should.have.length_of(4)
    res[6].dependencies.should.have.length_of(0)


def test_consume_commands_8():
    parser = Parser(overall)
    res = parser.consume()
        
    print(res[7].parts)
    res[7].alias.should.equal('8')
    res[7].parts[0].should.equal(parser.paths[0])
    res[7].parts[1].should.equal('somescript.py')
    res[7].parts[2].should.equal('-i')
    res[7].parts[3][0].should.equal(Input('test/files/*.counts', 
                                filename='test/files/*.counts'))
    res[7].parts[4].should.equal('>')
    res[7].parts[5].should.equal(Output('', magic='*.bam'))
    res[7].dependencies.should.have.length_of(0)
