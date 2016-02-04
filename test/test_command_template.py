""" Tests for the output of the command template. """

import sure

from .fixtures import *

from metapipe.parser import Parser
from metapipe.models import *


def test_eval_multiple_inputs():
    parser = Parser(multiple_inputs)

    templates = parser.consume()
    
    vals = ['bash', 'somescript', 
        [Input('1', 'somefile.1')], '--conf', 
        [Input('4', 'somefile.4')], 
        '>', Output('1.1', 'metapipe.1.1.output')]
    cmd = templates[0].eval()[0]
    print(cmd)
    for i, part in enumerate(cmd.parts):
        vals[i].should.equal(part)
