from sly import Parser
from lexer import CompilerLexer
# from ast import Manager
from ast import Manager


class CompilerParser(Parser):
	tokens = CompilerLexer.tokens

	def __init__(self):
		self.debug = False
		self.manager = Manager()

	# Program
	@_("DECLARE declarations BEGIN commands END")
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
		return f"{token.expr}{self.manager.getVariableAddress(token.id)}STORE c d\n"

	@_("IF cond THEN commands ELSE commands ENDIF")
	def command(self, token):
		if self.debug:
			print(f"Command1, condition: {token.cond}, Commands: {token.commands0, token.commands1}")
		comm0Len = self.manager.lengthOfCommands(token.commands0)
		comm1Len = self.manager.lengthOfCommands(token.commands1)
		return f"{token.cond}{comm0Len+2}\n{''.join(token.commands0)}JUMP {comm1Len+1}\n{''.join(token.commands1)}"

	@_("IF cond THEN commands ENDIF")
	def command(self, token):
		if self.debug:
			print(f"Command2, condition: {token.cond}, Commands: {token.commands}")
		return f"{token.cond}{self.manager.lengthOfCommands(token.commands)+1}\n{''.join(token.commands)}"

	@_("WHILE cond DO commands ENDWHILE")
	def command(self, token):
		if self.debug:
			print(f"Command3, condition: {token.cond}, Commands: {token.commands}")
		commandsLen = self.manager.lengthOfCommands(token.commands)
		condLen = self.manager.lengthOfCommands(token.cond)
		return f"{token.cond}{commandsLen+2}\n{''.join(token.commands)}JUMP -{commandsLen+condLen}\n"

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
		loadEaddr = self.manager.writeVariable(self.manager.variables[f"endfor{token.value1[1]}"], "a")
		varF = self.manager.loadVariable(token.value0, "f", token.lineno)
		varE = self.manager.loadVariable(token.value1, "e", token.lineno)
		self.manager.deleteVariable(f"endfor{token.value1[1]}", token.lineno)
		self.manager.deleteVariable(token.iter, token.lineno)
		commandsLen = self.manager.lengthOfCommands(token.commands)
		loadIterLen = self.manager.lengthOfCommands(loadIter)
		loadELen = self.manager.lengthOfCommands(loadE)
		return f"RESET b\n{varF}{iterAddr}STORE f a\n{varE}{loadEaddr}STORE e a\n{loadIter}{loadE}SUB b e\nJZERO b 2\nJUMP {commandsLen+loadIterLen+4}\n{''.join(token.commands)}{loadIter}INC b\nSTORE b a\nJUMP -{commandsLen+loadIterLen*2+loadELen+5}\n"

	@_("FOR iter FROM value DOWNTO value DO commands ENDFOR")
	def command(self, token):
		if self.debug:
			print(f"Command6, iterator: {token.iter}, Values: {token.value0, token.value1}, Commands: {token.commands}")
		loadIter = self.manager.loadVariable(("id", token.iter), "b", token.lineno)
		iterAddr = self.manager.writeVariable(self.manager.variables[token.iter], "a")
		self.manager.addVariable(f"endfor{token.value1[1]}", token.lineno)
		self.manager.initializedIdentifiers[f"endfor{token.value1[1]}"] = True
		loadEnd = self.manager.loadVariable(("id", f"endfor{token.value1[1]}"), "e", token.lineno)
		loadEndAddr = self.manager.writeVariable(self.manager.variables[f"endfor{token.value1[1]}"], "a")
		varF = self.manager.loadVariable(token.value0, "f", token.lineno)
		varE = self.manager.loadVariable(token.value1, "e", token.lineno)
		self.manager.deleteVariable(token.iter, token.lineno)
		self.manager.deleteVariable(f"endfor{token.value1[1]}", token.lineno)
		commandsLen = self.manager.lengthOfCommands(token.commands)
		loadIterLen = self.manager.lengthOfCommands(loadIter)
		loadEndLen = self.manager.lengthOfCommands(loadEnd)
		return f"RESET b\n{varF}{iterAddr}STORE f a\n{varE}{loadEndAddr}STORE e a\n{loadIter}{loadEnd}SUB e b\nJZERO e 2\nJUMP {commandsLen + loadIterLen + 4}\n{''.join(token.commands)}{loadIter}DEC b\nSTORE b a\nJUMP -{commandsLen + loadIterLen * 2 + loadEndLen + 5}\n"

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
		loadE = self.manager.loadVariable(token.value0, "e", token.lineno)
		loadF = self.manager.loadVariable(token.value1, "f", token.lineno)
		return f"RESET c\n{loadE}{loadF}JZERO f 8\nJODD f 4\nSHL e\nSHR f\nJUMP -3\nADD c e\nDEC f\nJUMP -7\n"

	@_("value DIV value")
	def expr(self, token):
		if self.debug:
			print(f"Expression3, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, "e", token.lineno)
		loadF = self.manager.loadVariable(token.value1, "f", token.lineno)
		return f"{loadE}{loadF}RESET b\nADD b f\nRESET c\nJZERO e 21\nJZERO f 20\nINC c\nSHL f\nRESET d\nADD d e\nSUB d f\nJZERO d 4\nSUB e f\nSHL c\nJUMP -8\nRESET d\nADD d b\nSUB d e\nJZERO d 2\nJUMP 5\nSUB e b\nINC c\nJZERO e 2\nJUMP -8\nDEC c\n"

	@_("value MOD value")
	def expr(self, token):
		if self.debug:
			print(f"Expression4, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, "e", token.lineno)
		loadF = self.manager.loadVariable(token.value1, "f", token.lineno)
		loadElen = self.manager.lengthOfCommands(loadE)
		loadFlen = self.manager.lengthOfCommands(loadF)
		return f"{loadE}{loadF}RESET c\nRESET b\nADD b f\nJZERO e {loadFlen+23}\nJZERO f {loadFlen+22}\nSUB f e\nJZERO f 3\nADD c e\nJUMP {loadFlen+18}\n{loadF}SHL f\nRESET d\nADD d e\nSUB d f\nJZERO d 3\nSUB e f\nJUMP -6\nRESET d\nADD d b\nSUB d e\nJZERO d 4\nSUB b d\nADD c b\nJUMP 4\nSUB e b\nJZERO e 2\nJUMP -9\n"

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
		return f"{loadE}RESET d\nADD d e\n{loadF}SUB d f\nJZERO d 2\nJUMP 3\nSUB f e\nJZERO f 2\nJUMP "

	@_("value NEQ value")
	def cond(self, token):
		if self.debug:
			print(f"Cond1, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, 'e', token.lineno)
		loadF = self.manager.loadVariable(token.value1, 'f', token.lineno)
		return f"{loadE}RESET d\nADD d e\n{loadF}SUB d f\nJZERO d 2\nJUMP 3\nSUB f e\nJZERO f "

	@_("value LTE value")
	def cond(self, token):
		if self.debug:
			print(f"Cond2, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, "e", token.lineno)
		loadF = self.manager.loadVariable(token.value1, "f", token.lineno)
		return f"{loadE}{loadF}SUB e f\nJZERO e 2\nJUMP "

	@_("value GTE value")
	def cond(self, token):
		if self.debug:
			print(f"Cond3, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, "e", token.lineno)
		loadF = self.manager.loadVariable(token.value1, "f", token.lineno)
		return f"{loadE}{loadF}SUB f e\nJZERO f 2\nJUMP "

	@_("value LT value")
	def cond(self, token):
		if self.debug:
			print(f"Cond4, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, "e", token.lineno)
		loadF = self.manager.loadVariable(token.value1, "f", token.lineno)
		return f"{loadE}{loadF}SUB f e\nJZERO f 2\nJUMP 2\nJUMP "

	@_("value GT value")
	def cond(self, token):
		if self.debug:
			print(f"Cond5, values: {token.value0, token.value1}")
		loadE = self.manager.loadVariable(token.value0, "e", token.lineno)
		loadF = self.manager.loadVariable(token.value1, "f", token.lineno)
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
		return "array", token.ID, ("number", token.NUM)
