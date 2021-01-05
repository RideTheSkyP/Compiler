from sly import Parser
from lexer import CompilerLexer


class CompilerParser(Parser):
	tokens = CompilerLexer.tokens

	def __init__(self):
		self.debug = True

	# Program
	@_("DECLARE declarations BEGIN commands END")
	def program(self, token):
		if self.debug:
			print(f"Declarations: {token.declarations}, Instructions: {token.instructions}")
		return token

	@_("BEGIN commands END")
	def program(self, token):
		if self.debug:
			print(f"Instructions: {token.instructions}")
		return token

	# Declarations
	@_("declarations ',' ID")
	def declarations(self, token):
		if self.debug:
			print(f"Declaration ID: {token.ID}")
		return token

	@_("declarations ',' ID '(' NUM ':' NUM ')'")
	def declarations(self, token):
		if self.debug:
			print(f"Declaration ID & array: {token.ID, token.NUM0, token.NUM1}")
		return token

	@_("ID")
	def declarations(self, token):
		if self.debug:
			print(f"Declaration ID: {token.ID}")
		return token

	@_("ID '(' NUM ':' NUM ')'")
	def declarations(self, token):
		if self.debug:
			print(f"Declaration ID & array: {token.ID, token.NUM0, token.NUM1}")
		return token

	# Commands
	@_("commands command")
	def commands(self, token):
		if self.debug:
			print(f"Commands: {token.commands}, Command:{token.command}")
		return token

	@_("command")
	def commands(self, token):
		if self.debug:
			print(f"Command: {token.command}")
		return token

	# Command
	@_("id ASSIGN expr ';'")
	def command(self, token):
		if self.debug:
			print(f"ID: {token.id}, Expression: {token.expr}")
		return token

	@_("IF cond THEN commands ELSE commands ENDIF")
	def command(self, token):
		if self.debug:
			print(f"Condition: {token.cond}, Commands: {token.commands0, token.commands1}")
		return token

	@_("IF cond THEN commands ENDIF")
	def command(self, token):
		if self.debug:
			print(f"Condition: {token.cond}, Commands: {token.commands}")
		return token

	@_("WHILE cond DO commands ENDWHILE")
	def command(self, token):
		if self.debug:
			print(f"Condition: {token.cond}, Commands: {token.commands}")
		return token

	@_("REPEAT commands UNTIL cond ';'")
	def command(self, token):
		if self.debug:
			print(f"Condition: {token.cond}, Commands: {token.commands}")
		return token

	@_("FOR iter FROM value TO value DO commands ENDFOR")
	def command(self, token):
		if self.debug:
			print(f"Iterator: {token.iter}, Values: {token.value0, token.value1}, Commands: {token.commands}")
		return token

	@_("FOR iter FROM value DOWNTO value DO commands ENDFOR")
	def command(self, token):
		if self.debug:
			print(f"Iterator: {token.iter}, Values: {token.value0, token.value1}, Commands: {token.commands}")
		return token

	@_("READ id ';'")
	def command(self, token):
		if self.debug:
			print(f"Read identifier: {token.id}")
		return token

	@_("WRITE value ';'")
	def command(self, token):
		if self.debug:
			print(f"Write value: {token.value}")
		return token

	# Expression
	@_("value")
	def expr(self, token):
		if self.debug:
			print(f"Expression0 value: {token.value}")
		return token

	@_("value ADD value")
	def expr(self, token):
		if self.debug:
			print(f"Expression1 values: {token.value0, token.value1}")
		return token

	@_("value SUB value")
	def expr(self, token):
		if self.debug:
			print(f"Expression2 values: {token.value0, token.value1}")
		return token

	@_("value MUL value")
	def expr(self, token):
		if self.debug:
			print(f"Expression3 values: {token.value0, token.value1}")
		return token

	@_("value DIV value")
	def expr(self, token):
		if self.debug:
			print(f"Expression4 values: {token.value0, token.value1}")
		return token

	@_("value MOD value")
	def expr(self, token):
		if self.debug:
			print(f"Expression5 values: {token.value0, token.value1}")
		return token

	# Condition
	@_("value EQ value")
	def cond(self, token):
		if self.debug:
			print(f"Cond1 values: {token.value0, token.value1}")
		return token

	@_("value NEQ value")
	def cond(self, token):
		if self.debug:
			print(f"Cond2 values: {token.value0, token.value1}")
		return token

	@_("value LTE value")
	def cond(self, token):
		if self.debug:
			print(f"Cond3 values: {token.value0, token.value1}")
		return token

	@_("value GTE value")
	def cond(self, token):
		if self.debug:
			print(f"Cond4 values: {token.value0, token.value1}")
		return token

	@_("value LT value")
	def cond(self, token):
		if self.debug:
			print(f"Cond5 values: {token.value0, token.value1}")
		return token

	@_("value GT value")
	def cond(self, token):
		if self.debug:
			print(f"Cond6 values: {token.value0, token.value1}")
		return token

	# Value
	@_("NUM")
	def value(self, token):
		if self.debug:
			print(f"Number: {token.NUM}")
		return token

	@_("id")
	def value(self, token):
		if self.debug:
			print(f"Identifier: {token.id}")
		return token

	# Identifier
	@_("ID")
	def iter(self, token):
		if self.debug:
			print(f"Identifier: {token.ID}")
		return token

	@_("ID")
	def id(self, token):
		if self.debug:
			print(f"ID identifier: {token.ID}")
		return token

	@_("ID '(' ID ')'")
	def id(self, token):
		if self.debug:
			print(f"ID identifiers: {token.ID0, token.ID1}")
		return token

	@_("ID '(' NUM ')'")
	def id(self, token):
		if self.debug:
			print(f"Identifier: {token.ID}, Number: {token.NUM}")
		return token
