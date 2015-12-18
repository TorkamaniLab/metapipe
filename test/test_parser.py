""" Tests for the overall parser. """

import sure

from metapipe.parser import Parser

from fixtures import *


def test_consume():
	parser = Parser(overall)
	parser.consume()
	
	print parser.commands
	
	parser.paths[0].alias.should.equal('python')
	parser.paths[0].path.should.equal('/usr/bin/python')
	parser.paths[1].alias.should.equal('bash')
	parser.paths[1].path.should.equal('/usr/bin/bash')
	parser.paths[2].alias.should.equal('rb')
	parser.paths[2].path.should.equal('/usr/bin/ruby')
	
	parser.files[0].alias.should.equal('1')
	parser.files[0].filename.should.equal('somefile.1')
	parser.files[1].alias.should.equal('2')
	parser.files[1].filename.should.equal('somefile.2')
	
	vals = ['python somescript.py -i ', '-o ', '-fgh somefile.txt']
	for i,  cmd in enumerate(parser.commands[0].command):
		cmd.should.equal(vals[i])
	
	vals = [['1', '2', '3'], ['4', '5', '6']]
	for i, _in in enumerate(parser.commands[0]._in):
		for j, __in in enumerate(_in):
			__in.should.equal(vals[i][j])
			
	parser.commands[2]._out.should.equal('')
