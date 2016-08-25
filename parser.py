import sys
import yacc
from tokenizer import tokens

precedence = (
         ('left', 'OR'),
         ('left', 'AND'),
         ('left', 'EQUALS'),
         ('left', 'GT', 'GE', 'LT', 'LE'),
         ('left', 'PLUS', 'MINUS'),
         ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    	 ('right', 'UMINUS')
     )

def p_program(p):
    """program : translation_unit"""
    p[0] = p[1]

def p_translation_unit(p):
    """translation_unit :	statement
    			|	translation_unit statement
    """
    if len(p) == 3:
        p[1]['children'].append(p[2])
        p[0] = p[1]
    else:
        p[0] = {'type': 'translation_unit', 'children': [p[1]]}


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
		 |	for_statement
    """
    p[0] = p[1]

#-------------
# Assignments
#-------------


def p_assignment(p):
    'assignment : identifier EQUALS expression'
    p[0] = {'type': 'assignment', 'var_type': None, 'children': [p[1], p[3]], 'lineno': p.lineno(2)}

#for now its not possible to just declare without assignment
def p_decl_assignment(p):
    """assignment : type_info identifier EQUALS expression
		  | CONST type_info identifier EQUALS value
    """
    if len(p) == 5:
        p[0] = {'type':'assignment', 'var_type': p[1], 'constant': False, 'children': [p[2], p[4]], 'lineno': p.lineno(2)}
    else:
        p[0] = {'type':'assignment', 'var_type': p[2], 'constant': True, 'children': [p[3], p[5]], 'lineno': p.lineno(1)}

def p_assignment_increment(p):
    'assignment : ID PLUSPLUS'
    p[0] = {'type': 'plus_plus', 'children': [p[1]], 'lineno': p.lineno(1)}

def p_assignment_decrement(p):
    'assignment : ID MINUSMINUS'
    p[0] = {'type': 'minus_minus', 'children': [p[1]], 'lineno': p.lineno(1)}

#------------
# Functions
#------------

def p_func_call(p):
    """func_call : 	CALL identifier LPAREN arguments_list RPAREN
    		 |	CALL identifier LPAREN RPAREN"""
    if len(p) == 6:
        p[0] = {'type': 'func_call', 'children': [p[2], p[4]]}
    else:
        p[0] = {'type': 'func_call', 'children': [p[2]]}
    p[0]['lineno'] = p.lineno(1)

#nested function declarations are not allowed, unlike gcc an error will be thrown,
#this is done during semantic analysis
def p_func_declaration(p):
    """func_declaration : 	FUNCTION identifier LPAREN params_list RPAREN COLON RETURNS return_type LBRACKET translation_unit RBRACKET
    			|	FUNCTION identifier LPAREN RPAREN COLON RETURNS return_type LBRACKET translation_unit RBRACKET
    """
    if len(p) == 12:
        p[0] = {'type': 'func_declaration', 'parameters':p[4], 'func_type':p[8], 'children': [p[2], p[10]]}
    else:
        p[0] = {'type': 'func_declaration', 'parameters': None, 'func_type': p[7], 'children': [p[2], p[9]]}
    p[0]['lineno'] = p.lineno(1)

def p_return_type(p):
    """return_type 	: type_info
			| VOID"""
    p[0] = p[1]

def p_return_statement(p):
    'return_statement : RETURN expression'
    p[0] = {'type': 'return', 'children': [p[2]], 'lineno': p.lineno(2)}


#---------------------
# Language constructs
#----------------------

#need to check if the binary op returns a boolean
def p_if_statement(p):
    'if_statement : IF binary_op LBRACKET translation_unit RBRACKET'
    p[0] = {'type': 'if_statement', 'children': [p[2], p[4]], 'lineno': p.lineno(1)}

# def p_if_else_statement(p):
#     'if_statement : IF binary_op LBRACKET translation_unit RBRACKET ELSE LBRACKET translation_unit RBRACKET'
#     p[0] = {'type': 'if_statement', 'else_block': p[8], 'children': [p[2], p[4]]}

def p_else_statement(p):
    'else_statement : ELSE LBRACKET translation_unit RBRACKET'
    p[0] = {'type': 'else_statement', 'children': [p[3]], 'lineno': p.lineno(1)}
def p_while_statement(p):
    'while_statement : WHILE binary_op LBRACKET translation_unit RBRACKET'
    p[0] = {'type': 'while_statement', 'children': [p[2], p[4]], 'lineno': p.lineno(1)}

def p_for_statement(p):
    """for_statement :	FOR ID IN ID
    		     |	FOR ID IN func_call
    """
    p[0] = {'type': 'for_statement', 'children': [p[2], p[4]], 'lineno': p.lineno(1)}


#-----------
# Lists
#-----------

def p_params_list(p):
    """params_list :	parameter_declaration
	           |	params_list COMMA parameter_declaration
    """
    if len(p) == 2:
        p[0] = {'type': 'params_list', 'children': [p[1]]}
    else:
        p[1]['children'].append(p[3])
        p[0] = p[1]

def p_parameter_declaration(p):
    'parameter_declaration : type_info identifier'
    p[0] = {'type': 'param_decl', 'children': [p[1], p[2]]}

def p_arguments_list(p):
    """arguments_list : 	expression
		      |		arguments_list COMMA expression"""
    if len(p) == 2:
        p[0] = {'type': 'arg_list', 'children': [p[1]]}
    else:
        p[1]['children'].append(p[3])
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
    	    |	value
    """
    p[0] = p[1]

