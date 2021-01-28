from sly import Parser
from lexer import CompilerLexer
from ast import *

memoryWrite = ""


class CompilerParser(Parser):
	tokens = CompilerLexer.tokens

	def __init__(self):
		self.debug = True

	# Program
	@_("DECLARE declarations BEGIN commands END")
	def program(self, token):
		if self.debug:
			print(f"Program0: {token.declarations}, Instructions: {token.commands}")
		# print(manager.variablesMemoryStore)
		return token.commands

	@_("BEGIN commands END")
	def program(self, token):
		if self.debug:
			print(f"Program1: {token.commands}")
		return token.commands

	# Declarations
	@_("declarations ',' ID")
	def declarations(self, token):
		global memoryWrite
		if self.debug:
			print(f"Declarations0, ID: {token.ID}. Lineno: {token.lineno}")
		manager.addVariable(token.ID, token.lineno)

	@_("declarations ',' ID '(' NUM ':' NUM ')'")
	def declarations(self, token):
		if self.debug:
			print(f"Declarations1, ID & array: {token.ID, token.NUM0, token.NUM1}")
		manager.addArray(token.ID, token.lineno, token.NUM0, token.NUM1)

	@_("ID")
	def declarations(self, token):
		if self.debug:
			print(f"Declarations2, ID: {token.ID}. Lineno: {token.lineno}")
		manager.addVariable(token.ID, token.lineno)

	@_("ID '(' NUM ':' NUM ')'")
	def declarations(self, token):
		if self.debug:
			print(f"Declarations3, ID & array: {token.ID, token.NUM0, token.NUM1}")
		manager.addArray(token.ID, token.lineno, token.NUM0, token.NUM1)

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
			print(f"Command0, ID: {token.id}, Expression: {token.expr}")
		manager.initializedIdentifiers[token.id[1]] = True
		print(token.expr, "tokenID", token.id)
		return f"{token.expr}{manager.writeVariable(manager.getVariableAddress(token.id), 'b')}STORE c b\n"

	@_("IF cond THEN commands ELSE commands ENDIF")
	def command(self, token):
		if self.debug:
			print(f"Command1, condition: {token.cond}, Commands: {token.commands0, token.commands1}")
		return f"{token.cond}{manager.lengthOfCommands(token.commands0)+1}\n{''.join(token.commands0)}JUMP {manager.lengthOfCommands(token.commands1)}\n{''.join(token.commands1)}"

	@_("IF cond THEN commands ENDIF")
	def command(self, token):
		if self.debug:
			print(f"Command2, condition: {token.cond}, Commands: {token.commands}")
		return f"{token.cond}{manager.lengthOfCommands(token.commands)}\n{''.join(token.commands)}"

	@_("WHILE cond DO commands ENDWHILE")
	def command(self, token):
		if self.debug:
			print(f"Command3, condition: {token.cond}, Commands: {token.commands}")
		return CommandWhile(token.lineno, token.cond, token.commands)

	@_("REPEAT commands UNTIL cond ';'")
	def command(self, token):
		if self.debug:
			print(f"Command4, condition: {token.cond}, Commands: {token.commands}")
		return token

	@_("FOR iter FROM value TO value DO commands ENDFOR")
	def command(self, token):
		if self.debug:
			print(f"Command5, iterator: {token.iter}, Values: {token.value0, token.value1}, Commands: {token.commands}")
		return f"{manager.loadIterator(token.iter, 'c', token.lineno)}{manager.loadVariable(token.value0, 'b', token.lineno)}{manager.loadVariable(token.value0, 'e', token.lineno)}{manager.loadVariable(token.value1, 'f', token.lineno)}INC b\nSUB f b\nJZERO f {manager.lengthOfCommands(token.commands)}\n{''.join(token.commands)}\nJUMP -{manager.lengthOfCommands(token.commands)}\n"

	@_("FOR iter FROM value DOWNTO value DO commands ENDFOR")
	def command(self, token):
		if self.debug:
			print(f"Command6, iterator: {token.iter}, Values: {token.value0, token.value1}, Commands: {token.commands}")
		return token

	@_("READ id ';'")
	def command(self, token):
		if self.debug:
			print(f"Command7, read identifier: {token.id}")
		manager.initializedIdentifiers[token.id[1]] = True
		return f"{manager.loadVariable(token.id, 'a', token.lineno)}GET a\n"

	@_("WRITE value ';'")
	def command(self, token):
		if self.debug:
			print(f"Command8, write value: {token.value}")
		print("WR", token.value)
		return f"{manager.writeVariable(manager.getVariableAddress(token.value), 'd')}PUT d\n"

	# Expression
	@_("value ADD value")
	def expr(self, token):
		if self.debug:
			print(f"Expression0, values: {token.value0, token.value1}")
		return f"{manager.loadVariable(token.value0, 'c', token.lineno)}{manager.loadVariable(token.value1, 'b', token.lineno)}ADD c b\n"

	@_("value SUB value")
	def expr(self, token):
		if self.debug:
			print(f"Expression1, values: {token.value0, token.value1}")
		return f"{manager.loadVariable(token.value0, 'c', token.lineno)}{manager.loadVariable(token.value1, 'b', token.lineno)}SUB c b\n"

	@_("value MUL value")
	def expr(self, token):
		if self.debug:
			print(f"Expression2, values: {token.value0, token.value1}")
		return f"{manager.loadVariable(token.value0, 'c', token.lineno)}{manager.loadVariable(token.value0, 'e', token.lineno)}{manager.loadVariable(token.value1, 'b', token.lineno)}DEC b\nJZERO b 3\nADD c e\nJUMP -3\n"

	@_("value DIV value")
	def expr(self, token):
		if self.debug:
			print(f"Expression3, values: {token.value0, token.value1}")
		return f"{manager.loadVariable(token.value0, 'e', token.lineno)}{manager.loadVariable(token.value1, 'b', token.lineno)}RESET c\n{manager.loadVariable(token.value1, 'f', token.lineno)}JZERO f 8\nJZERO e 7\nSUB f e\nJZERO f 2\nJUMP 2\nINC c\nSUB e b\nJUMP -8\n"

	@_("value MOD value")
	def expr(self, token):
		if self.debug:
			print(f"Expression4, values: {token.value0, token.value1}")
		return f"{manager.loadVariable(token.value0, 'e', token.lineno)}{manager.loadVariable(token.value1, 'b', token.lineno)}{manager.loadVariable(token.value1, 'f', token.lineno)}JZERO f 9\nRESET c\nJZERO e 7\nSUB f e\nJZERO f 3\nADD c e\nJUMP 3\nSUB e b\nJUMP -8\n"

	@_("value")
	def expr(self, token):
		if self.debug:
			print(f"Expression5, value: {token.value}")
		return f"{manager.loadVariable(token.value, 'c', None)}"

	# Condition
	@_("value EQ value")
	def cond(self, token):
		if self.debug:
			print(f"Cond0, values: {token.value0, token.value1}")
		return ConditionEq(token.lineno, token.value0, token.value1)

	@_("value NEQ value")
	def cond(self, token):
		if self.debug:
			print(f"Cond1, values: {token.value0, token.value1}")
		return ConditionNeq(token.lineno, token.value0, token.value1)

	@_("value LTE value")
	def cond(self, token):
		if self.debug:
			print(f"Cond2, values: {token.value0, token.value1}")
		return ConditionLte(token.lineno, token.value0, token.value1)

	@_("value GTE value")
	def cond(self, token):
		if self.debug:
			print(f"Cond3, values: {token.value0, token.value1}")
		return ConditionGte(token.lineno, token.value0, token.value1)

	@_("value LT value")
	def cond(self, token):
		if self.debug:
			print(f"Cond4, values: {token.value0, token.value1}")
		return f"{manager.loadVariable(token.value0, 'e', token.lineno)}{manager.loadVariable(token.value1, 'f', token.lineno)}SUB f e\nJZERO f 2\nJUMP 2\nJUMP "

	@_("value GT value")
	def cond(self, token):
		if self.debug:
			print(f"Cond5, values: {token.value0, token.value1}")
		return f"{manager.loadVariable(token.value0, 'e', token.lineno)}{manager.loadVariable(token.value1, 'f', token.lineno)}SUB e f\nJZERO e 2\nJUMP 2\nJUMP "

	# Value
	@_("NUM")
	def value(self, token):
		if self.debug:
			print(f"Value0, number: {token.NUM}")
		manager.addVariable(token.NUM, token.lineno)
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
		manager.addVariable(token.ID, token.lineno)
		manager.initializedIdentifiers[token.ID] = True
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
		manager.addVariableToArray(token.ID, token.NUM, token.lineno)
		return "array", token.ID, ("number", token.NUM)
