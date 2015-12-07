""" A parser and other parser related classes. """

from lexer import Token


class Parser(object):

	def __init__(self, lexer_tokens):
		self.tokens = lexer_tokens
		self.statements = []
		
	def consume(self):
		""" Converts the lexer tokens into valid statements. This process
		also checks command syntax. 
		"""
		self.statements = [s for s in self.next_token()]
		self.statements = [s for s in self.next_statement()]
		return self.statements
		
	def next_statement(self):
		""" Given a list of statements, expand them into independent commands. """
		for statement in self.statements:
			for sub_statement in self._parse_statement(statement):
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
	
	def _parse_statement(self, statement):
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
			
	def _seperate_or(self, buffer):
		res = [[]] 
		for token in buffer:
			if token.type != 'OR':
				res[-1].append(token)
			else:
				res.append([])
		return res
			
			
			
