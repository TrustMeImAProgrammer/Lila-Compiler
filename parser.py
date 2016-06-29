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
    """program: statements"""
    p[0] = p[1]

def p_statement(p):
    """statement :	assignment
		 |	func_call
    		 |	if_statement
		 |	for_statement
		 |	while_statement
		 | 	return_statement
    """
    p[0] = p[1]

def assignment(p):
    'assignment : ID EQUALS expression'
    p[0] = ast.Assignment()
def p_assignment_int(p):
    """declaration :	INTEGER ID EQUALS NUMBER
    		   |	INTEGER multiplication
		   |	INTEGER addition
    """
    p[0] = ast.Assignment()




#rule for expressions, which also count as statemets
def p_statement_expression(p):
    """statement_expression :	simple_expression
		    	    |	func_call
    			    |	atom
    """
    p[0] = p[1]

def p_simple_expression(p):
    """simple_expression :	binary_op
    			 |	unary_op
    			 |	preincrement_expression
   			 |	predecrement_expression
    """
    p[0] = p[1]

## Function calls
def p_func_call(p):
    """func_call 	: CALL identifier LPAREN arguments_list RPAREN
    			| CALL identifier LPAREN RPAREN"""
    p[0] = ast.FuncCall(p[2], p[4] if len(p) == 6 else None)

def p_arguments_list(p):
    """arguments_list : 	atom
		      |		arguments_list COMMA atom"""

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

## Increments

def p_preincrement_expression(p):
    'preincrement_expression : PLUS PLUS statement_expression'
    p[0] = ast.PreIncrExpression([p[1], p[2]], p[3])

def p_predecrement_expression(p):
    'predecrement_expression : MINUS MINUS statement_expression'
    p[0] = ast.PreDecrExpression([p[1], p[2]], p[3])
    
##########################
def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]

def p_term_divide(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

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
