""" Various Token Types. """


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
		return '<File: %s (%s)>' % (self.number, self.text)
	
	@classmethod
	def from_token(token):
		pass


class PathToken(Token):
	
	def __init__(self, text):
		try:
			super().__init__('Path', text)
		except Exception:
			super(Token, self).__init__('Path', text)
		
	def __repr__(self):
		return '<Path: %s (%s)>' % (self.alias, self.path)
		
	@classmethod
	def from_token(token):
		pass

