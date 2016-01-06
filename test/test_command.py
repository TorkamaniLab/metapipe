""" Tests for the command class. """

from fixtures import *

from metapipe.parser import Parser


def test_eval():
    parser = Parser(overall)
    cmds = parser.consume()
    print len(cmds)
    for i, cmd in enumerate(cmds):
        cmd.find_dependencies(cmds) 


    cmds[0].eval().should.equal('/usr/bin/python somescript.py -i test/files/somefile.1 test/files/somefile.2 test/files/somefile.3 -o metapipe.1.1.output -fgh somefile.txt')
    
    cmds[1].eval().should.equal('/usr/bin/python somescript.py -i test/files/somefile.4 test/files/somefile.5 test/files/somefile.6 -o metapipe.1.2.output -fgh somefile.txt')
    
    cmds[2].eval().should.equal('/usr/bin/bash somescript.sh -i metapipe.1.1.output -o metapipe.2.1.output -fgh somefile.txt')
    
    cmds[3].eval().should.equal('/usr/bin/bash somescript.sh -i metapipe.1.2.output -o metapipe.2.2.output -fgh somefile.txt')
    
    cmds[4].eval().should.equal('/usr/bin/ruby somescript.rb -i metapipe.2.1.output >> somefile')
    
    cmds[5].eval().should.equal('/usr/bin/ruby somescript.rb -i metapipe.2.2.output >> somefile')
    
    cmds[6].eval().should.equal('/usr/bin/ruby somescript.rb -i metapipe.1.1.output metapipe.1.2.output >> somefile')
    
    cmds[7].eval().should.equal('cut -f *.counts > something.file')
    
    cmds[8].eval().should.equal('paste *.counts >  metapipe.5.0.output')
    
    cmds[9].eval().should.equal('./somescript  test/files/somefile.1 test/files/somefile.2 test/files/somefile.3 test/files/somefile.4')
    
    cmds[10].eval().should.equal('./somescript  test/files/somefile.1.counts test/files/somefile.2.counts test/files/somefile.3.counts test/files/somefile.4.counts ')
    
    cmds[11].eval().should.equal('/usr/bin/python somescript.py -i test/files/somefile.1.counts test/files/somefile.2.counts test/files/somefile.3.counts test/files/somefile.4.counts > metapipe.7.1.output')        