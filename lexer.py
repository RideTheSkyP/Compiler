from sly import Lexer


class CompilerLexer(Lexer):
	tokens = {
		"DECLARE", "IN", "END", "NUM", "ID",
		"ADD", "SUB", "MUL", "DIV", "POWER", "MOD", "ASSIGN",
		"EQ", "NEQ", "LT", "GT", "LEQ", "GEQ",
		"LPAREN", "RPAREN",
		"READ", "WRITE",
		"COLON", "SEMICOLON",
		"FOR", "ENDFOR", "FROM", "TO", "DOWNTO",
		"WHILE", "ENDWHILE",
		"IF", "ENDIF", "THEN", "ELSE",
		"DO", "ENDDO",
	}
	ignore = " \t"
	ignore_comment = r"\[[^\]]*\]"
	ignore_newline = r"\n+"

	NUM = r"\d+"
	ID = r"[_a-z]+"

	ADD = r"\+"
	SUB = r"\-"
	MUL = r"\*"
	DIV = r"\/"
	POWER = r"\^"
	MOD = r"\%"
	ASSIGN = r":="
	LPAREN = r"\("
	RPAREN = r"\)"
	EQ = r"\="
	NEQ = r"\!="
	LT = r"\<"
	GT = r"\>"
	LTE = r"\<="
	GTE = r"\>="

	COLON = r"\:"
	SEMICOLON = r"\;"

	DECLARE = r"DECLARE"
	IN = r"IN"
	END = r"END"
	READ = r"READ"
	WRITE = r"WRITE"
	FOR = r"FOR"
	ENDFOR = r"ENDFOR"
	FROM = r"FROM"
	TO = r"TO"
	DOWNTO = r"DOWNTO"
	WHILE = r"WHILE"
	ENDWHILE = r"ENDWHILE"
	IF = r"IF"
	ENDIF = r"ENDIF"
	THEN = r"THEN"
	ELSE = r"ELSE"
	DO = r"DO"
	ENDDO = r"ENDDO"

	def ignore_newline(self, token):
		self.lineno += token.value.count("\n")

	def error(self, token):
		print(f"Illegal character {token.value[0]} in line {self.lineno}")
		self.index += 1
