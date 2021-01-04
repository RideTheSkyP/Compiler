from sly import Parser
from lexer import CompilerLexer


class CompilerParser(Parser):
	tokens = CompilerLexer.tokens

	def __init__(self):
		self.debug = True

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

	@_("DO commands WHILE cond ENDDO")
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
