from sly import Parser
from lexer import CompilerLexer
from astree import Manager


class CompilerParser(Parser):
	tokens = CompilerLexer.tokens

	def __init__(self):
		self.debug = False
		self.manager = Manager()

	# Program
	@_("VAR declarations BEGIN commands END")
	def program(self, token):
		if self.debug:
			print(f"Program0: {token.declarations}, Instructions: {token.commands}")
		return token.commands

	@_("BEGIN commands END")
	def program(self, token):
		if self.debug:
			print(f"Program1: {token.commands}")
		return token.commands

	# Declarations
	@_("declarations ',' ID")
	def declarations(self, token):
		if self.debug:
			print(f"Declarations0, ID: {token.ID}. Lineno: {token.lineno}")
		self.manager.addVariable(token.ID, token.lineno)

	@_("declarations ',' ID '[' NUM ':' NUM ']'")
	def declarations(self, token):
		if self.debug:
			print(f"Declarations1, ID & array: {token.ID, token.NUM0, token.NUM1}")
		self.manager.addArray(token.ID, token.lineno, token.NUM0, token.NUM1)

	@_("ID")
	def declarations(self, token):
		if self.debug:
			print(f"Declarations2, ID: {token.ID}. Lineno: {token.lineno}")
		self.manager.addVariable(token.ID, token.lineno)

	@_("ID '[' NUM ':' NUM ']'")
	def declarations(self, token):
		if self.debug:
			print(f"Declarations3, ID & array: {token.ID, token.NUM0, token.NUM1}")
		self.manager.addArray(token.ID, token.lineno, token.NUM0, token.NUM1)

	# Commands
	@_("commands command")
	def commands(self, token):
		if self.debug:
			print(f"Commands0: {token.commands}, Command:{token.command}")
		token.commands.append(token.command)
		return token.commands

	@_("command")
	def commands(self, token):
		if self.debug:
			print(f"Commands1, command: {token.command}")
		return [token.command]

	# Command
	@_("id ASSIGN expr ';'")
	def command(self, token):
		if self.debug:
			print(f"Command0, ID: {token.id}, Expression: {token.expr}. Lineno: {token.lineno}")
		self.manager.initializedIdentifiers[token.id[1]] = True
		self.manager.checkIterator(token.id)
		return f"{token.expr}{self.manager.getVariableAddress(token.id)}SWAP c\nSTORE c\n"

	@_("IF cond THEN commands ELSE commands ENDIF")
	def command(self, token):
		if self.debug:
			print(f"Command1, condition: {token.cond}, Commands: {token.commands0, token.commands1}")
		comm0Len = self.manager.lengthOfCommands(token.commands0)
		comm1Len = self.manager.lengthOfCommands(token.commands1)
		return f"{token.cond}{comm0Len + 2}\n{''.join(token.commands0)}JUMP {comm1Len + 1}\n{''.join(token.commands1)}"

	@_("IF cond THEN commands ENDIF")
	def command(self, token):
		if self.debug:
			print(f"Command2, condition: {token.cond}, Commands: {token.commands}")
		return f"{token.cond}{self.manager.lengthOfCommands(token.commands) + 1}\n{''.join(token.commands)}"

	@_("WHILE cond DO commands ENDWHILE")
	def command(self, token):
		if self.debug:
			print(f"Command3, condition: {token.cond}, Commands: {token.commands}")
		commandsLen = self.manager.lengthOfCommands(token.commands)
		condLen = self.manager.lengthOfCommands(token.cond)
		return f"{token.cond}{commandsLen + 2}\n{''.join(token.commands)}JUMP -{commandsLen + condLen}\n"

	@_("REPEAT commands UNTIL cond ';'")
	def command(self, token):
		if self.debug:
			print(f"Command4, condition: {token.cond}, Commands: {token.commands}")
		return f"{''.join(token.commands)}{token.cond}-{self.manager.lengthOfCommands(token.commands) + self.manager.lengthOfCommands(token.cond) - 1}\n"

	@_("FOR iter FROM value TO value DO commands ENDFOR")
	def command(self, token):
		if self.debug:
			print(f"Command5, iterator: {token.iter}, Values: {token.value0, token.value1}, Commands: {token.commands}")
		iterAddr = self.manager.writeVariable(self.manager.variables[token.iter[1]], "b")
		self.manager.addVariable(f"endfor{token.value1[1]}", token.lineno)
		self.manager.initializedIdentifiers[f"endfor{token.value1[1]}"] = True
		loadE = self.manager.loadVariable(("id", f"endfor{token.value1[1]}"), "e", token.lineno)
		loadEAddr = self.manager.writeVariable(self.manager.variables[f"endfor{token.value1[1]}"], "b")
		varF = self.manager.loadVariable(token.value0, "f", token.lineno)
		varE = self.manager.loadVariable(token.value1, "e", token.lineno)
		self.manager.deleteVariable(f"endfor{token.value1[1]}", token.lineno)
		self.manager.deleteVariable(token.iter[1], token.lineno)
		del self.manager.initializedIterators[token.iter[1]]
		commandsLen = self.manager.lengthOfCommands(token.commands)
		iterAddrLen = self.manager.lengthOfCommands(iterAddr)
		loadELen = self.manager.lengthOfCommands(loadE)
		return f"{varE}{loadEAddr}SWAP e\nSTORE e\n{varF}{iterAddr}SWAP f\nSTORE f\nSWAP f\n{loadE}{iterAddr}LOAD a\nSWAP f\nRESET a\nADD e\nSUB f\nJNEG {commandsLen + iterAddrLen + 6}\n{''.join(token.commands)}{iterAddr}SWAP f\nLOAD f\nINC a\nSTORE f\nJUMP -{commandsLen + iterAddrLen * 2 + loadELen + 10}\n"

	@_("FOR iter FROM value DOWNTO value DO commands ENDFOR")
	def command(self, token):
		if self.debug:
			print(f"Command6, iterator: {token.iter}, Values: {token.value0, token.value1}, Commands: {token.commands}")
		iterAddr = self.manager.writeVariable(self.manager.variables[token.iter[1]], "b")
		self.manager.addVariable(f"endfor{token.value0[1]}", token.lineno)
		self.manager.initializedIdentifiers[f"endfor{token.value0[1]}"] = True
		loadE = self.manager.loadVariable(("id", f"endfor{token.value0[1]}"), "e", token.lineno)
		loadFAddr = self.manager.writeVariable(self.manager.variables[f"endfor{token.value0[1]}"], "b")
		varF = self.manager.loadVariable(token.value0, "f", token.lineno)
		varE = self.manager.loadVariable(token.value1, "e", token.lineno)
		self.manager.deleteVariable(token.iter[1], token.lineno)
		self.manager.deleteVariable(f"endfor{token.value0[1]}", token.lineno)
		del self.manager.initializedIterators[token.iter[1]]
		commandsLen = self.manager.lengthOfCommands(token.commands)
		iterAddrLen = self.manager.lengthOfCommands(iterAddr)
		loadELen = self.manager.lengthOfCommands(loadE)
		return f"{varE}{loadFAddr}SWAP e\nSTORE e\n{varF}{iterAddr}SWAP f\nSTORE f\nSWAP f\n{loadE}{iterAddr}LOAD a\nSWAP f\nRESET a\nADD f\nSUB e\nJNEG {commandsLen + iterAddrLen + 6}\n{''.join(token.commands)}{iterAddr}SWAP f\nLOAD f\nDEC a\nSTORE f\nJUMP -{commandsLen + iterAddrLen * 2 + loadELen + 11}\n"

	@_("READ id ';'")
	def command(self, token):
		if self.debug:
			print(f"Command7, read identifier: {token.id}")
		self.manager.initializedIdentifiers[token.id[1]] = True
		return f"{self.manager.getVariableAddress(token.id)}SWAP h\nGET\nSTORE h\n"

	@_("WRITE value ';'")
	def command(self, token):
		if self.debug:
			print(f"Command8, write value: {token.value}")
		self.manager.checkVariableInitialization(token.value[1], token.lineno)
		return f"{self.manager.getVariableAddress(token.value)}LOAD a\nPUT\n"

	# Expression
	@_("value PLUS value")
	def expr(self, token):
		if self.debug:
			print(f"Expression0, values: {token.value0, token.value1}")
		loadC = f"{self.manager.loadVariable(token.value0, 'c', token.lineno)}"
		loadB = f"{self.manager.loadVariable(token.value1, 'b', token.lineno)}"
		return f"{loadC}{loadB}SWAP b\nADD c\nSWAP c\n"

	@_("value MINUS value")
	def expr(self, token):
		if self.debug:
			print(f"Expression1, values: {token.value0, token.value1}")
		loadC = self.manager.loadVariable(token.value0, 'c', token.lineno)
		loadB = self.manager.loadVariable(token.value1, 'b', token.lineno)
		return f"{loadC}{loadB}SWAP c\nSUB b\nSWAP c\n"

	@_("value TIMES value")
	def expr(self, token):
		if self.debug:
			print(f"Expression2, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, "e", token.lineno)
		loadF = self.manager.loadVariable(token.value1, "f", token.lineno)
		loadFlen = self.manager.lengthOfCommands(loadF)
		isOdd = self.checkIfNumberIsOdd("f")
		isOddLen = self.manager.lengthOfCommands(isOdd)
		return f"RESET c\n{loadE}SWAP e\nJZERO {loadFlen + isOddLen + 31}\nSWAP e\n{loadF}SWAP f\nJPOS 9\nRESET g\nSWAP g\nSUB g\nSWAP e\nRESET g\nSWAP g\nSUB g\nSWAP e\nJZERO {isOddLen + 19}\n{self.checkIfNumberIsOdd('f')}JZERO 7\nSWAP c\nADD e\nSWAP c\nDEC f\nSWAP f\nJUMP -{isOddLen + 7}\nRESET a\nADD e\nRESET h\nINC h\nSHIFT h\nSWAP e\nSWAP f\nRESET h\nDEC h\nSHIFT h\nJUMP -{isOddLen + 18}\n"

	def checkIfNumberIsOdd(self, register):
		return f"SWAP g\nRESET a\nADD g\nRESET {register}\nDEC {register}\nSHIFT {register}\nRESET {register}\nINC {register}\nSHIFT {register}\nRESET {register}\nSWAP {register}\nADD g\nSWAP {register}\nSWAP g\nSUB g\n"

	@_("value DIV value")
	def expr(self, token):
		if self.debug:
			print(f"Expression3, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, "e", token.lineno)
		loadF = self.manager.loadVariable(token.value1, "f", token.lineno)
		loadFlen = self.manager.lengthOfCommands(loadF)
		# h is a carry
		b = f"RESET a\nADD e\nSUB f\nJZERO 18\nINC c\nRESET a\nADD e\nSUB f\nJNEG 12\nRESET b\nINC b\nSWAP f\n" \
			f"SHIFT b\nSWAP f\nRESET b\nINC b\nSWAP c\nSHIFT b\nSWAP c\nJUMP -14\n"
		c = f"RESET d\nRESET g\nSWAP d\nADD f\nSWAP d\nSWAP g\nADD c\nSWAP g\nRESET a\nADD e\nSUB f\nJNEG 8\nSWAP f\n" \
			f"ADD d\nSWAP f\nSWAP c\nADD g\nSWAP c\nJUMP -10\n"
		d = f"DEC g\nSWAP g\nJZERO 20\nSWAP g\nINC g\nSWAP f\nSUB d\nSWAP f\nSWAP c\nSUB g\nSWAP c\nRESET b\nDEC b\n" \
			f"SWAP d\nSHIFT b\nSWAP d\nRESET b\nDEC b\nSWAP g\nSHIFT b\nSWAP g\nJUMP -32\n"
		e = f"RESET a\nADD f\nSUB e\nJZERO 8\nSWAP f\nSUB d\nSWAP f\nSWAP e\nSUB f\nSWAP e\nJZERO 2\nDEC c\n"

		bLen = self.manager.lengthOfCommands(b)
		cLen = self.manager.lengthOfCommands(c)
		dLen = self.manager.lengthOfCommands(d)
		eLen = self.manager.lengthOfCommands(e)
		checkBigger = f"RESET a\n" \
					  f"ADD e\n" \
					  f"SUB f\n" \
					  f"JNEG 4\n" \
					  f"JZERO 2\n" \
					  f"JUMP 3\n" \
					  f"INC c\n" \
					  f"JUMP {bLen + cLen + dLen + eLen + 1}\n"
		checkBiggerLen = self.manager.lengthOfCommands(checkBigger)
		a = f"RESET c\n" \
			f"RESET h\n" \
			f"{loadE}" \
			f"SWAP e\n" \
			f"JPOS 6\n" \
			f"JZERO {checkBiggerLen + loadFlen + bLen + cLen + dLen + eLen + 18}\n" \
			f"RESET g\n" \
			f"SWAP g\n" \
			f"SUB g\n" \
			f"DEC h\n" \
			f"SWAP e\n" \
			f"{loadF}" \
			f"SWAP f\n" \
			f"JPOS 10\n" \
			f"JZERO {checkBiggerLen + bLen + cLen + dLen + eLen + 10}\n" \
			f"RESET g\n" \
			f"SWAP g\n" \
			f"SUB g\n" \
			f"SWAP f\n" \
			f"RESET a\n" \
			f"DEC a\n" \
			f"SUB h\n" \
			f"SWAP h\n" \
			f"SWAP f\n"
		ret = f"{a}{checkBigger}{b}{c}{d}{e}SWAP h\nJZERO 5\nRESET a\nSUB c\nSWAP c\nDEC c\n"
		return ret

	@_("value MOD value")
	def expr(self, token):
		if self.debug:
			print(f"Expression4, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, "e", token.lineno)
		loadF = self.manager.loadVariable(token.value1, "f", token.lineno)
		loadElen = self.manager.lengthOfCommands(loadE)
		loadFlen = self.manager.lengthOfCommands(loadF)
		carry = f"SWAP h\nJZERO 4\nSWAP g\nSUB c\nSWAP c\n{loadF}SWAP f\nJPOS 5\nSWAP f\nRESET a\nSUB c\nSWAP c\n"
		carryLen = self.manager.lengthOfCommands(carry)
		c = f"RESET g\nRESET d\nSWAP g\nADD f\nSWAP g\nSWAP d\nADD c\nSWAP d\nRESET a\nADD e\nSUB f\nJNEG 9\nJZERO 8\n" \
			f"SWAP f\nADD g\nSWAP f\nSWAP c\nADD d\nSWAP c\nJUMP -11\n"
		cLen = self.manager.lengthOfCommands(c)
		d = f"SWAP f\nSUB g\nSWAP f\nDEC d\nSWAP d\nJNEG 16\nJZERO 15\nSWAP d\nINC d\nSWAP c\nSUB d\nSWAP c\n" \
			f"RESET b\nDEC b\nSWAP g\nSHIFT b\nSWAP g\nSWAP d\nSHIFT b\nSWAP d\nJUMP -32\nSWAP d\n"
		dLen = self.manager.lengthOfCommands(d)
		e = f"RESET c\nRESET a\nSWAP f\nADD g\nSWAP f\nADD f\nSUB e\nJNEG 14\nJZERO 13\nSWAP f\nSUB g\n" \
			f"SWAP f\nSWAP e\nSUB f\nJNEG 6\nJZERO 5\nSWAP e\nSWAP c\nADD e\nSWAP c\nSWAP e\n"
		eLen = self.manager.lengthOfCommands(e)
		doubleValues = f"INC c\nRESET a\nADD e\nSUB f\nJNEG 11\nJZERO 10\nSWAP f\nRESET b\nINC b\nSHIFT b\n" \
					   f"SWAP f\nSWAP c\nSHIFT b\nSWAP c\nJUMP -13\n"
		doubleValuesLen = self.manager.lengthOfCommands(doubleValues)
		checkBigger = f"RESET a\n" \
					  f"ADD e\n" \
					  f"SUB f\n" \
					  f"JNEG 3\n" \
					  f"JZERO 5\n" \
					  f"JUMP 5\n" \
					  f"SWAP c\n" \
					  f"ADD e\n" \
					  f"SWAP c\n" \
					  f"JUMP {doubleValuesLen + cLen + dLen + eLen + carryLen + 1}\n"
		checkBiggerLen = self.manager.lengthOfCommands(checkBigger)
		a = f"RESET c\n" \
			f"RESET h\n" \
			f"{loadE}" \
			f"SWAP e\n" \
			f"JPOS 6\n" \
			f"RESET g\n" \
			f"SWAP g\n" \
			f"SUB g\n" \
			f"INC h\n" \
			f"JZERO {checkBiggerLen + loadFlen + doubleValuesLen + cLen + dLen + eLen + carryLen + 16}\n" \
			f"SWAP e\n" \
			f"{loadF}" \
			f"SWAP f\n" \
			f"JPOS 5\n" \
			f"RESET g\n" \
			f"SWAP g\n" \
			f"SUB g\n" \
			f"DEC h\n" \
			f"JZERO {checkBiggerLen + doubleValuesLen + cLen + dLen + eLen + carryLen + 2}\n" \
			f"SWAP f\n"
		return f"{a}{checkBigger}{doubleValues}{c}{d}{e}{carry}"

	@_("value")
	def expr(self, token):
		if self.debug:
			print(f"Expression5, value: {token.value}")
		return f"{self.manager.loadVariable(token.value, 'c', None)}"

	# Condition
	@_("value EQ value")
	def cond(self, token):
		if self.debug:
			print(f"Cond0, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, 'e', token.lineno)
		loadF = self.manager.loadVariable(token.value1, 'f', token.lineno)
		return f"{loadE}{loadF}SWAP e\nSUB f\nJZERO 2\nJUMP "

	@_("value NEQ value")
	def cond(self, token):
		if self.debug:
			print(f"Cond1, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, 'e', token.lineno)
		loadF = self.manager.loadVariable(token.value1, 'f', token.lineno)
		return f"{loadE}{loadF}SWAP e\nSUB f\nJZERO 2\nJUMP 2\nJUMP "

	@_("value LEQ value")
	def cond(self, token):
		if self.debug:
			print(f"Cond2, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, "e", token.lineno)
		loadF = self.manager.loadVariable(token.value1, "f", token.lineno)
		return f"{loadE}{loadF}SWAP e\nSUB f\nJNEG 3\nJZERO 2\nJUMP "

	@_("value GEQ value")
	def cond(self, token):
		if self.debug:
			print(f"Cond3, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, "e", token.lineno)
		loadF = self.manager.loadVariable(token.value1, "f", token.lineno)
		return f"{loadE}{loadF}SWAP e\nSUB f\nJPOS 3\nJZERO 2\nJUMP "

	@_("value LE value")
	def cond(self, token):
		if self.debug:
			print(f"Cond4, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, "e", token.lineno)
		loadF = self.manager.loadVariable(token.value1, "f", token.lineno)
		return f"{loadF}{loadE}SWAP f\nSUB e\nJNEG 3\nJZERO 2\nJUMP 2\nJUMP "

	@_("value GE value")
	def cond(self, token):
		if self.debug:
			print(f"Cond5, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, "e", token.lineno)
		loadF = self.manager.loadVariable(token.value1, "f", token.lineno)
		return f"{loadE}{loadF}SWAP e\nSUB f\nJNEG 3\nJZERO 2\nJUMP 2\nJUMP "

	# Value
	@_("NUM")
	def value(self, token):
		if self.debug:
			print(f"Value0, number: {token.NUM}")
		self.manager.addVariable(token.NUM, token.lineno)
		return "number", token.NUM, token.lineno

	@_("id")
	def value(self, token):
		if self.debug:
			print(f"Value1, identifier: {token.id}")
		return token.id

	# Identifier
	@_("ID")
	def iter(self, token):
		if self.debug:
			print(f"Identifier0: {token.ID}")
		self.manager.addVariable(token.ID, token.lineno)
		self.manager.initializedIdentifiers[token.ID] = True
		self.manager.initializedIterators[token.ID] = True
		return "iter", token.ID

	@_("ID")
	def id(self, token):
		if self.debug:
			print(f"Identifier1, ID identifier: {token.ID}")
		return "id", token.ID

	@_("ID '[' ID ']'")
	def id(self, token):
		if self.debug:
			print(f"Identifier2, ID identifiers: {token.ID0, token.ID1}")
		return "array", token.ID0, ("id", token.ID1)

	@_("ID '[' NUM ']'")
	def id(self, token):
		if self.debug:
			print(f"Identifier3: {token.ID}, Number: {token.NUM}")
		return "array", token.ID, ("number", token.NUM)
