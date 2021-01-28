class Manager:
	def __init__(self):
		self.filename = "1.txt"
		self.variables = {}
		self.arrays = {}
		self.initializedIdentifiers = {}
		self.variablesMemoryStore = ""
		self.memoryCounter = -1

	def addVariable(self, identifier, lineno):
		reg = "a"
		if identifier not in self.variables:
			self.memoryCounter += 1
			self.variables[identifier] = self.memoryCounter
			# print("AV:", identifier, self.variables[identifier], self.variables)
			if type(identifier) == int:
				self.variablesMemoryStore += f"{self.writeVariable(identifier, 'b')}"
				reg = "b"
			self.variablesMemoryStore += f"{self.writeVariable(self.variables[identifier], 'a')}STORE {reg} a\n"
		elif type(identifier) == int:
			return ""
		else:
			raise Exception(f"Trying to initialize an existing variable: {identifier}. In line: {lineno}")

	def addVariableToArray(self, identifier, variable, lineno):
		if identifier in self.arrays:
			self.variables[variable] = variable
			self.variablesMemoryStore += f"{self.writeVariable(variable, 'a')}STORE a a\n"
		else:
			raise Exception(f"Error. Array: {identifier}, doesn't exist. In line: {lineno}")

	def deleteVariable(self, identifier, lineno):
		if identifier not in self.variables:
			raise Exception(f"Trying to delete non-existing variable: {identifier}. In line: {lineno}")
		self.variables.pop(identifier)

	def getVariableAddress(self, identifier):
		print("gVA: ", self.variables, identifier)
		try:
			position = identifier[2][1]
			if identifier[1] in self.arrays:
				if type(position) is not int:
					position = self.variables[identifier[2][1]]
				# if (position < self.arrays[identifier[1]][1]) or (position > self.arrays[identifier[1]][2]):
				# 	raise Exception(f"Trying to access variable: {position}, which is not in array: {identifier[1]}")
				# else:
				return self.arrays[identifier[1]][0] + position
			else:
				raise Exception(f"Trying to access non-existing array: {identifier[1]}")
		except:
			if identifier[1] not in self.variables:
				raise Exception(f"Trying to access non-existing variable: {identifier[1]}")
			else:
				return self.variables[identifier[1]]

	def addArray(self, identifier, lineno, start, stop):
		# print(f"AddArray: {identifier, lineno, start, stop}")
		if stop < start:
			raise Exception(f"Wrong array declaration: {identifier}. In line: {lineno}")
		self.arrays[identifier] = (self.memoryCounter + 1, start, stop)
		self.memoryCounter += stop - start + 1

	def getArrayData(self, identifier):
		if identifier not in self.arrays:
			raise Exception(f"Trying to access non-existing array: {identifier}")
		else:
			return self.arrays[identifier]

	def loadVariable(self, variable, register, lineno):
		print("LV", variable, self.variables)
		if variable[0] == "number":
			if variable[1] not in self.variables:
				self.addVariable(variable[1], lineno)
			return f"{self.writeVariable(self.variables[variable[1]], 'a')}LOAD {register} a\n"
		elif variable[0] == "id":
			self.checkVariableInitialization(variable[1], lineno)
		return self.loadDataMemoryAddress(variable, register, lineno)

	def loadDataMemoryAddress(self, data, register, lineno):
		if data[0] == "id":
			self.checkVariable(data[1], lineno)
			return f"{self.writeVariable(self.variables[data[1]], 'a')}LOAD {register} a\n"
		elif data[0] == "array":
			self.checkArray(data[1], lineno)
			print("LDMA: ", self.arrays[data[1]][0], data[2][1])
			return f"{self.writeVariable(self.arrays[data[1]][0]+data[2][1], 'a')}LOAD {register} a\n"

	def writeVariable(self, number, register):
		string, array = "", []
		while number != 0:
			if number % 2 == 0:
				number //= 2
				array.append(f"SHL {register}\n")
			else:
				number -= 1
				array.append(f"INC {register}\n")
		string = string.join([i for i in reversed(array)])
		return f"RESET {register}\n" + string

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

	def checkVariableInitialization(self, identifier, lineno):
		if identifier not in self.initializedIdentifiers:
			raise Exception(f"Error. Variable {identifier} isn't initialized. Line: {lineno}")


manager = Manager()


class Program:
	def __init__(self, declarations=None, commands=None):
		self.declarations = declarations
		self.commands = commands
		self.print()

	def print(self):
		print(self.declarations)
		print(self.commands)


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
		print(f"{manager.loadVariable(self.value0, 'a', self.lineno)}{manager.loadVariable(self.value1, 'b', self.lineno)}SUB a b\nJZERO a ?\n")
