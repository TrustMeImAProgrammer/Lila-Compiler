import sys
import symbol_table
import parser
import ast

path = sys.argv[1]
file = open(path, 'r')
source_code = file.read()
file.close()
ast = parser.parse(source_code)
symbol_table = SymbolTable()

def type_check(node):
    if node:
        





