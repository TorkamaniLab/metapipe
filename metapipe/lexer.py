""" A basic lexer, and it's components.

author: Brian Schrader
since: 2015-12-4
"""


class Token(object):

    def __init__(self, type, text):
        self.type = type
        self.text = text

    def __repr__(self):
        return '<Token: %s (%s)>' % (self.type, self.text)


class Lexer(object):

    NO_GROUP = {'AND', 'OPEN', 'CLOSE'}

    def __init__(self, input):
        self.input = input
        self.tokens = []

    def consume(self):
        """ Using the input, return a list of tokens for that input. """
        self.tokens = [token for token in self.nextToken()]
        return self.tokens

    def condense(self):
        """ Combine simple tokens together into more complex tokens. """
        self.tokens = self._condense(start=0, tokens=self.tokens)
        return self.tokens

    def _condense(self, start, tokens):
        """ From start, combine all similar tokens. """
        next = start+1
        try:
            curr_token, next_token = tokens[start], tokens[next]
        except IndexError:
            return tokens

        if next_token.type == curr_token.type and curr_token.type not in self.NO_GROUP:
            tokens[next] = Token(curr_token.type, curr_token.text+next_token.text)
            del tokens[start]
            return self._condense(start, tokens)

        return self._condense(next, tokens)


    def nextToken(self):
        for c in self.input:
            if c == '|':
                yield Token('OR', c)
            elif c == ',':
                yield Token('AND', c)
            elif c == '{':
                yield Token('OPEN', c)
            elif c == '}':
                yield Token('CLOSE', c)
            elif c == '\'' or c == '"':
                yield Token('QUOTE', c)
            elif c == '\\':
                yield Token('ESCAPE', c)
            else:
                yield Token('LTR_NUM', c)

