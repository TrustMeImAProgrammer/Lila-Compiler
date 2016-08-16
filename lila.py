import sys
import symbol_table
import parser
import analyzer
import codegen

input = sys.argv[1]
infile = open(input, 'r')
source_code = infile.read()
infile.close()
ast = parser.parse(source_code)
analyzer.analyze(ast)
print "Analyzed all lines successfully"

# code = codegen.generate_code(ast)
# output = sys.argv[1].split('.')[0]
# outfile = open(output, 'w')

