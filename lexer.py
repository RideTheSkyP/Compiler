from sly import Lexer


class CompilerLexer(Lexer):
	tokens = {
		"DECLARE", "BEGIN", "END", "NUM", "ID",
		"ADD", "SUB", "MUL", "DIV", "MOD", "ASSIGN",
		"EQ", "NEQ", "LT", "GT", "LTE", "GTE",
		"READ", "WRITE", "DO",
		"FOR", "ENDFOR", "FROM", "TO", "DOWNTO",
		"REPEAT", "UNTIL",
		"WHILE", "ENDWHILE",
		"IF", "ENDIF", "THEN", "ELSE",
	}

	NUM = r"\d+"
	ID = r"[_a-z]+"

	ADD = r"\+"
	SUB = r"\-"
	MUL = r"\*"
	DIV = r"\/"
	MOD = r"\%"
	ASSIGN = r"\:="
	EQ = r"\="
	NEQ = r"\!="
	LTE = r"\<="
	GTE = r"\>="
	LT = r"\<"
	GT = r"\>"

	ENDWHILE = r"ENDWHILE"
	DECLARE = r"DECLARE"
	ENDFOR = r"ENDFOR"
	DOWNTO = r"DOWNTO"
	REPEAT = r"REPEAT"
	WRITE = r"WRITE"
	UNTIL = r"UNTIL"
	WHILE = r"WHILE"
	ENDIF = r"ENDIF"
	BEGIN = r"BEGIN"
	READ = r"READ"
	THEN = r"THEN"
	ELSE = r"ELSE"
	FROM = r"FROM"
	FOR = r"FOR"
	END = r"END"
	TO = r"TO"
	IF = r"IF"
	DO = r"DO"

	ignore = " \t"
	ignore_comment = r"\[[^\]]*\]"
	ignore_newline = r"\n+"
	literals = "();,:"

	@_(NUM)
	def NUM(self, token):
		token.value = int(token.value)
		return token

	@_(ignore_newline)
	def ignore_newline(self, token):
		self.lineno += token.value.count("\n")

	def error(self, token):
		print(f"Illegal character {token.value[0]} in line {self.lineno}")
		self.index += 1
