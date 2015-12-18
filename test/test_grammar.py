""" A test of PyParsing. """

import sure

from metapipe.grammar import Grammar 
from fixtures import *


def test_cmd():
	res = Grammar.command.parseString(cmd)
	val = ['python somescript.py -i ', '-o ', '-fgh  somefile.txt']
	for i, c in enumerate(res.command):
		c.should.equal(val[i])
	res._in[0][0].should.equal('1')
	res._in[0][1].should.equal('2')
	res._in[0][2].should.equal('3')
	res._in[1][0].should.equal('4')
	res._in[1][1].should.equal('5')
	res._in[1][2].should.equal('6')
	res._out[0].should.equal('o')


def test_file():
	res = Grammar.file.parseString(file)
	print res
	res.alias.should.equal('1')
	res.filename.should.equal('somedir/somefile.ext')


def test_path():
	res = Grammar.path.parseString(path)
	print res
	res.alias.should.equal('python')
	res.path.should.equal('/usr/bin/python')


def test_overall():
	res = Grammar.overall.parseString(overall)
	print res
	
	res['COMMANDS'][0][0].should.equal('python')
	res['COMMANDS'][0][1].should.equal(' somescript.py -i {1,2,3||4,5,6} -o {o} -fgh somefile.txt')
