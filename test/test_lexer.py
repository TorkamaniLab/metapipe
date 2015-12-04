""" Tests for the lexer. """

import sure, sys

from metapipe.lexer import Lexer


def test_consume():
	input = 'some string with\ncomplex\tinput {1,2,3||4,3,5}'
	lexer = Lexer(input)
	tokens = lexer.consume()
	tokens[0].text.should.equal(input[0])
	tokens[33].text.should.equal(input[33])
	tokens[31].type.should.equal('OPEN')
	tokens[33].type.should.equal('AND')
	tokens[44].type.should.equal('CLOSE')
	
	
def test_condense():
	input = 'some "string" with\ncomplex\tinput {1,2,3||4,3,5} \\woo boy!'
	lexer = Lexer(input)
	tokens = lexer.consume()
	tokens[0].text.should.equal(input[0])
	tokens[33].text.should.equal(input[33])
	tokens[33].type.should.equal('OPEN')
	tokens[35].type.should.equal('AND')
	tokens[46].type.should.equal('CLOSE')

	tokens = lexer.condense()
	print tokens
	tokens[0].type.should.equal('LTR_NUM')
	tokens[0].text.should.equal('some ')
	tokens[1].type.should.equal('QUOTE')
	tokens[2].text.should.equal('string')
	tokens[3].type.should.equal('QUOTE')
