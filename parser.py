import yacc
from tokenizer import tokens
import ast

precedence = (
         ('left', 'OR'),
         ('left', 'AND'),
         ('left', 'EQ'),
         ('left', 'GT', 'GE', 'LT', 'LE'),
         ('left', 'PLUS', 'MINUS'),
         ('left', 'TIMES', 'DIVIDE', 'MOD')
     )


def statement_expression(p):
    """statement : 	simple_expression
    		 |	func_call
    		 |	atom
    """
    p[0] = p[1]

def simple_expression(p):
    """simple_expression :	binary_op
    			 |	unary_op
    			 |	preincrement_expression
   			 |	postincrement_expression
			 | 	simple_expression
    """
    p[0] = p[1]

## Function calls
def func_call(p):
    """func_call 	: CALL identifier LPARENT arguments_list RPAREN
    			| CALL identifier LPAREN RPAREN"""
    p[0] = ast.FuncCall(p[2], p[4] if len(p) == 6 else None)

 ## Atomic expressions
def atom_expression_1(p):
    """atom :	identifier
    	    |	constant
    """
    p[0] = p[1]

def conastant(p):
    """constant :	NUMBER
		|	SLITERAL
    		|	FLOAT
    """
    p[0] = p[1]
    
## Boolean expressions
def binary_op_and(p):
    'binary_op : statement_expression AND statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def binary_op_or(p):
    'binary_op: statement_expression OR statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def binary_op_gt(p):
    'binary_op : statement_expression GT statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def binary_op_lt(p):
    'binary_op : statement_expression LT statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def binary_op_ge(p):
    'binary_op : statement_expression GE statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def binary_op_le(p):
    'binary_op : statement_expression LE statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def binary_op_equals(p):
    'binary_op : statement_expression ISEQUALS statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])
    
## Numeric expressions

def binary_op_mod(p):
    'binary_op : statement_expression MODULO statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def binary_op_plus(p):
    'binary_op : statement_expression PLUS statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def binary_op_minus(p):
    'binary_op : statement_expression MINUS statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

def binary_op_times(p):
    'binary_op : statement_expression TIMES statement_expression'
    p[0] = ast.BinaryOp(p[2], [p[1], p[3]])

######

def unary_op_minus(p):
    'unary_op : MINUS '
    
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
    print(p[0][1])
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
        print("length of s : %s" % len(s))
    except EOFError:
        break;
    if not s: continue
    result = parser.parse(s)
    print(result)

