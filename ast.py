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


class CommandAssign:
	def __init__(self, lineno, identifier=None, expr=None, cond=None):
		self.identifier = identifier
		self.expr = expr
		self.lineno = lineno
		self.cond = cond
		self.print()

	def print(self):
		print(f"CommandAssign: {self.lineno, self.identifier, self.expr, self.cond}")


class CommandIf:
	def __init__(self, lineno, cond, commandIf, commandElse=None):
		self.lineno = lineno
		self.cond = cond
		self.commandIf = commandIf
		self.commandElse = commandElse
		self.print()

	def print(self):
		print(f"CommandIf: {self.lineno, self.cond, self.commandIf, self.commandElse}")


class CommandWhile:
	def __init__(self, lineno, cond, commands):
		self.lineno = lineno
		self.cond = cond
		self.commands = commands
		self.print()

	def print(self):
		print(f"CommandWhile: {self.lineno, self.cond, self.commands}")


class CommandRepeat:
	def __init__(self, lineno, cond, commands):
		self.lineno = lineno
		self.cond = cond
		self.commands = commands
		self.print()

	def print(self):
		print(f"CommandRepeat: {self.lineno, self.cond, self.commands}")


class CommandFor:
	def __init__(self, lineno, iterator, valueFrom, valueTo, commands, downTo=False):
		self.lineno = lineno
		self.iterator = iterator
		self.valueFrom = valueFrom
		self.valueTo = valueTo
		self.commands = commands
		self.downTo = downTo
		self.print()

	def print(self):
		print(f"CommandFor: {self.lineno, self.iterator, self.valueFrom, self.valueTo, self.commands, self.downTo}")


class CommandRead:
	def __init__(self, lineno, identifier):
		self.lineno = lineno
		self.identifier = identifier
		self.print()

	def print(self):
		print(f"CommandRead: {self.lineno, self.identifier}")


class CommandWrite:
	def __init__(self, lineno, value):
		self.lineno = lineno
		self.value = value
		self.print()

	def print(self):
		print(f"CommandWrite: {self.lineno, self.value}")
