""" A parser and other parser related classes. """

try:
    from metapipe.models.tokens import Token 	# Python3
except ImportError:
    from models.tokens import Token


class Parser(object):

    def __init__(self, lexer_tokens):
        self.tokens = lexer_tokens
        self.statements = []
        self.paths = []
        self.files = []

    def consume(self):
        """ Converts the lexer tokens into valid statements. This process
        also checks command syntax.
        """
        self.files = [s for s in self.next_file()]
        self.paths = [s for s in self.next_path()]
        self.statements = [s for s in self.next_token()]
        self.statements = [s for s in self.next_statement()]
        return self.statements, self.files, self.paths

    def next_file(self):
        """ Given a list of statements, pull out the files. """
        return self._next_file(start=0, file_mode=False)

    def next_path(self):
        """ Given a list of statements, pull out the paths. """
        return self._next_path(start=0, path_mode=False)

    def next_statement(self):
        """ Given a list of statements, expand them into independent commands. """
        for statement in self.statements:
            for sub_statement in self._next_statement(statement):
                yield sub_statement

    def next_token(self):
        """ Given the tokens from the lexer, collect them into statements."""
        statement = []
        escape_next = False
        for token in self.tokens:
            statement.append(token)
            if not escape_next:
                if token.type == 'ESCAPE':
                    escape_next = True
                    continue
                elif token.type == 'NEWLINE':
                    yield statement
                    statement = []
            escape_next = False

    def _next_statement(self, statement):
        """ Given a statement, break it down and return a list of substatements. """
        cmd_buffer, other_buffer = [], []

        opened = False
        for i, token in enumerate(statement):
            if token.type == 'OPEN':
                opened = True
                other_buffer.append(Token('PL_HDR', ''))
            elif token.type == 'CLOSE':
                if not opened:
                    raise SyntaxError('Invalid Syntax: Statement is never opened.')
                opened = False
            elif opened:
                cmd_buffer.append(token)
            else:
                other_buffer.append(token)
        if opened:
            raise SyntaxError('Invalid Syntax: Statement is never closed.')

        cmd_buffer = self._seperate_or(cmd_buffer)

        for cmds in cmd_buffer:
            statement = []
            for token in other_buffer:
                if token.type != 'PL_HDR':
                    statement.append(token)
                else:
                    statement.append(Token('OPEN', ''))
                    statement.extend(cmds)
                    statement.append(Token('CLOSE', ''))
            yield statement

    def _next_file(self, start, file_mode):
        result = []

        try:
            token = self.tokens[start]
        except IndexError:
            return result

        next = start + 1
        type, text = token.type, token.text.strip()
        if type == 'LTR_NUM' and text == 'FILES:':
            file_mode = True
        elif text == 'COMMANDS:' or text == 'PATHS:':
            file_mode = False
        elif file_mode and type == 'LTR_NUM':
            del self.tokens[start]
            next = start
            result.append(token)
        elif file_mode:
            del self.tokens[start]
            next = start
        else:
            pass

        return result + self._next_file(next, file_mode)

    def _next_path(self, start, path_mode):
        result = []

        try:
            token = self.tokens[start]
        except IndexError:
            return result

        next = start + 1
        type, text = token.type, token.text.strip()
        if type == 'LTR_NUM' and text == 'PATHS:':
            path_mode = True
        elif text == 'COMMANDS:' or text == 'FILES:':
            path_mode = False
        elif path_mode and type == 'LTR_NUM':
            del self.tokens[start]
            next = start
            result.append(token)
        elif path_mode:
            del self.tokens[start]
            next = start
        else:
            pass
        return result + self._next_path(next, path_mode)

    def _seperate_or(self, buffer):
        res = [[]]
        for token in buffer:
            if token.type != 'OR':
                res[-1].append(token)
            else:
                res.append([])
        return res
