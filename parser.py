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
    """program : translation_unit"""
    p[0] = p[1]

def p_translation_unit(p):
    """translation_unit :	statement
    			|	translation_unit statement
    """
    if len(p) == 3:
        p[1].children.append(p[2])
        p[0] = p[1]
    else:
        p[0] = ast.TranslationUnit('translation_unit', [p[1]])


#-------------
# Statements
#-------------

def p_statement(p):
    """statement :	assignment
		 |	func_call
		 | 	return_statement
		 | 	func_declaration
    """
    p[0] = p[1]

def p_statement_block(p):
    """statement :     	if_statement
		 |	while_statement
    """
    p[0] = p[1]

def p_assignment(p):
    'assignment : ID EQUALS expression'
    p[0] = ast.Assignment('=', None, [p[1], p[3]])

#for now its not possible to just declare without assignment
def p_assignment_declaration(p):
    """assignment : type_info ID EQUALS expression
    """
    p[0] = ast.Assignment('=', p[1], [p[2], p[4]])

def p_assignment_increment(p):
    'assignment : ID PLUSPLUS'
    p[0] = ast.Assignment('plus_plus', None, [p[1]])

def p_assignment_decrement(p):
    'assignment : ID MINUSMINUS'
    p[0] = ast.Assignment('minus_minus', [p[1]])

def p_func_call(p):
    """func_call : 	CALL identifier LPAREN arguments_list RPAREN
    		 |	CALL identifier LPAREN RPAREN"""
    if len(p) == 6:
        p[0] = ast.FuncCall('func_call',[p[2], p[4]])
    else:
        p[0] = ast.FuncCall('func_call', [p[2]])

def p_return_statement(p):
    'return_statement : RETURN expression'
    p[0] = ast.Return('return', [p[2]])

#nested function declarations are not allowed, unlike gcc an error will be thrown,
#this must be done during tree traversal
def p_func_declaration(p):
    """func_declaration :	FUNCTION ID LPAREN params_list RPAREN LBRACKET translation_unit RBRACKET
    			|	FUNCTION ID LPAREN RPAREN LBRACKET translation_unit RBRACKET
    """
    if len(p) == 9:
        p[0] = ast.FuncDecl('func_declaration', p[4], [p[2], p[7]])
    else:
        p[0] = ast.FuncDecl('func_declaration', None, [p[2], p[6]])

def p_if_statement(p):
    'if_statement : IF binary_op LBRACKET translation_unit RBRACKET'
    p[0] = ast.If('if', [p[2], p[4]])

def p_while_statement(p):
    'while_statement : WHILE binary_op LBRACKET translation_unit RBRACKET'
    p[0] = ast.While('while', [p[2], p[4]])

#TODO: add for and else rules

#-----------
# Lists
#-----------


def p_params_list(p):
    """params_list :	parameter_declaration
	           |	params_list COMMA parameter_declaration
    """
    if len(p) == 2:
        p[0] = ast.ParamsList('params_list', [p[1]])
    else:
        p[1].append(p[3])

def p_parameter_declaration(p):
    'parameter_declaration : type_info ID'
    p[0] = ast.ParamDecl('param_decl', [p[1], p[2]])

def p_arguments_list(p):
    """arguments_list : 	expression
		      |		arguments_list COMMA expression"""
    if len(p) == 2:
        p[0] = ast.ArgList('arg_list', [p[1]])
    else:
        p[1].append(p[3])
        p[0] = p[1]
    
#------------
# Expressions
#------------

def p_expression(p):
    """expression :	simple_expression
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
def p_atom_expression_(p):
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
    'binary_op : expression AND expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def p_binary_op_or(p):
    'binary_op : expression OR expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def p_binary_op_gt(p):
    'binary_op : expression GT expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def p_binary_op_lt(p):
    'binary_op : expression LT expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def p_binary_op_ge(p):
    'binary_op : expression GE expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def p_binary_op_le(p):
    'binary_op : expression LE expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def p_binary_op_equals(p):
    'binary_op : expression ISEQUALS expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])
    
## Numeric expressions

def p_binary_op_mod(p):
    'binary_op : expression MODULO expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def p_binary_op_plus(p):
    'binary_op : expression PLUS expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def p_binary_op_minus(p):
    'binary_op : expression MINUS expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def p_binary_op_times(p):
    'binary_op : expression TIMES expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def p_binary_op_divide(p):
    'binary_op : expression DIVIDE expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

######

def p_unary_op_minus(p):
    'unary_op : MINUS expression'
    p[0] = ast.UnaryOp(p[1], [p[2]])

def p_unary_op_plus(p):
    'unary_op : PLUS expression'
    p[0] = ast.UnaryOp(p[1], [p[2]])

def p_unary_op_not(p):
    'unary_op : NOT expression'
    p[0] = ast.UnaryOp(p[1], [p[2]])

def p_type_info(p):
    """type_info : INT
		 | STRING
    		 | REAL
		 | BOOLEAN
		 | CHAR
    """
    p[0] = p[1]

#Error rule for syntax errors
def p_error(p):
    print("Syntax error")

def parse(source):
    par = yacc.yacc()
    return par.parse(source)

if __name__ == "__main__":
    parser = yacc.yacc()
    while True:
        try:
            s = raw_input('calc > ')
        except EOFError:
            break;
        if not s: continue
        result = par.parse(s)
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
