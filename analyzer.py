import symbol_table
import sys

symboltable = symbol_table.SymbolTable()
# add built-in names and functions to the symbol table
# -1 is used by the print function to accept a variable number of arguments
symboltable.add_symbol(symbol_table.Symbol('print', None, 'function', False, -1))
symboltable.add_symbol((symbol_table.Symbol('str', 'string', 'function', False, 1)))

def analyze(node):
    print "got node of type: {0}".format(node['type'])
    if node['type'] == 'translation_unit': 	return analyze_translation_unit(node)
    if node['type'] == 'assignment':		return analyze_assignment(node)
    if node['type'] == 'plus_plus': 		return analyze_shorthand_assignment(node)
    if node['type'] == 'minus_minus': 		return analyze_shorthand_assignment(node)
    if node['type'] == 'func_call':	     	return analyze_func_call(node)
    if node['type'] == 'func_declaration':	return analyze_function_declaration(node)
    if node['type'] == 'if_statement':		return analyze_if_statement(node)
    if node['type'] == 'if_else_statement': return analyze_if_else_statement(node)
    if node['type'] == 'while_statement':   return analyze_while_statement(node)
    #if node['type'] == 'return':            return analyze_return_statement(node)

def analyze_translation_unit(node):
    for child in node['children']:
        analyze(child)

def analyze_assignment(node):
    id = node['children'][0]['children'][0]
    print "expression id = {0} at line {1}".format(id, node['lineno'])
    expression = node['children'][1]
    if node['var_type']:
        #this is a declaration and assignment
        #check if variable has been defined already in the current scope, lila is statically scoped and
        #does variable shadowing
        if symboltable.check_scope(id):
            print "Error at line {0}: variable {1} already defined".format(node['lineno'], id)
            sys.exit(1)
        #check type of expression
        expr_type = type_check(expression)
        print "got type {0}".format(expr_type)
        if expr_type == node['var_type']:
            #Add symbol to symbol table
            symboltable.add_symbol(symbol_table.Symbol(id, node['var_type'], 'var', True if node['constant'] else False))
        else:
            print "Error at line {0}: variable type and expression type don't coincide".format(node['lineno'])
            sys.exit(1)
        #if the value to assign is a function call, check that its a legal call
        try:
            if expression['type'] == 'func_call':
                analyze_func_call(expression)
        except TypeError:
            #value being assigned is an explicit value
            pass
    else:
        #this is a simple reassignment of an existing variable
        #check if the variable has been declared
        symbol = symboltable.find_symbol(id)
        if not symbol:
            print "Error at line {0}: variable {1} does not exist".format(node['lineno'], id)
            sys.exit(1)
        #get type of expression being assigned
        expr_type = type_check(expression)
        if not expr_type == symbol.type:
            print "Error at line {0}: cannot assigned expression of type {1} to variable of type {2}".format(node['lineno'], type, symbol.type)
            sys.exit(1)

def analyze_shorthand_assignment(node):
    #first check if the variable being modified has been defined
    id = node['children'][0]
    symbol = symboltable.find_symbol(id)
    if not symbol:
        print "Error at line {0}: use of undefined variable {1}".format(node['lineno'], id)
        sys.exit(1)
    #now check if the variable is an lvalue
    if symbol.kind == 'function':
        print "Error at line {0}: cannot perform assignment to {1}, lvalue required".format(node['lineno'], id)
        sys.exit(1)
    #next, check if the variable is a constant
    if symbol.is_constant:
        print "Error at line {0}: cannot modify value of {1}, because it's a constan".format(node['lineno'], id)
        sys.exit(1)
    #now check if plusplus or minus_minusis a valid operation on this type of variable
    print symbol.type
    if symbol.type != 'integer' and symbol.type != 'real':
        print "Error at line {0}: cannot petform operation on variable of type {1}".format(node['lineno'], symbol.type)
        sys.exit(1)    

