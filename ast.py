memory = 0
variables = {}
arrays = {}


class Program:
	def __init__(self, declarations=None, commands=None):
		self.declarations = declarations
		self.commands = commands
		self.print()

	def print(self):
		print(self.declarations)
		print(self.commands)


class Declarations:
	def __init__(self, identifier, lineno, start=None, stop=None):
		self.identifier = identifier
		self.lineno = lineno
		self.start = start
		self.stop = stop
		self.print()

	def print(self):
		print(self.lineno, self.identifier, self.start, self.stop)
