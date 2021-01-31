class Manager:
	def __init__(self):
		self.variables = {}
		self.arrays = {}
		self.initializedIdentifiers = {}
		self.variablesMemoryStore = ""
		self.memoryCounter = -1

	def addVariable(self, identifier, lineno):
		if identifier not in self.variables:
			self.memoryCounter += 1
			self.variables[identifier] = self.memoryCounter
			if type(identifier) == int:
				self.variablesMemoryStore += f"{self.writeVariable(identifier, 'b')}"
			else:
				self.variablesMemoryStore += f"{self.writeVariable(0, 'b')}"
			self.variablesMemoryStore += f"{self.writeVariable(self.variables[identifier], 'a')}STORE b a\n"
		elif type(identifier) == int:
			pass
		else:
			raise Exception(f"Trying to initialize an existing variable: {identifier}. In line: {lineno}")

	def deleteVariable(self, identifier, lineno):
		if identifier not in self.variables:
			raise Exception(f"Trying to delete non-existing variable: {identifier}. In line: {lineno}")
		self.variables.pop(identifier)

	def getVariableAddress(self, identifier):
		try:
			if identifier[2][0] == "id":
				pos = self.variables[identifier[2][1]]
				return f"{self.writeVariable(self.arrays[identifier[1]][0], 'f')}{self.loadVariable(identifier[2], 'd', None)}ADD d f\n"
			elif identifier[2][0] == "number":
				pos = self.arrays[identifier[1]][0] + identifier[2][1]
				return self.writeVariable(pos, "d")

			else:
				raise Exception(f"Trying to access non-existing array: {identifier[1]}")
		except:
			if identifier[1] not in self.variables:
				raise Exception(f"Trying to access non-existing variable: {identifier[1]}")
			else:
				return self.writeVariable(self.variables[identifier[1]], "d")

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

	def loadVariable(self, variable, register, lineno):
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
			pos = data[2][1]
			if data[2][0] == "id":
				pos = self.variables[data[2][1]]

			return f"{self.writeVariable(self.arrays[data[1]][0], 'f')}{self.loadVariable(data[2], 'd', None)}ADD d f\nLOAD {register} d\n"

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

	def lengthOfCommands(self, array):
		if type(array) == list:
			loc = sum([len(i.splitlines()) for i in array])
		else:
			loc = len(array.splitlines())
		return loc
