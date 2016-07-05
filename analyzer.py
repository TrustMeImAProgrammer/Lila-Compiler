import symbol_table
import sys

symboltable = SymbolTable()
    

def analyze(node):
    if node['type'] == 'assignment':	return analyze_assignment(node)
    


def analyze_assignment(node):
    id = node['children'][0]
    expression = node['children'][1]
    if(node['var_type']): 
        #this is a declaration and assignment
        #check if variable has been defined already in the current scope, lila is statically scoped and
        #does variable shadowing
        if check_scope(id):
            print "Error at line {0}: variable {1} already defined".format(node['lineno'], id)
            sys.exit()
        #check type of expression
        type = type_check(expression)
        if type == node['var_type']:
            #Add symbol to symbol table
            symboltable.add_symbol(Symbol(id, node['type'], 'var', True if node['constant'] else False))
        else:
            print "Error at line {0}: variable type and expression type don't coincide"
            sys.exit()
    else:
        #this is a simple reassignment of an existing variable
        #check if the variable has been declared
        symbol = find_symbol(id)
        if not symbol:
            print "Error at line {0}: variable {1} does not exist".format(node['lineno'], id)
            sys.exit()
        #get type of expression being assigned
        type = type_check(expression)
        if not type == symbol.type:
            print "Error at line {0}: cannot assigned expression of type {1} to variable of type {2}".format(node['lineno'], type, symbol.type)
            sys.exit()

#an expression can be either a binary op, unary op, 
#func call, identifier or literal value
def type_check(node):
    if not isinstance(node, dict): #if node is not a dictionary then it's an explicit value
        return convert_types(type(node).__name__)
    if node['type'] == 'ID' or node['type'] == 'func_call':
        type = symboltable.find_symbol(node['name'])
        if type:
            return type
        else:
            obj = 'variable' if node['type'] == 'ID' else 'function'
            print "Error at line {0}: use of undefined {1} {2}".format(node['lineno'], obj, node['name'])
            sys.exit()
    if node['type'] == 'uminus':
        type = type_check(node['children'][0])
        if type == 'integer' or type == 'real':
            return type
        print "Error at line {0}: invalid operand type, expected integer or float, got {1}".format(node['lineno'], type)
        sys.exit()
    if node['type'] == 'not':
        type = type_check(node['children'][0])
        if type == 'boolean':
            return type
        print "Error at line {0}: invalid operand type, expected boolean, got {1}".format(node['lineno'], type)
        sys.exit()
    #type checking is done using a post-order tree traversal
    if (node['type'] == 'and' or node['type'] == 'or' or node['type'] == '>' or 
        node['type'] == '<' or node['type'] == '>=' or node['type'] == '<=' or node['type'] == 'isequals'):
        ltype = type_check(node['children'][0])
        if not ltype == 'boolean':
            print "Error at line {0}: invalid left operand type, expected boolean, got {1}".format(node['lineno'], ltype)
            sys.exit()
        rtype = type_check(node['children'][1])
        if not rtype == 'boolean':
            print "Error at line {0}: invalid right operand type, expected boolean, got {1}".format(node['lineno'], rtype)
            sys.exit()
        return 'boolean'
    if node['type'] == 'modulo':
        ltype = type_check(node['children'][0])
        if not ltype == 'integer':
            print "Error at line {0}: invalid left operand type, expected integer, got {1}".format(node['lineno'], ltype)
            sys.exit()
        rtype = type_check(node['children'][1])
        if not rtype == 'integer':
            print "Error at line {0}: invalid right operand type, expected integer, got {1}".format(node['lineno'], rtype)
            sys.exit()
        return 'integer'
    if (node['type'] == '+' or node['type'] == '-' or node['type'] == '*' or
        node['type'] == '/'):
        ltype = type_check(node['children'][0])
        if not ltype == 'integer' or not ltype == 'real':
            print "Error at line {0}: invalid left operand type, expected integer or real, got {1}".format(node['lineno'], ltype)
            sys.exit()
        rtype = type_check(node['children'][1])
        if not rtype == 'integer' or not rtype == 'real':
            print "Error at line {0}: invalid right operand type, expected integer or real, got {1}".format(node['lineno'], rtype)
            sys.exit()
        #type inference for numeric expressions:
        return 'integer' if ltype == 'integer' and rtype == 'integer' else 'real'
    print "Error: unknown type" #This error should never happen
    sys.exit()

def convert_types(type):
    switcher = {
        'int' : 'integer',
        'float' : 'real',
        'str' : 'string',
        'bool' : 'boolean'
    }
    return switcher.get(type)
