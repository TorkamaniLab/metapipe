""" Tests for the overall parser. """

from __future__ import print_function

import sure

from metapipe.parser import Parser

from .fixtures import *


def test_consume():
    parser = Parser(overall)
    res = parser.consume()
    
    parser.paths[0].alias.should.equal('python')
    parser.paths[0].path.should.equal('/usr/bin/python')
    parser.paths[1].alias.should.equal('bash')
    parser.paths[1].path.should.equal('/usr/bin/bash')
    parser.paths[2].alias.should.equal('rb')
    parser.paths[2].path.should.equal('/usr/bin/ruby')

    parser.files[0].alias.should.equal('1')
    parser.files[0].filename.should.equal('test/files/somefile.1')
    parser.files[1].alias.should.equal('2')
    parser.files[1].filename.should.equal('test/files/somefile.2')

    vals = ['python somescript.py -i ', '-o ', '-fgh somefile.txt']
    len(res[0].input).should.equal(3)
    res[0].output.alias.should.equal('1.1')
    for cmd, val in zip([cmd for cmd in res[0].cmds
            if isinstance(cmd, str)], vals):
        cmd.should.equal(val)
    len(res[1].input).should.equal(3)
    res[1].output.alias.should.equal('1.2')
    for cmd, val in zip([cmd for cmd in res[1].cmds
            if isinstance(cmd, str)], vals):
        cmd.should.equal(val)

    vals = ['bash somescript.sh -i ', '-o ', '-fgh somefile.txt']
    len(res[2].input).should.equal(1)
    res[2].output.alias.should.equal('2.1')
    for cmd, val in zip([cmd for cmd in res[2].cmds
            if isinstance(cmd, str)], vals):
        cmd.should.equal(val)
    len(res[3].input).should.equal(1)
    res[3].output.alias.should.equal('2.2')
    for cmd, val in zip([cmd for cmd in res[3].cmds
            if isinstance(cmd, str)], vals):
        cmd.should.equal(val)

    vals = ['rb somescript.rb -i ', '>> somefile']
    len(res[4].input).should.equal(1)
    res[4].output.should.equal(None)
    for cmd, val in zip([cmd for cmd in res[4].cmds
            if isinstance(cmd, str)], vals):
        cmd.should.equal(val)
    len(res[5].input).should.equal(1)
    res[5].output.should.equal(None)
    for cmd, val in zip([cmd for cmd in res[5].cmds
            if isinstance(cmd, str)], vals):
        cmd.should.equal(val)
    len(res[6].input).should.equal(2)
    res[6].output.should.equal(None)
    for cmd, val in zip([cmd for cmd in res[6].cmds
            if isinstance(cmd, str)], vals):
        cmd.should.equal(val)

    vals = ['cut -f *.counts > something.file']
    len(res[7].input).should.equal(0)
    res[7].output.should.equal(None)
    for cmd, val in zip([cmd for cmd in res[7].cmds
            if isinstance(cmd, str)], vals):
        cmd.should.equal(val)

    vals = ['paste *.counts > ']
    len(res[8].input).should.equal(0)
    res[8].output.alias.should.equal('5.0')
    res[8].output.magic.should.equal('some.file')
    for cmd, val in zip([cmd for cmd in res[8].cmds
            if isinstance(cmd, str)], vals):
        cmd.should.equal(val)

    vals = ['./somescript ']
    len(res[9].input).should.equal(4)
    res[9].output.should.equal(None)
    for cmd, val in zip([cmd for cmd in res[9].cmds
            if isinstance(cmd, str)], vals):
        cmd.should.equal(val)
#     len(res[10].input).should.equal(2)
#     res[10].output.should.equal(None)
#     res[10]._and.should.equal(True)
#     for cmd, val in zip([cmd for cmd in res[10].cmds
#             if isinstance(cmd, str)], vals):
#         cmd.should.equal(val)

#     vals = ['rb somescript.rb -i ']
#     len(res[11].input).should.equal(1)
#     res[11].output.should.equal(None)
#     res[11]._or.should.equal(True)
#     for cmd, val in zip([cmd for cmd in res[11].cmds
#             if isinstance(cmd, str)], vals):
#         cmd.should.equal(val)

    vals = ['python somescript.py -i ']
    len(res[11].input).should.equal(1)
    res[11].output.magic.should.equal('*.bam')
    res[11].output.alias.should.equal('7.1')
    res[11]._and.should.equal(True)
    for cmd, val in zip([cmd for cmd in res[11].cmds
            if isinstance(cmd, str)], vals):
        cmd.should.equal(val)