def analyze_func_call(node):
    #check that the function has been declared
    id = node['children'][0]['children'][0]
    print "func call id = {0}".format(id)
    symbol = symboltable.find_symbol(id)
    if not symbol:
        print "Error at line {0}: undefined function {1}".format(node['lineno'], id)
        sys.exit(1)
    if symbol.params:
        #check the parameters coincide with the func declaration
        if len(node['children']) < 2:
            print "Error at line {0}: function {1} requires {2} parameters, found 0".format(node['lineno'], id, len(symbol.params))
            sys.exit(1)
        found_params = node['children'][1]['children']
        required_params = symbol.params
        if required_params == -1: return #function accepts an arbitrary number of parameters of arbitrary type
        if len(found_params) != len(required_params):
            print "Error at line {0}: function {1} requires {2} parameters, found {3}".format(node['lineno'], id, len(required_params), len(found_params))
            sys.exit(1)
        for i, param in enumerate(found_params):
            if convert_types(type(param).__name__) != required_params[i]['children'][0]:
                print "Error at line {0}: parameter number {1} must be of type {2}, found {3}".format(node['lineno'], i + 1, required_params[i]['children'][0], convert_types(type(param).__name__))
                sys.exit(1)

def analyze_function_declaration(node):
    #check the function hasn't been declared already
    id = node['children'][0]['children'][0]
    print "func declaration id = {0}".format(id)
    if symboltable.check_scope(id):
        print "Error at line {0}: function {1} already defined".format(node['lineno'], id)
        sys.exit(1)
    #Add function to the symbol table now to allow for recursion
    if node['parameters']:
        symboltable.add_symbol(symbol_table.Symbol(id, node['func_type'], 'function', False, node['parameters']['children']))
    else:
        symboltable.add_symbol(symbol_table.Symbol(id, node['func_type'], 'function', False))
    #add parameters temporarily to the symbol table
    symboltable.enter_scope()
    for param in node['parameters']['children']:
        symboltable.add_symbol(symbol_table.Symbol(param['children'][1]['children'][0], param['children'][0], 'parameter', False))
    #analyze the function's body
    ret_type = 0
    for child in node['children'][1]['children']:
        if child['type'] == 'func_declaration':
            #found nested function declaration throw error
            print "Error at line {0}: Nested function declaration".format(child['lineno'])
            sys.exit(1)
        #look for return statements in the function
        if child['type'] == 'return':
            ret_type = type_check(child['children'][0])
            #if the return type doesn't match the function's type
            if ret_type != node['func_type']:
                print "Error at line {0}: wrong return type {1}".format(child['lineno'], ret_type)
                sys.exit(1)
        else:
            analyze(child)
    #if there are no return statements but the function isn't of void type
    if ret_type == 0 and node['func_type'] != 'void':
        print "Error at line {0}: Non-void function {1} without return statement".format(node['lineno'], id)
        sys.exit(1)
    #remove the parameters from the scope again
    symboltable.exit_scope()

# def analyze_return_statement(node):
#     #this return statement is not within a function
#     print "Error at line {0}: return statement outside a function".format(node['lineno'])
#     sys.exit(1)

def analyze_if_statement(node):
    condition = node['children'][0]
    #check that the condition is a boolean expression
    condition_type = type_check(condition)
    if condition_type != 'boolean':
        print "Error at line {0}: condition must be a boolean expression".format(node['lineno'])
        sys.exit(1)
    #now analyze the if block
    analyze_translation_unit(node['children'][1])

def analyze_if_else_statement(node):
    condition = node['children'][0]['children'][0]
    condition_type= type_check(condition)
    if condition_type != 'boolean':
        print "Error at line {0}: condition must be a boolean expression".format(node['lineno'])
        sys.exit(1)
    #analyze the if block
    analyze_translation_unit(node['children'][0]['children'][1])
    #and now the else block
    analyze_translation_unit(node['children'][1]['children'][0])

def analyze_while_statement(node):
    condition_type = type_check(node['children'][0])
    if condition_type != 'boolean':
        print "Error at line {0}: condition must be a boolean expression".format(node['lineno'])
        sys.exit(1)
    analyze_translation_unit(node['children'][1])

