from sly import Parser
from lexer import CompilerLexer
# from ast import Manager
from ast import Manager


class CompilerParser(Parser):
	tokens = CompilerLexer.tokens

	def __init__(self):
		self.debug = True
		self.manager = Manager()

	# Program
	@_("DECLARE declarations BEGIN commands END")
	def program(self, token):
		if self.debug:
			print(f"Program0: {token.declarations}, Instructions: {token.commands}")
		# print(self.manager.variablesMemoryStore)
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

	@_("declarations ',' ID '(' NUM ':' NUM ')'")
	def declarations(self, token):
		if self.debug:
			print(f"Declarations1, ID & array: {token.ID, token.NUM0, token.NUM1}")
		self.manager.addArray(token.ID, token.lineno, token.NUM0, token.NUM1)

	@_("ID")
	def declarations(self, token):
		if self.debug:
			print(f"Declarations2, ID: {token.ID}. Lineno: {token.lineno}")
		self.manager.addVariable(token.ID, token.lineno)

	@_("ID '(' NUM ':' NUM ')'")
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
		# print(token.expr, "tokenID", token.id)
		return f"{token.expr}{self.manager.getVariableAddress(token.id)}STORE c d\n"

	@_("IF cond THEN commands ELSE commands ENDIF")
	def command(self, token):
		if self.debug:
			print(f"Command1, condition: {token.cond}, Commands: {token.commands0, token.commands1}")
		return f"{token.cond}{self.manager.lengthOfCommands(token.commands0)}\n{''.join(token.commands0)}JUMP {self.manager.lengthOfCommands(token.commands1)+1}\n{''.join(token.commands1)}"

	@_("IF cond THEN commands ENDIF")
	def command(self, token):
		if self.debug:
			print(f"Command2, condition: {token.cond}, Commands: {token.commands}")
		return f"{token.cond}{self.manager.lengthOfCommands(token.commands)}\n{''.join(token.commands)}"

	@_("WHILE cond DO commands ENDWHILE")
	def command(self, token):
		if self.debug:
			print(f"Command3, condition: {token.cond}, Commands: {token.commands}")
		return f"{token.cond}{self.manager.lengthOfCommands(token.commands)+2}\n{''.join(token.commands)}JUMP -{self.manager.lengthOfCommands(token.commands)+self.manager.lengthOfCommands(token.cond)}\n"

	@_("REPEAT commands UNTIL cond ';'")
	def command(self, token):
		if self.debug:
			print(f"Command4, condition: {token.cond}, Commands: {token.commands}")
		return f"{''.join(token.commands)}{token.cond}-{self.manager.lengthOfCommands(token.commands)+self.manager.lengthOfCommands(token.cond)-1}\n"

	@_("FOR iter FROM value TO value DO commands ENDFOR")
	def command(self, token):
		if self.debug:
			print(f"Command5, iterator: {token.iter}, Values: {token.value0, token.value1}, Commands: {token.commands}")
		loadIter = self.manager.loadVariable(("id", token.iter), "b", token.lineno)
		iterAddr = self.manager.writeVariable(self.manager.variables[token.iter], "a")
		self.manager.addVariable(f"endfor{token.value1[1]}", token.lineno)
		self.manager.initializedIdentifiers[f"endfor{token.value1[1]}"] = True
		loadE = self.manager.loadVariable(("id", f"endfor{token.value1[1]}"), "e", token.lineno)
		varEAddr = self.manager.writeVariable(self.manager.variables[f"endfor{token.value1[1]}"], "a")
		varF = self.manager.loadVariable(token.value0, "f", token.lineno)
		varE = self.manager.loadVariable(token.value1, "e", token.lineno)
		self.manager.deleteVariable(f"endfor{token.value1[1]}", token.lineno)
		self.manager.deleteVariable(token.iter, token.lineno)
		commandsLen = self.manager.lengthOfCommands(token.commands)
		loadIterLen = self.manager.lengthOfCommands(loadIter)
		loadELen = self.manager.lengthOfCommands(loadE)
		return f"{varF}{iterAddr}STORE f a\n{varE}{varEAddr}STORE e a\n{loadIter}{loadE}SUB b e\nJZERO b 2\nJUMP {commandsLen+loadIterLen+4}\n{''.join(token.commands)}{loadIter}INC b\nSTORE b a\nJUMP -{commandsLen+loadIterLen*2+loadELen+5}\n"

	@_("FOR iter FROM value DOWNTO value DO commands ENDFOR")
	def command(self, token):
		if self.debug:
			print(f"Command6, iterator: {token.iter}, Values: {token.value0, token.value1}, Commands: {token.commands}")
		loadIter = self.manager.loadVariable(("id", token.iter), "b", token.lineno)
		storeIter = self.manager.storeIterator(token.iter, "e", token.lineno)
		varE = self.manager.loadVariable(token.value0, "e", token.lineno)
		varF = self.manager.loadVariable(token.value1, "f", token.lineno)
		self.manager.deleteVariable(token.iter, token.lineno)
		commandsLen = self.manager.lengthOfCommands(token.commands)
		loadIterLen = self.manager.lengthOfCommands(loadIter)
		return f"{varE}{storeIter}{loadIter}{varF}SUB b e\nJZERO b 2\nJUMP {commandsLen+loadIterLen*2+6}\n{''.join(token.commands)}{loadIter}SUB b f\nJZERO b {loadIterLen+4}\n{loadIter}DEC b\nSTORE b a\nJUMP -{commandsLen+loadIterLen*2+7}\n"

	@_("READ id ';'")
	def command(self, token):
		if self.debug:
			print(f"Command7, read identifier: {token.id}")
		self.manager.initializedIdentifiers[token.id[1]] = True
		return f"{self.manager.getVariableAddress(token.id)}GET d\n"

	@_("WRITE value ';'")
	def command(self, token):
		if self.debug:
			print(f"Command8, write value: {token.value}")
		return f"{self.manager.getVariableAddress(token.value)}PUT d\n"

	# Expression
	@_("value ADD value")
	def expr(self, token):
		if self.debug:
			print(f"Expression0, values: {token.value0, token.value1}")
		loadC = self.manager.loadVariable(token.value0, 'c', token.lineno)
		loadB = self.manager.loadVariable(token.value1, 'b', token.lineno)
		return f"{loadC}{loadB}ADD c b\n"

	@_("value SUB value")
	def expr(self, token):
		if self.debug:
			print(f"Expression1, values: {token.value0, token.value1}")
		loadC = self.manager.loadVariable(token.value0, 'c', token.lineno)
		loadB = self.manager.loadVariable(token.value1, 'b', token.lineno)
		return f"{loadC}{loadB}SUB c b\n"

	@_("value MUL value")
	def expr(self, token):
		if self.debug:
			print(f"Expression2, values: {token.value0, token.value1}")
		# loadC = self.manager.loadVariable(token.value0, 'c', token.lineno)
		loadE = self.manager.loadVariable(token.value0, "e", token.lineno)
		loadF = self.manager.loadVariable(token.value1, "f", token.lineno)
		return f"RESET c\n{loadE}{loadF}JZERO f 8\nJODD f 4\nSHL e\nSHR f\nJUMP -3\nADD c e\nDEC f\nJUMP -7\n"

	@_("value DIV value")
	def expr(self, token):
		if self.debug:
			print(f"Expression3, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, "e", token.lineno)
		loadF = self.manager.loadVariable(token.value1, "f", token.lineno)
		loadElen = self.manager.lengthOfCommands(loadE)
		loadFlen = self.manager.lengthOfCommands(loadF)
		# return f"{loadE}{loadF}RESET b\nRESET c\nSUB e f\nJZERO e {loadFlen+loadElen+22}\n{loadE}{loadF}JZERO e 23\nJZERO f 22\nADD b f\nINC c\nSHL f\nRESET d\nADD d e\nSUB d f\nJZERO d 4\nSUB e f\nSHL c\nJUMP -7\nRESET d\nADD d b\nSUB d e\nJZERO d 2\nJUMP 5\nSUB e b\nINC c\nJZERO e 2\nJUMP -8\n"
		# return f"{loadE}RESET b\nADD b e\nRESET c\n{loadF}JZERO e {loadFlen*2+33}\nJZERO f {loadFlen*2+32}\nINC c\nSUB b f\nJZERO b 2\nJUMP 3\nSUB f e\nJZERO f 2\nJUMP {loadFlen*2+22}\nRESET b\nADD b e\n{loadF}ADD f b\nJZERO f 2\nJUMP {loadFlen+20}\n{loadF}RESET b\nADD b f\nSHL f\nRESET d\nADD d e\nSUB d f\nJZERO d 4\nSUB e f\nSHL c\nJUMP -7\nRESET d\nADD d b\nSUB d e\nJZERO d 2\nJUMP 5\nSUB e b\nINC c\nJZERO e 2\nJUMP -8\n"
		## Works div
		# return f"{loadE}{loadF}RESET b\nADD b f\nRESET c\nJZERO e 21\nJZERO f 20\nINC c\nSHL f\nRESET d\nADD d e\nSUB d f\nJZERO d 4\nSUB e f\nSHL c\nJUMP -8\nRESET d\nADD d b\nSUB d e\nJZERO d 2\nJUMP 5\nSUB e b\nINC c\nJZERO e 2\nJUMP -8\nDEC c\n"

		return f"{loadE}{loadF}RESET b\nADD b f\nRESET c\nJZERO e 21\nJZERO f 20\nINC c\nSHL f\nRESET d\nADD d e\nSUB d f\nJZERO d 4\nSUB e f\nSHL c\nJUMP -8\nRESET d\nADD d b\nSUB d e\nJZERO d 2\nJUMP 5\nSUB e b\nINC c\nJZERO e 2\nJUMP -8\nDEC c\n"

	@_("value MOD value")
	def expr(self, token):
		if self.debug:
			print(f"Expression4, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, "e", token.lineno)
		loadF = self.manager.loadVariable(token.value1, "f", token.lineno)
		loadElen = self.manager.lengthOfCommands(loadE)
		loadFlen = self.manager.lengthOfCommands(loadF)
		return f"{loadE}RESET b\nADD b e\nRESET c\n{loadF}JZERO e {loadElen+loadFlen+31}\nJZERO f {loadElen+loadFlen+30}\nSUB e f\nJZERO e 2\nJUMP 3\nSUB f b\nJZERO f {loadElen+loadFlen+25}\n{loadF}{loadE}SUB b f\nJZERO b 2\nJUMP 3\nADD c e\nJUMP 20\nRESET b\nADD b f\nSHL f\nRESET d\nADD d e\nSUB d f\nJZERO d 3\nSUB e f\nJUMP -6\nRESET d\nADD d b\nSUB d e\nJZERO d 2\nJUMP 6\nSUB e b\nRESET c\nADD c e\nJZERO e 2\nJUMP -9\n"

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
		return f"{loadE}RESET b\nADD b e\n{loadF}SUB b f\nJZERO b 2\nJUMP 3\nSUB f e\nJZERO f 2\nJUMP "

	@_("value NEQ value")
	def cond(self, token):
		if self.debug:
			print(f"Cond1, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, 'e', token.lineno)
		loadF = self.manager.loadVariable(token.value1, 'f', token.lineno)
		return f"{loadE}RESET b\nADD b e\n{loadF}SUB b f\nJZERO b 2\nJUMP 3\nSUB f e\nJZERO f "

	@_("value LTE value")
	def cond(self, token):
		if self.debug:
			print(f"Cond2, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, 'e', token.lineno)
		loadF = self.manager.loadVariable(token.value1, 'f', token.lineno)
		return f"{loadE}{loadF}SUB e f\nJZERO e 2\nJUMP "

	@_("value GTE value")
	def cond(self, token):
		if self.debug:
			print(f"Cond3, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, 'e', token.lineno)
		loadF = self.manager.loadVariable(token.value1, 'f', token.lineno)
		return f"{loadE}{loadF}SUB f e\nJZERO f 2\nJUMP "

	@_("value LT value")
	def cond(self, token):
		if self.debug:
			print(f"Cond4, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, 'e', token.lineno)
		loadF = self.manager.loadVariable(token.value1, 'f', token.lineno)
		return f"{loadE}{loadF}SUB f e\nJZERO f 2\nJUMP 2\nJUMP "

	@_("value GT value")
	def cond(self, token):
		if self.debug:
			print(f"Cond5, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, 'e', token.lineno)
		loadF = self.manager.loadVariable(token.value1, 'f', token.lineno)
		return f"{loadE}{loadF}SUB e f\nJZERO e 2\nJUMP 2\nJUMP "

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
		return token.ID

	@_("ID")
	def id(self, token):
		if self.debug:
			print(f"Identifier1, ID identifier: {token.ID}")
		return "id", token.ID

	@_("ID '(' ID ')'")
	def id(self, token):
		if self.debug:
			print(f"Identifier2, ID identifiers: {token.ID0, token.ID1}")
		return "array", token.ID0, ("id", token.ID1)

	@_("ID '(' NUM ')'")
	def id(self, token):
		if self.debug:
			print(f"Identifier3: {token.ID}, Number: {token.NUM}")
		# self.manager.addVariableToArray(token.ID, token.NUM, token.lineno)
		return "array", token.ID, ("number", token.NUM)
