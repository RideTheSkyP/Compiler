from lexer import CompilerLexer
from parser import CompilerParser


if __name__ == "__main__":
	lexer = CompilerLexer()
	parser = CompilerParser()
	# text = ""
	with open("testy2020/program1.imp") as text:
		tokens = lexer.tokenize(text.read())
		# print([tok for tok in tokens])
		parser.parse(tokens)

	# while True:
	# 	try:
	# 		text = input("")
	# 	except EOFError:
	# 		print("Error")
	# 	if text:
	# 		parser.parse(lexer.tokenize(text))
