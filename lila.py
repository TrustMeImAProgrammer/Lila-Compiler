import sys
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

code = codegen.generate(ast)
output = sys.argv[1].split('.')[0] + ".asm"
outfile = open(output, 'w')
outfile.write(code)
outfile.close()

