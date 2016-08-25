import sys
import os
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
output = sys.argv[1].split('.')[0]
outfile = open(output + ".asm", 'w')
outfile.write(code)
outfile.close()
result = os.system("nasm -f elf -g -F stabs " + output + ".asm")
if result:
    print "Error during assembly, is NASM installed and added to $PATH?"
    sys.exit(1)
linked_library = ""
for function in codegen.builtin_functions:
    result = os.system("nasm -f elf -g -F stabs " + function+ ".asm")
    if result:
        print "Error during assembly, is NASM installed and added to $PATH?"
        sys.exit(1)
    linked_library += function + ".o "
result = os.system("ld -m elf_i386 " + output + ".o " + linked_library + "-o " + output)
if result:
    print "Error linking the program"
    sys.exit(1)

