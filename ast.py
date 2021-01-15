class Manager:
	def __init__(self):
		self.variables = {}
		self.arrays = {}
		self.memoryCounter = 0
		self.exceptions = Exceptions()

	def addVariable(self, identifier, lineno):
		if identifier in self.variables:
			raise Exception(f"Trying to initialize an existing variable: {identifier}. In line: {lineno}")
		self.memoryCounter += 1
		self.variables[identifier] = self.memoryCounter

	def deleteVariable(self, identifier, lineno):
		if identifier not in self.variables:
			raise Exception(f"Trying to delete non-existing variable: {identifier}. In line: {lineno}")
		self.variables.pop(identifier)

	def createTemporaryVariable(self):
		pass

	def getVariablePosition(self, identifier):
		if identifier not in self.variables:
			raise Exception(f"Trying to access non-existing variable: {identifier}")
		else:
			return self.variables[identifier]

	def addArray(self, identifier, lineno, start, stop):
		if stop < start:
			raise Exception(f"Wrong array declaration: {identifier}. In line: {lineno}")
		self.arrays[identifier] = (self.memoryCounter + 1, start, stop)
		self.memoryCounter += stop - start + 1

	def getArrayData(self, identifier):
		if identifier not in self.arrays:
			raise Exception(f"Trying to access non-existing array: {identifier}")
		else:
			return self.arrays[identifier]

	def loadDataMemoryAddress(self, data, lineno):
		if data[0] == "id":
			self.exceptions.checkVariable(data[1], lineno)
			# return
		elif data[0] == "array":
			self.exceptions.checkArray(data[1], lineno)
			# return


class Exceptions(Manager):
	def __init__(self):
		super().__init__()

	def checkVariable(self, identifier, lineno):
		if identifier not in self.variables:
			if identifier not in self.arrays:
				raise Exception(f"Error. Variable {identifier} isn't initialized. Line: {lineno}")
			else:
				raise Exception(f"Error. Variable {identifier} initialized like an array. Line: {lineno}")

	def checkArray(self, identifier, lineno):
		if identifier not in self.arrays:
			if identifier not in self.variables:
				raise Exception(f"Error. Array {identifier} isn't initialized. Line: {lineno}")
			else:
				raise Exception(f"Error. Array {identifier} initialized like a variable. Line: {lineno}")


class Program:
	def __init__(self, declarations=None, commands=None):
		self.declarations = declarations
		self.commands = commands

	# self.print()

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


class ExpressionValue:
	def __init__(self, value):
		self.value = value
		self.print()

	def print(self):
		print(f"ExpressionValue: {self.value}")


class ExpressionAdd:
	def __init__(self, lineno, value0, value1):
		self.lineno = lineno
		self.value0 = value0
		self.value1 = value1
		self.print()

	def print(self):
		print(f"ExpressionAdd: {self.lineno, self.value0, self.value1}")


class ExpressionSub:
	def __init__(self, lineno, value0, value1):
		self.lineno = lineno
		self.value0 = value0
		self.value1 = value1
		self.print()

	def print(self):
		print(f"ExpressionSub: {self.lineno, self.value0, self.value1}")


class ExpressionMul:
	def __init__(self, lineno, value0, value1):
		self.lineno = lineno
		self.value0 = value0
		self.value1 = value1
		self.print()

	def print(self):
		print(f"ExpressionMul: {self.lineno, self.value0, self.value1}")


class ExpressionDiv:
	def __init__(self, lineno, value0, value1):
		self.lineno = lineno
		self.value0 = value0
		self.value1 = value1
		self.print()

	def print(self):
		print(f"ExpressionDiv: {self.lineno, self.value0, self.value1}")


class ExpressionMod:
	def __init__(self, lineno, value0, value1):
		self.lineno = lineno
		self.value0 = value0
		self.value1 = value1
		self.print()

	def print(self):
		print(f"ExpressionMod: {self.lineno, self.value0, self.value1}")


class ConditionEq:
	def __init__(self, lineno, value0, value1):
		self.lineno = lineno
		self.value0 = value0
		self.value1 = value1
		self.print()

	def print(self):
		print(f"ConditionEq: {self.lineno, self.value0, self.value1}")


class ConditionNeq:
	def __init__(self, lineno, value0, value1):
		self.lineno = lineno
		self.value0 = value0
		self.value1 = value1
		self.print()

	def print(self):
		print(f"ConditionNeq: {self.lineno, self.value0, self.value1}")


class ConditionLte:
	def __init__(self, lineno, value0, value1):
		self.lineno = lineno
		self.value0 = value0
		self.value1 = value1
		self.print()

	def print(self):
		print(f"ConditionLte: {self.lineno, self.value0, self.value1}")


class ConditionGte:
	def __init__(self, lineno, value0, value1):
		self.lineno = lineno
		self.value0 = value0
		self.value1 = value1
		self.print()

	def print(self):
		print(f"ConditionGte: {self.lineno, self.value0, self.value1}")


class ConditionLt:
	def __init__(self, lineno, value0, value1):
		self.lineno = lineno
		self.value0 = value0
		self.value1 = value1
		self.print()

	def print(self):
		print(f"ConditionLt: {self.lineno, self.value0, self.value1}")


class ConditionGt:
	def __init__(self, lineno, value0, value1):
		self.lineno = lineno
		self.value0 = value0
		self.value1 = value1
		self.print()

	def print(self):
		print(f"ConditionGt: {self.lineno, self.value0, self.value1}")
