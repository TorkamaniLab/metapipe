""" Various Token Types. """

import shlex


class Token(object):

    def __init__(self, type, text):
        self.type = type
        self.text = text

    def __repr__(self):
        return '<Token: %s (%s)>' % (self.type, self.text)
                
        
class FileToken(Token):
	
	def __init__(self, text, number):
		self.number = number
		try:
			super().__init__('File', text)
		except Exception:
			super(Token, self).__init__('File', text)
		
	def __repr__(self):
		return '<FileToken: %s (%s)>' % (self.number, self.text)
	
	@staticmethod
	def from_token(token):
		try:
			number, text = shlex.split(token.text)
		except ValueError:
			raise SyntaxError('Invalid Syntax: File must have a number and path.')
		return FileToken(text, number)


class PathToken(Token):
	
	def __init__(self, alias, path):
		self.alias = alias
		try:
			super().__init__('Path', path)
		except Exception:
			super(Token, self).__init__('Path', path)
		
	def __repr__(self):
		return '<PathToken: %s (%s)>' % (self.alias, self.text)
		
	@staticmethod
	def from_token(token):
		try:
			alias, path = shlex.split(token.text)
		except ValueError:
			raise SyntaxError('Invalid Syntax: File must have a number and path.')
		return PathToken(alias, path)

