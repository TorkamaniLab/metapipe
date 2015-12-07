""" Tests for the lexer and parser. """

import sure

from metapipe.parser import Parser
from metapipe.lexer import Token

tokens = [
        Token('LTR_NUM', 'cut -f '),	# Statement 1
        Token('OPEN', '{'),
        Token('LTR_NUM', '1'),
        Token('AND', ','),
        Token('LTR_NUM', '2'),
        Token('OR', '||'),		# Sub_statement 1.1
        Token('LTR_NUM', '3'),
        Token('AND', ','),
        Token('LTR_NUM', '4'),
        Token('CLOSE', '}'),
        Token('NEWLINE', '\n'),

        Token('LTR_NUM', 'paste -d \',\''),	# Statement 2
        Token('OPEN', '{'),
        Token('LTR_NUM', '2'),
        Token('LTR_NUM', '3'),
        Token('CLOSE', '}'),
        Token('ESCAPE', '\\'),
        Token('NEWLINE', '\n'),

        Token('LTR_NUM', '>'), 	# Still statement 2
        Token('OUTPUT', ''),
        Token('NEWLINE', '\n')
        ]


def test_make_statements():
    parser = Parser(tokens)
    statements = [s for s in parser.next_token()]
    len(statements).should.equal(2)

def test_parse_statements():
    parser = Parser(tokens)
    statements = parser.consume()
    len(statements).should.equal(3)
    statements[0][2].text.should.equal('1')
    statements[0][4].text.should.equal('2')
    statements[1][2].text.should.equal('3')
    statements[1][4].text.should.equal('4')
    statements[2][2].text.should.equal('2')
    statements[2][3].text.should.equal('3')

