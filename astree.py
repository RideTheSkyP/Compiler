class Manager:
	def __init__(self):
		self.variables = {}
		self.arrays = {}
		self.initializedIdentifiers = {}
		self.variablesMemoryStore = ""
		self.registers = ["b", "c", "d", "e", "f", "g", "h"]
		self.memoryCounter = -1

	def addVariable(self, identifier, lineno):
		print("addVariable", identifier, lineno)
		if identifier not in self.variables:
			self.memoryCounter += 1
			self.variables[identifier] = self.memoryCounter
			if type(identifier) == int:
				self.variablesMemoryStore += f"{self.writeVariable(identifier, 'b')}SWAP b\n"
			else:
				self.variablesMemoryStore += f"{self.writeVariable(0, 'b')}"
			self.variablesMemoryStore += f"{self.writeVariable(self.variables[identifier], 'h')}SWAP b\nSTORE b\n"
		elif type(identifier) == int:
			pass
		else:
			raise Exception(f"Trying to initialize an existing variable: {identifier}. In line: {lineno}")
		print(self.variables)

	def deleteVariable(self, identifier, lineno):
		if identifier not in self.variables:
			raise Exception(f"Trying to delete non-existing variable: {identifier}. In line: {lineno}")
		self.variables.pop(identifier)

	def emptyRegister(self, register):
		if register not in self.registers:
			self.registers.append(register)
		else:
			raise Exception("Register already free!")

	def getFreeRegister(self):
		if len(self.registers) > 0:
			return self.registers[0]
		else:
			raise Exception("No free registers!")

	def getVariableAddress(self, identifier):
		print("getVariableAddress", identifier)
		try:
			if identifier[2][0] == "id":
				pos = self.variables[identifier[2][1]]
				print("id", pos)
				return f"{self.writeVariable(self.arrays[identifier[1]][0], 'b')}SWAP f\n{self.loadVariable(identifier[2], 'b', None)}ADD f\n"
			elif identifier[2][0] == "number":
				pos = self.calculateDistance(identifier)
				print("number", pos)
				return f"{self.writeVariable(pos, 'b')}"
			else:
				raise Exception(f"Trying to access non-existing array: {identifier[1]}")
		except:
			print("ex")
			if identifier[1] not in self.variables:
				raise Exception(f"Trying to access non-existing variable: {identifier[1]}")
			else:
				return f"{self.writeVariable(self.variables[identifier[1]], 'b')}"

	def calculateDistance(self, identifier):
		print("calculateDistance", identifier)
		memCount = 0
		for i in range(self.arrays[identifier[1]][1], self.arrays[identifier[1]][2]+1):
			if i == identifier[2][1]:
				break
			memCount += 1
		pos = self.arrays[identifier[1]][0] + memCount
		print("pos", pos)
		return pos

	def addArray(self, identifier, lineno, start, stop):
		print("addArray", identifier, lineno, start, stop)
		if stop < start:
			raise Exception(f"Wrong array declaration: {identifier}. In line: {lineno}")
		self.arrays[identifier] = (self.memoryCounter + 1, start, stop)
		self.memoryCounter += stop - start + 1

	def getArrayData(self, identifier):
		print("getArrayData", identifier)
		if identifier not in self.arrays:
			raise Exception(f"Trying to access non-existing array: {identifier}")
		else:
			return self.arrays[identifier]

	def loadVariable(self, variable, register, lineno):
		print("loadVariable", variable, register, lineno)
		if variable[0] == "number":
			if variable[1] not in self.variables:
				self.addVariable(variable[1], lineno)
			return f"{self.writeVariable(self.variables[variable[1]], register)}LOAD a\nSWAP {register}\n"
		elif variable[0] == "id":
			self.checkVariableInitialization(variable[1], lineno)
		return self.loadDataMemoryAddress(variable, register, lineno)

	def loadDataMemoryAddress(self, data, register, lineno):
		print("loadDataMemoryAddress", data, register, lineno)
		if data[0] == "id":
			self.checkVariable(data[1], lineno)
			return f"{self.writeVariable(self.variables[data[1]], register)}LOAD a\nSWAP {register}\n"
		elif data[0] == "array":
			self.checkArray(data[1], lineno)
			pos = data[2][1]
			if data[2][0] == "id":
				pos = self.variables[data[2][1]]
			return f"{self.writeVariable(self.calculateDistance(data), 'd')}LOAD a\nSWAP {register}\n"

	def writeVariable(self, number, register):
		print("writeVariable", number, register)
		array, increment, countPower = [f"RESET a\n"], "INC", 0
		if number < 0:
			number = abs(number)
			increment = "DEC"
		elif number == 0:
			array.append(f"RESET {register}\n")

		for b in str(bin(number))[2:]:
			if b == "1":
				if countPower > 0:
					array.append(f"RESET {register}\n" + "".join([f"INC {register}\n" for _ in range(countPower)]) + f"SHIFT {register}\n")
				array.append(f"{increment} a\n")
				countPower = 0
			countPower += 1
		if countPower - 1 != 0:
			array.append(f"RESET {register}\n" + "".join([f"INC {register}\n" for _ in range(countPower - 1)]) + f"SHIFT {register}\n")
		return f"".join(array)

	def checkVariable(self, identifier, lineno):
		print("checkVariable", identifier, lineno)
		if identifier not in self.variables:
			if identifier not in self.arrays:
				raise Exception(f"Error. Variable {identifier} isn't initialized. Line: {lineno}")
			else:
				raise Exception(f"Error. Variable {identifier} initialized like an array. Line: {lineno}")

	def checkArray(self, identifier, lineno):
		print("checkArray", identifier, lineno)
		if identifier not in self.arrays:
			if identifier not in self.variables:
				raise Exception(f"Error. Array {identifier} isn't initialized. Line: {lineno}")
			else:
				raise Exception(f"Error. Array {identifier} initialized like a variable. Line: {lineno}")

	def checkVariableInitialization(self, identifier, lineno):
		print("checkVariableInitialization", identifier, lineno)
		if identifier not in self.initializedIdentifiers:
			raise Exception(f"Error. Variable {identifier} isn't initialized. Line: {lineno}")

	def lengthOfCommands(self, array):
		if type(array) == list:
			loc = sum([len(i.splitlines()) for i in array])
		else:
			loc = len(array.splitlines())
		return loc
