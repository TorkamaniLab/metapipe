""" Tests for the output of the command template. """

import sure

from .fixtures import *

from metapipe.parser import Parser
from metapipe.models import *


def test_eval_1():
    parser = Parser(overall)

    templates = parser.consume()

    vals = [PathToken('python', '/usr/bin/python'), 'somescript.py', '-i',
        Input('1', 'somefile.1'),
        Input('2', 'somefile.2'),
        Input('3', 'somefile.3'), 
        '-o', Output('1.1', 'metapipe.1.1.output'),
        '-fgh', 'somefile.txt']
    cmd = templates[0].eval()[0]
    print(cmd.parts)
    for i, part in enumerate(cmd.parts):
        vals[i].should.equal(part)
    
    
def test_eval_2():
    parser = Parser(overall)
    templates = parser.consume()
    print(templates[0].parts)

    vals = [PathToken('python', '/usr/bin/python'), 'somescript.py', '-i',
        Input('4', 'somefile.4'),
        Input('5', 'somefile.5'),
        Input('6', 'somefile.6'), 
        '-o', Output('1.2', 'metapipe.1.2.output'),
        '-fgh', 'somefile.txt']
    cmd = templates[0].eval()[1]
    print(cmd.parts)
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
    print(cmd)
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
    print(cmd.parts)
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
    print(cmd)
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
    print(cmd.parts)
    for i, part in enumerate(cmd.parts):
        vals[i].should.equal(part)
