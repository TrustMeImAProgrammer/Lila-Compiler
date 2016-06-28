import lex

reserved = {
    'if' : 'IF',
    'while' : 'WHILE',
    'do' : 'DO',
#    'is' : 'IS',
    'equals' : 'ISEQUALS',
    'call' : 'CALL',
    'and' : 'AND',
    'or' : 'OR',
    'not' : 'NOT',
    'mod' : 'MODULO',
    'integer' : 'INT',
    'string' : 'STRING',
    'real' : 'REAL',
    'boolean' : 'BOOLEAN',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'character' : 'CHAR'
}
tokens = ["SLITERAL", "LPAREN", "RPAREN", "LBRACKET", "RBRACKET",
          "PLUS", "MINUS", "GT", "GE", "LT", "LE", "TIMES", "DIVIDE", 
          "EQUALS", "TIMESEQUALS", "DIVEQUALS", "PLUSEQUALS", "MINUSEQUALS",
          "PLUSPLUS", "MINUSMINUS", "COMMENT", 'COMMA', 'ID', 'NUMBER'] + list(reserved.values())

#
#	All tokens defined by functions are added in the same order as they appear in the lexer file.
#	Tokens defined by strings are added next by sorting them in order of decreasing regular expression
#	length (longer expressions are added first).
#

t_SLITERAL = r"'([^']|'')*'" #Lila uses single quotes for strings and characters, two single quotes can be used when it's necessary to represent one inside the string
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACKET = r"\{"
t_RBRACKET = r"\}"
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_EQUALS = r"="
t_GT = r">"
t_GE = r">="
t_LT = r"<"
t_LE = r"<="
t_TIMESEQUALS = r"\*="
t_DIVEQUALS = r"/="
t_PLUSEQUALS = r"\+="
t_MINUSEQUALS = r"-="
t_COMMA = r","
t_MODULO = r"%"
t_CHARLITERAL = r"'.'"


def t_NUMBER(t):
    r"\d+"
    t.value = int(t.value)
    return t

def t_FLOAT(t):
    r"[\d]*\.[\d]*"
    t.value = float(t.value)
    return t

#rule to track line numbers
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r"\/\/.*"
    pass

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID') # Check for reserved words
    return t

#ignored characters
t_ignore = " \t"

#error handling rule
def t_error(t):
    print("Illegal character '%s" % t.value[0])
    t.lexer.skip(1)

#build the lexer
lexer = lex.lex()

# Give the lexer some input
if __name__ == "__main__":
    data = raw_input()
    lexer.input(data)
    for tok in lexer:
        print(tok)
