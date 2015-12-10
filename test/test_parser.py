""" Tests for the lexer and parser. """

import sure

from metapipe.parser import Parser
from metapipe.lexer import Token

from fixtures import *


def test_make_statements():
    parser = Parser(tokens)
    statements = [s for s in parser.next_token()]
    len(statements).should.equal(2)


def test_parse_statements():
    parser = Parser(tokens)
    statements, f, p = parser.consume()
    len(statements).should.equal(3)
    statements[0][2].text.should.equal('1')
    statements[0][4].text.should.equal('2')
    statements[1][2].text.should.equal('3')
    statements[1][4].text.should.equal('4')
    statements[2][2].text.should.equal('2')
    statements[2][3].text.should.equal('3')


def test_consume():
	parser = Parser(tokens+file_tokens+path_tokens)
	parser.consume()
	len(parser.statements).should.equal(3)
	len(parser.paths).should.equal(2)
	len(parser.files).should.equal(2)