def p_identifier(p):
    'identifier : ID'
    p[0] = {'type': 'ID', 'children': [p[1]], 'lineno': p.lineno(1)}

def p_value(p):
    """value 	:	NUMBER
		|	SLITERAL
    		|	FLOATNUMBER
		|	TRUE
		|	FALSE
    """
    p[0] = p[1]
    
## Boolean expressions
def p_binary_op_and(p):
    'binary_op : expression AND expression'
    p[0] = {'type': 'and', 'children': [p[1], p[3]], 'lineno': p.lineno(2)}

def p_binary_op_or(p):
    'binary_op : expression OR expression'
    p[0] = {'type': 'or', 'children': [p[1], p[3]], 'lineno': p.lineno(2)}

def p_binary_op_gt(p):
    'binary_op : expression GT expression'
    p[0] = {'type': '>', 'children': [p[1], p[3]], 'lineno': p.lineno(2)}

def p_binary_op_lt(p):
    'binary_op : expression LT expression'
    p[0] = {'type': '<', 'children': [p[1], p[3]], 'lineno': p.lineno(2)}

def p_binary_op_ge(p):
    'binary_op : expression GE expression'
    p[0] = {'type': '>=', 'children': [p[1], p[3]], 'lineno': p.lineno(2)}

def p_binary_op_le(p):
    'binary_op : expression LE expression'
    p[0] = {'type': '<=', 'children': [p[1], p[3]], 'lineno': p.lineno(2)}

def p_binary_op_equals(p):
    'binary_op : expression ISEQUALS expression'
    p[0] = {'type': 'isequals', 'children': [p[1], p[3]], 'lineno': p.lineno(2)}
    
## Numeric expressions

def p_binary_op_mod(p):
    'binary_op : expression MODULO expression'
    p[0] = {'type': 'modulo', 'children': [p[1], p[3]], 'lineno': p.lineno(2)}

def p_binary_op_plus(p):
    'binary_op : expression PLUS expression'
    p[0] = {'type': '+', 'children': [p[1], p[3]], 'lineno': p.lineno(2)}

def p_binary_op_minus(p):
    'binary_op : expression MINUS expression'
    p[0] = {'type': '-', 'children': [p[1], p[3]], 'lineno': p.lineno(2)}

def p_binary_op_times(p):
    'binary_op : expression TIMES expression'
    p[0] = {'type': '*', 'children': [p[1], p[3]], 'lineno': p.lineno(2)}

def p_binary_op_divide(p):
    'binary_op : expression DIVIDE expression'
    p[0] = {'type': '/', 'children': [p[1], p[3]], 'lineno': p.lineno(2)}

######

def p_unary_op_minus(p):
    'unary_op : MINUS expression %prec UMINUS'
    p[0] = {'type': 'uminus', 'children': [p[2]], 'lineno': p.lineno(1)}

# def p_unary_op_plus(p):
#     'unary_op : PLUS expression'
#     p[0] = ast.UnaryOp(p[1], [p[2]])

def p_unary_op_not(p):
    'unary_op : NOT expression'
    p[0] = {'type': 'not', 'children': [p[2]], 'lineno': p.lineno(1)}

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
    print "A Syntax error has been found: {0}".format(p)
    sys.exit(1)

def parse(source):
    par = yacc.yacc()
    return par.parse(source)

if __name__ == "__main__":
    parser = yacc.yacc()
    while True:
        try:
            s = raw_input('calc > ')
        except EOFError:
            break
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
