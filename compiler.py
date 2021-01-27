from lexer import CompilerLexer
from parser import CompilerParser
from ast import *

if __name__ == "__main__":
	lexer = CompilerLexer()
	parser = CompilerParser()
	with open("testy2020/2-fib.imp") as text:
		tokens = lexer.tokenize(text.read())
		parsed = parser.parse(tokens)
		writeToFile = f"{manager.variablesMemoryStore}{''.join(parsed)}HALT"
		print(writeToFile)
		with open("1.txt", "w") as fw:
			fw.write(writeToFile)
			print("Saved to 1.txt successfully")

	print("Comp: ", parsed)
