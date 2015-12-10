
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

file_tokens = [
        Token('LTR_NUM', 'FILES:'),
        Token('NEWLINE', '\n'),
        Token('LTR_NUM', '1. somefile'),
        Token('NEWLINE', '\n'),
        Token('LTR_NUM', '2. somefile'),
        Token('NEWLINE', '\n'),
]

path_tokens = [
        Token('LTR_NUM', 'PATHS:'),
        Token('NEWLINE', '\n'),
        Token('LTR_NUM', '1. somepath'),
        Token('NEWLINE', '\n'),
        Token('LTR_NUM', '2. somepath'),
        Token('NEWLINE', '\n'),
]
