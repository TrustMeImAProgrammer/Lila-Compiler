import sys
import symbol_table
import parser
import analyzer

path = sys.argv[1]
file = open(path, 'r')
source_code = file.read()
file.close()
ast = parser.parse(source_code)
analyzer.analyze(ast)
