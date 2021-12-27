from lexer import CompilerLexer
from parser import CompilerParser
import sys

if __name__ == "__main__":
	try:
		testFile = sys.argv[1]
		filename = sys.argv[2]
		with open(testFile) as text:
			lexer = CompilerLexer()
			parser = CompilerParser()
			tokens = lexer.tokenize(text.read())
			parsed = parser.parse(tokens)
			writeToFile = f"{parser.manager.variablesMemoryStore}{''.join(parsed)}HALT"
			with open(filename, "w") as fw:
				fw.write(writeToFile)
				print(f"Saved to {filename} successfully")
	except Exception as e:
		print("Usage: python3 compiler.py [test file name] [output file name]")
		print(f"Exception: {e}")