#an expression can be either a binary op, unary op, 
#func call, identifier or literal value
#type checking is done using a post-order tree traversal
def type_check(node):
    """This function returns an expression's type
    and also analyzes the expression"""
    global type
    if not isinstance(node, dict): #if node is not a dictionary then it's an explicit value

        return convert_types(type(node).__name__)
    if node['type'] == 'ID' or node['type'] == 'func_call':
        id = node['children'][0] if node['type'] == 'ID' else node['children'][0]['children'][0]
        print "looking up {0}".format(id)
        symbol = symboltable.find_symbol(id)
        if symbol:
            return symbol.type
        else:
            obj = 'variable' if node['type'] == 'ID' else 'function'
            print "Error at line {0}: use of undefined {1} {2}".format(node['lineno'], obj, id)
            sys.exit(1)
    if node['type'] == 'params_list':
        parameters = []
        for param in node['children']:
            parameters.append(param['children'][0])
        return parameters
    if node['type'] == 'uminus':
        found_type = type_check(node['children'][0])
        if found_type == 'integer' or type == 'real':
            return found_type
        print "Error at line {0}: invalid operand type, expected integer or float, got {1}".format(node['lineno'], type)
        sys.exit(1)
    if node['type'] == 'not':
        found_type = type_check(node['children'][0])
        if found_type == 'boolean':
            return found_type
        print "Error at line {0}: invalid operand type, expected boolean, got {1}".format(node['lineno'], type)
        sys.exit(1)
    #and and or operations are only defined for boolean types
    if node['type'] == 'and' or node['type'] == 'or':
        ltype = type_check(node['children'][0])
        if not ltype == 'boolean':
            print "Error at line {0}: invalid left operand type, expected boolean, got {1}".format(node['lineno'], ltype)
            sys.exit(1)
        rtype = type_check(node['children'][1])
        if not rtype == 'boolean':
            print "Error at line {0}: invalid right operand type, expected boolean, got {1}".format(node['lineno'], rtype)
            sys.exit(1)
        return 'boolean'
    #modulo operation only accepts integers
    if node['type'] == 'modulo':
        ltype = type_check(node['children'][0])
        if not ltype == 'integer':
            print "Error at line {0}: invalid left operand type, expected integer, got {1}".format(node['lineno'], ltype)
            sys.exit(1)
        rtype = type_check(node['children'][1])
        if not rtype == 'integer':
            print "Error at line {0}: invalid right operand type, expected integer, got {1}".format(node['lineno'], rtype)
            sys.exit(1)
        return 'integer'
    #these operations can be done on real or integer types
    if (node['type'] == '+' or node['type'] == '-' or node['type'] == '*' or node['type'] == '/' 
        or node['type'] == '<' or node['type'] == '>' or node['type'] == '>=' or node['type'] == '<='):
        ltype = type_check(node['children'][0])
        if ltype != 'integer' and ltype != 'real':
            print "Error at line {0}: invalid left operand type, expected integer or real, got {1}".format(node['lineno'], ltype)
            sys.exit(1)
        rtype = type_check(node['children'][1])
        if rtype != 'integer' and rtype != 'real':
            print "Error at line {0}: invalid right operand type, expected integer or real, got {1}".format(node['lineno'], rtype)
            sys.exit(1)
        #type inference for numeric expressions:
        if node['type'] == '+' or node['type'] == '-' or node['type'] == '*' or node['type'] == '/':
            return 'integer' if ltype == 'integer' and rtype == 'integer' else 'real'
        return 'boolean'
    #isequals and != accept any type
    if node['type'] == '==' or node['type'] == '!=':
        return 'boolean'
    print "Error: unknown type" #This error should never happen
    sys.exit(1)

def convert_types(type):
    switcher = {
        'int' : 'integer',
        'float' : 'real',
        'str' : 'string',
        'bool' : 'boolean'
    }
    return switcher.get(type)
