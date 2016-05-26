import yacc
from tokenizer import tokens
from ast import *

precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQ'),
        ('left', 'GT', 'GE', 'LT', 'LE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MOD')
    )

def p_expression(p): #not sure here about 2nd rule
    '''expression 	: assignment_expression
			| expression COMMA assignment_expression
    '''

def p_assignment_expression(p):
    '''assignment_expression : binary_expression'''

def

def p_binary_expression(p):
    ''' 
    binary_expression	: unary_expression
    			| binary_expression PLUS binary_expression
    			| binary_expression MINUS binary_expression
			| binary_expression TIMES binary_expression
    			| binary_expression DIVIDE binary_expression
    			| binary_expression MODULO binary_expression
    			| binary_expression LT binary_expression
    			| binary_expression LE binary_expression
    			| binary_expression GT binary_expression
    			| binary_expression GE binary_expression
    			| binary_expression IS binary_expression
    			| binary_expression ISEQUALS binary_expression
    			| binary_expression OR binary_expression
    			| binary_expression AND binary_expression
    '''
    p[0] = ast.BinaryOp(p[2], p[1], p[3])

def p_unary_expression_1(p):
    '''unary_expression	: primary_expression'''
    p[0] = p[1]

def p_unary_expression_2(p):
    '''unary_expression : PLUSPLUS unary_expression
    			| MINUSMINUS unary_expression
			| unary_operator primary_expression
    '''
    p[0] = UnaryOp(p[1], p[2])

def p_unary_operator(p):
    '''unary_operator 	: MINUS
    			| NOT
    '''
    p[0] = p[1]

def primary_expression_1(p):
    '''primary_expression : ID'''
    p[0] = p[1]

def p_primary_expression_2(p):
    '''primary_expression : constant'''
    p[0] = p[1]

def p_primary_expression_3(p):
    '''primary_expression : SLITERAL'''
    p[0] = p[1]

def p_primary_expression_4(p):
    '''primary_expression : LPAREN expression RPAREN'''
    p[0] = p[2]


##########################
def p_expression_plus(p):
    'expression : expression PLUS term'
    print len(p)
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
    print len(p)
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

