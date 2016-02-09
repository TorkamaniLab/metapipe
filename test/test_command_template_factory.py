""" Tests for the output of the command template factory. """

import sure

from .fixtures import *

from metapipe.parser import Parser
from metapipe.models import *


def test_multiple_inputs():
    parser = Parser(multiple_inputs)

    cmds = parser.consume()
    
    vals = ['bash', 'somescript', 
        [[Input('1', 'somefile.1')], [Input('2', 'somefile.2')], 
            [Input('3', 'somefile.3')]], '--conf', 
        [[Input('4', 'somefile.4')], [Input('5', 'somefile.5')], 
            [Input('6', 'somefile.6')]], 
        '>', Output('1', 'metapipe.1.output')]

    for i, part in enumerate(cmds[0].parts):
        vals[i].should.equal(part)


def test_multiple_outputs():
    parser = Parser(multiple_outputs)

    cmds = parser.consume()
    
    vals = ['bash', 'somescript', 
        [[Input('1', 'somefile.1')], [Input('2', 'somefile.2')], 
            [Input('3', 'somefile.3')]], '--log', 
        Output('1', 'metapipe.1.output'), '-r', 
        Output('1', 'metapipe.1.output')]

    print(cmds[0].parts)
    for i, part in enumerate(cmds[0].parts):
        vals[i].should.equal(part)
