import yacc
from tokenizer import tokens
import ast

precedence = (
         ('left', 'OR'),
         ('left', 'AND'),
         ('left', 'EQUALS'),
         ('left', 'GT', 'GE', 'LT', 'LE'),
         ('left', 'PLUS', 'MINUS'),
         ('left', 'TIMES', 'DIVIDE', 'MODULO')
     )

def p_program(p):
    """program: translation_unit"""
    p[0] = p[1]

def p_translation_unit(p):
    """translation_unit :	statement
    			|	translation_unit statement
    """
    if len(p) == 3:
        p[0] = ast.TranslationUnit('translation unit', [p[1], p[2]])
    else:
        p[0] = p[1]


#-------------
# Statements
#-------------

def p_statement(p):
    """statement :	assignment
		 |	func_call
		 | 	return_statement
    """
    p[0] = p[1]

def p_statement_block(p):
    """statement :     	if_statement
		 |	for_statement
		 |	while_statement
    """
    p[0] = p[1]

#for now its not possible to just declare without assignment
def p_assignment_declaration(p):
    """assignment :	INTEGER ID EQUALS expression
    		  |	REAL ID EQUALS expression
		  | 	STRING ID EQUALS expression
    		  |	CHARACTER ID expression
		  |	BOOLEAN ID EQUALS expression
    """
    p[0] = Declaration('declaration', [p[1], p[2], p[4]])

def p_assignment(p):
    'assignment : ID EQUALS expression'
    p[0] = ast.Assignment(p[0], [p[1], p[3]])

def p_assignment_increment(p):
    'assignment : ID PLUS PLUS'
    p[0] = ast.Assignment('plus_plus', p[1])

def p_assignment_decrement(p):
    'assignment : ID MINUS MINUS'
    p[0] = ast.Assignment('minus_minus', p[1])

def p_func_call(p):
    """func_call : 	CALL identifier LPAREN arguments_list RPAREN
    		 |	CALL identifier LPAREN RPAREN"""
    if len(p) == 6:
        p[0] = ast.FuncCall(p[0], p[2], p[4])
    else:
        p[0] = ast.FuncCall(p[0], p[2], None)


#------------
# Expressions
#------------

def p_arguments_list(p):
    """arguments_list : 	expression
		      |		arguments_list COMMA expression"""
    if len(p) == 2:
        p[0] = ast.ExprList()

def p_expression(p):
    """statement_expression :	simple_expression
		    	    |	func_call
    			    |	atom
    """
    p[0] = p[1]

def p_simple_expression(p):
    """simple_expression :	binary_op
    			 |	unary_op
    """
    p[0] = p[1]

 ## Atomic expressions
def p_atom_expression_1(p):
    """atom :	identifier
    	    |	constant
    """
    p[0] = p[1]

def p_identifier(p):
    'identifier : ID'
    p[0] = p[1]

def p_constant(p):
    """constant :	NUMBER
		|	SLITERAL
    		|	FLOAT
		|	TRUE
		|	FALSE
    """
    p[0] = p[1]
    
## Boolean expressions
def p_binary_op_and(p):
    'binary_op : statement_expression AND statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def p_binary_op_or(p):
    'binary_op : statement_expression OR statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def p_binary_op_gt(p):
    'binary_op : statement_expression GT statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def p_binary_op_lt(p):
    'binary_op : statement_expression LT statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def p_binary_op_ge(p):
    'binary_op : statement_expression GE statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def p_binary_op_le(p):
    'binary_op : statement_expression LE statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def p_binary_op_equals(p):
    'binary_op : statement_expression ISEQUALS statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])
    
## Numeric expressions

def p_binary_op_mod(p):
    'binary_op : statement_expression MODULO statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def p_binary_op_plus(p):
    'binary_op : statement_expression PLUS statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def p_binary_op_minus(p):
    'binary_op : statement_expression MINUS statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def p_binary_op_times(p):
    'binary_op : statement_expression TIMES statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def p_binary_op_divide(p):
    'binary_op : statement_expression DIVIDE statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

######

def p_unary_op_minus(p):
    'unary_op : MINUS statement_expression'
    p[0] = ast.UnaryOp(p[1], p[2])

def p_unary_op_plus(p):
    'unary_op : PLUS statement_expression'
    p[0] = ast.UnaryOp(p[1], p[2])

def p_unary_op_not(p):
    'unary_op : NOT statement_expression'
    p[0] = ast.UnaryOp(p[1], p[2])

#Error rule for syntax errors
def p_error(p):
    print("Syntax error")

#Build the parser
parser = yacc.yacc()
while True:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break;
    if not s: continue
    result = parser.parse(s)
    print(result)


#Following code produces "syntax error"
# with open("data.txt", "r") as f:
#     for line in f:
#         try:
#             print("length of s : %s" % len(line))
#             result = parser.parse(line)
#             #result.show()
#             print result
#         except EOFError:
#             break
# f.close()
