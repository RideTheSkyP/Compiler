from sly import Lexer


class CompilerLexer(Lexer):
	tokens = {
		"VAR", "BEGIN", "END", "NUM", "ID",
		"PLUS", "MINUS", "TIMES", "DIV", "MOD", "ASSIGN",
		"EQ", "NEQ", "LE", "GE", "LEQ", "GEQ",
		"READ", "WRITE", "DO",
		"FOR", "ENDFOR", "FROM", "TO", "DOWNTO",
		"REPEAT", "UNTIL",
		"WHILE", "ENDWHILE",
		"IF", "ENDIF", "THEN", "ELSE",
	}

	NUM = r"\-?\d+"
	ID = r"[_a-z]+"

	ENDWHILE = r"ENDWHILE"
	ENDFOR = r"ENDFOR"
	DOWNTO = r"DOWNTO"
	REPEAT = r"REPEAT"
	ASSIGN = r"ASSIGN"
	WRITE = r"WRITE"
	UNTIL = r"UNTIL"
	WHILE = r"WHILE"
	ENDIF = r"ENDIF"
	BEGIN = r"BEGIN"
	TIMES = r"TIMES"
	MINUS = r"MINUS"
	PLUS = r"PLUS"
	READ = r"READ"
	THEN = r"THEN"
	ELSE = r"ELSE"
	FROM = r"FROM"
	DIV = r"DIV"
	MOD = r"MOD"
	VAR = r"VAR"
	FOR = r"FOR"
	NEQ = r"NEQ"
	LEQ = r"LEQ"
	GEQ = r"GEQ"
	END = r"END"
	EQ = r"EQ"
	LE = r"LE"
	GE = r"GE"
	TO = r"TO"
	IF = r"IF"
	DO = r"DO"

	ignore = " \t"
	ignore_comment = r"\([^\(\)]*\)"
	ignore_newline = r"\n+"
	literals = "[];,:"

	@_(NUM)
	def NUM(self, token):
		token.value = int(token.value)
		return token

	@_(ignore_newline)
	def ignore_newline(self, token):
		self.lineno += token.value.count("\n")

	@_(ignore_comment)
	def ignore_comment(self, token):
		self.lineno += token.value.count("\n")

	def error(self, token):
		print(f"Illegal character {token.value[0]} in line {self.lineno}")
		self.index += 1
