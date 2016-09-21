This is a university project in which we design a programming language and write a compiler for it.

This compiler translates a lila source code file into x86 NASM Assembler. It then calls nasm to assemble the file and finally calls the GNU linker (ld) to link and generate a linux executable file.
As a result, in order to test the compiler both nasm and ld must be installed and added to the system $PATH. Also, the compiler is written in python 2 and will not work under python 3 (although it should be very easy to get it working).

Each file is separated in the logical steps the compiler takes:

1. tokenizer.py uses the lexer from <a href="https://github.com/dabeaz/ply">ply</a> to define the tokens available in lila

2. parser.py similarly uses ply to parse the lila source code and builds a syntax tree

3. analyzer.py performs semantic analysis

4. codegen.py generates the actual assembler code

5. lila.py is the actual file that calls all other files and does the assembling and linking

To test the compiler simply do:


python lila.py sourcecode.lila


After this an executable file called sourcecode will be generated if everything went well.

I've tried to make Lila's syntax very readable while taking a few ideas from C's and python's syntax.
I'll upload a list of example lila files to run tests on and get an idea of lila's syntax.
