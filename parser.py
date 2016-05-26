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

