from sly import Parser
from lexer import CompilerLexer
from ast import *


class CompilerParser(Parser):
	tokens = CompilerLexer.tokens

	def __init__(self):
		self.debug = False

	# Program
	@_("DECLARE declarations BEGIN commands END")
	def program(self, token):
		if self.debug:
			print(f"Program0: {token.declarations}, Instructions: {token.commands}")
		return Program(token.declarations, token.commands)

	@_("BEGIN commands END")
	def program(self, token):
		if self.debug:
			print(f"Program1: {token.commands}")
		return Program(commands=token.commands)

	# Declarations
	@_("declarations ',' ID")
	def declarations(self, token):
		if self.debug:
			print(f"Declarations0, ID: {token.ID}")
		return Declarations(token.ID, token.lineno)

	@_("declarations ',' ID '(' NUM ':' NUM ')'")
	def declarations(self, token):
		if self.debug:
			print(f"Declarations1, ID & array: {token.ID, token.NUM0, token.NUM1}")
		return Declarations(token.ID, token.lineno, token.NUM0, token.NUM1)

	@_("ID")
	def declarations(self, token):
		if self.debug:
			print(f"Declarations2, ID: {token.ID}")
		return Declarations(token.ID, token.lineno)

	@_("ID '(' NUM ':' NUM ')'")
	def declarations(self, token):
		if self.debug:
			print(f"Declarations3, ID & array: {token.ID, token.NUM0, token.NUM1}")
		return Declarations(token.ID, token.lineno, token.NUM0, token.NUM1)

	# Commands
	@_("commands command")
	def commands(self, token):
		if self.debug:
			print(f"Commands0: {token.commands}, Command:{token.command}")
		return token

	@_("command")
	def commands(self, token):
		if self.debug:
			print(f"Commands1, command: {token.command}")
		return token

	# Command
	@_("id ASSIGN expr ';'")
	def command(self, token):
		if self.debug:
			print(f"Command0, ID: {token.id}, Expression: {token.expr}")
		return CommandAssign(token.lineno, token.id, token.expr)

	@_("IF cond THEN commands ELSE commands ENDIF")
	def command(self, token):
		if self.debug:
			print(f"Command1, condition: {token.cond}, Commands: {token.commands0, token.commands1}")
		return CommandIf(token.lineno, token.cond, token.commands0, commandElse=token.commands1)

	@_("IF cond THEN commands ENDIF")
	def command(self, token):
		if self.debug:
			print(f"Command2, condition: {token.cond}, Commands: {token.commands}")
		return CommandIf(token.lineno, token.cond, token.commands)

	@_("WHILE cond DO commands ENDWHILE")
	def command(self, token):
		if self.debug:
			print(f"Command3, condition: {token.cond}, Commands: {token.commands}")
		return CommandWhile(token.lineno, token.cond, token.commands)

	@_("REPEAT commands UNTIL cond ';'")
	def command(self, token):
		if self.debug:
			print(f"Command3, condition: {token.cond}, Commands: {token.commands}")
		return token

	@_("FOR iter FROM value TO value DO commands ENDFOR")
	def command(self, token):
		if self.debug:
			print(f"Command3, iterator: {token.iter}, Values: {token.value0, token.value1}, Commands: {token.commands}")
		return CommandFor(token.lineno, token.iter, token.value0, token.value1, token.commands)

	@_("FOR iter FROM value DOWNTO value DO commands ENDFOR")
	def command(self, token):
		if self.debug:
			print(f"Command4, iterator: {token.iter}, Values: {token.value0, token.value1}, Commands: {token.commands}")
		return CommandFor(token.lineno, token.iter, token.value0, token.value1, token.commands, downTo=True)

	@_("READ id ';'")
	def command(self, token):
		if self.debug:
			print(f"Command5, read identifier: {token.id}")
		return CommandRead(token.lineno, token.id)

	@_("WRITE value ';'")
	def command(self, token):
		if self.debug:
			print(f"Command6, write value: {token.value}")
		return CommandWrite(token.lineno, token.value)

	# Expression
	@_("value")
	def expr(self, token):
		if self.debug:
			print(f"Expression0, value: {token.value}")
		return ExpressionValue(token.lineno, token.value)

	@_("value ADD value")
	def expr(self, token):
		if self.debug:
			print(f"Expression1, values: {token.value0, token.value1}")
		return ExpressionAdd(token.lineno, token.value0, token.value0)

	@_("value SUB value")
	def expr(self, token):
		if self.debug:
			print(f"Expression2, values: {token.value0, token.value1}")
		return ExpressionSub(token.lineno, token.value0, token.value0)

	@_("value MUL value")
	def expr(self, token):
		if self.debug:
			print(f"Expression3, values: {token.value0, token.value1}")
		return ExpressionMul(token.lineno, token.value0, token.value0)

	@_("value DIV value")
	def expr(self, token):
		if self.debug:
			print(f"Expression4, values: {token.value0, token.value1}")
		return ExpressionDiv(token.lineno, token.value0, token.value0)

	@_("value MOD value")
	def expr(self, token):
		if self.debug:
			print(f"Expression5, values: {token.value0, token.value1}")
		return ExpressionMod(token.lineno, token.value0, token.value0)

	# Condition
	@_("value EQ value")
	def cond(self, token):
		if self.debug:
			print(f"Cond0, values: {token.value0, token.value1}")
		return token

	@_("value NEQ value")
	def cond(self, token):
		if self.debug:
			print(f"Cond1, values: {token.value0, token.value1}")
		return token

	@_("value LTE value")
	def cond(self, token):
		if self.debug:
			print(f"Cond2, values: {token.value0, token.value1}")
		return token

	@_("value GTE value")
	def cond(self, token):
		if self.debug:
			print(f"Cond3, values: {token.value0, token.value1}")
		return token

	@_("value LT value")
	def cond(self, token):
		if self.debug:
			print(f"Cond4, values: {token.value0, token.value1}")
		return token

	@_("value GT value")
	def cond(self, token):
		if self.debug:
			print(f"Cond5, values: {token.value0, token.value1}")
		return token

	# Value
	@_("NUM")
	def value(self, token):
		if self.debug:
			print(f"Value0, number: {token.NUM}")
		return token

	@_("id")
	def value(self, token):
		if self.debug:
			print(f"Value1, identifier: {token.id}")
		return token

	# Identifier
	@_("ID")
	def iter(self, token):
		if self.debug:
			print(f"Identifier0: {token.ID}")
		return token

	@_("ID")
	def id(self, token):
		if self.debug:
			print(f"Identifier1, ID identifier: {token.ID}")
		return token

	@_("ID '(' ID ')'")
	def id(self, token):
		if self.debug:
			print(f"Identifier2, ID identifiers: {token.ID0, token.ID1}")
		return token

	@_("ID '(' NUM ')'")
	def id(self, token):
		if self.debug:
			print(f"Identifier3: {token.ID}, Number: {token.NUM}")
		return token
