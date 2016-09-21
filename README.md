#Lila compiler

Lila is a strongly typed, imperative programming language designed by me as part of a university project.

This compiler translates a lila source code file into x86 NASM Assembler. It then calls nasm to assemble the file and finally calls the GNU linker (ld) to link and generate a linux executable file.
As a result, in order to test the compiler both nasm and ld must be installed and added to the system $PATH. Also, the compiler is written in python 2 and will not work under python 3 (although it should be very easy to get it working).

Each file is separated in the logical steps the compiler takes:

1. tokenizer.py uses the lexer from <a href="https://github.com/dabeaz/ply">ply</a> to define the tokens available in lila

2. parser.py similarly uses ply to parse the lila source code and builds a syntax tree

3. analyzer.py performs semantic analysis

4. codegen.py generates the actual assembler code

5. lila.py is the actual file that calls all other files and does the assembling and linking

## Installation

Just do:
``` bash
$ git clone https://github.com/TrustMeImAProgrammer/Lila-Compiler.git
$ cd Lila-Compiler
```
To compile a source file simply do:

```bash
python lila.py sourcecode.lila
```


After this an executable file called sourcecode will be generated if everything went well.

I've tried to make Lila's syntax very readable while taking a few ideas from C's and python's syntax.
I'll upload a list of example lila files to run tests on and get an idea of lila's syntax.

## License

    Copyright (C) 2016 Carlos Manrique
    
    Lila is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    Lila is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with Kernel Adiutor.  If not, see <http://www.gnu.org/licenses/>.
