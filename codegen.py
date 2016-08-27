import analyzer
import symbol_table

table = symbol_table.SymbolTable()


rodata = "SECTION .rodata" + '\n'

data = "SECTION .data" + '\n'
bss = "SECTION .bss" + '\n'

text = dict()
text['functions'] = '\n' + "SECTION .text" + '\n'
text['functions'] += "EXTERN print_number, print_text" + '\n'
text['code'] = "global _start" + '\n'
text['code'] += "_start:" + '\n'

rodata_index = 0
data_index = 0
label_index = 0

builtin_functions = ['print']

def generate(node):
    initialize_code()
    generate_text(node, 'code')
    terminate_code()
    return rodata + data + bss + text['functions'] + text['code']

def initialize_code():
    text['code'] += '\t' + "mov ebp, esp" + '\n'

def terminate_code():
    text['code'] += '\t' + "mov eax,  1" + '\n'
    text['code'] += '\t' + "mov ebx,  0" + '\n'
    text['code'] += '\t' + "int 0x80" + '\n'

def generate_text(node, place):
    if node['type'] == 'translation_unit':		generate_translation_unit(node, place)
    elif node['type'] == 'assignment':			generate_assignment(node, place)
    elif node['type'] == 'func_call':       	generate_func_call(node, place)
    elif node['type'] == 'func_declaration':	generate_function_declaration(node)
    elif node['type'] == 'return':              generate_return_statement(node)
    elif node['type'] == 'if_statement' or node['type'] == 'if_else_statement':
        generate_if_statement(node, place)


def generate_translation_unit(node, place):
    for child in node['children']:
        generate_text(child, place)

def generate_assignment(node, place):
    generate_expression(node['children'][1], place)
    text[place] += '\t' + "sub esp,  4" + '\n'
    variables = 0
    if node['var_type']:
        #declaration + assignment
        for symbol in table.scopes[len(table.scopes) - 1]: #the innermost scope
            if symbol.kind == 'var': #parameters and functions never change offset
                variables += 1
        table.add_symbol(symbol_table.Symbol(node['children'][0]['children'][0], node['var_type'],
                                                 offset = 4 * variables + 4))
        text[place] += '\t' + "mov [ebp-" + str(variables * 4 + 4) + "], eax" + '\n'
    else:
        #just reassignment of existing variable
        id = table.find_symbol(node['children'][0]['children'][0])
        text[place] += '\t' + "mov [ebp-" + str(id.offset) + "], eax" + '\n'

#functions can only be declared in the functions section
def generate_function_declaration(node):
    id = node['children'][0]['children'][0]
    text['functions'] += id + ':' + '\n'
    #first of all create the stack frame
    text['functions'] += '\t' + "push ebp" + '\n'
    text['functions'] += '\t' + "mov ebp,  esp" + '\n'
    #function assumes parameters are available since these will be pushed by the function call
    parameters = node['parameters']['children']
    if node['parameters']:
        table.add_symbol(symbol_table.Symbol(id, node['func_type'], 'function', False, parameters))
    else:
        table.add_symbol(symbol_table.Symbol(id, node['func_type'], 'function', False))
    table.enter_scope()
    i = 0
    for param in parameters:
        #offset is calculated as the (number of parameters - i) * 4 + 4
        #first four is due to the size in bytes, second four is due to the return address being on the way
        table.add_symbol(symbol_table.Symbol(param['children'][1]['children'][0], param['children'][0],
                                             'parameter', False, offset = (len(parameters)-i) * 4 + 4))
        i += 1
    generate_text(node['children'][1], 'functions')
    #if function is void the stack frame must be destroyed here, otherwise it's
    #done by the return statement(s)
    if node['func_type'] == "void":
        delete_ar()
    table.exit_scope()
    text['functions'] += '\n'

def generate_func_call(node, place):
    id = node['children'][0]['children'][0]
    #first check if the call is to a built in function
    for function in builtin_functions:
        if id == function:
            calling_builtin = "generate_call_to_" + id
            globals()[calling_builtin](node, place)
            return
    #we're calling a self defined function, start the function prologue
    function = table.find_symbol(id)
    if function.params:
        #push parameters in the stack
        found_params = node['children'][1]['children']
        for param in found_params:
            generate_expression(param, place)
            text[place] += '\t' + "push eax" + '\n'
    text[place] += '\t' + "call " + function.name + '\n'
    if function.params:
        text[place] += '\t' + "add esp,  " + str(len(function.params) * 4) + '\n'

#return statements can also only exist within a function
def generate_return_statement(node):
    #return values are passed on eax
    generate_expression(node['children'][0], 'functions')
    delete_ar()

def generate_if_statement(node, place):
    global label_index
    else_block = None
    if node['type'] == 'if_else_statement':
        expression = node['children'][0]['children'][0]
        if_block = node['children'][0]['children'][1]
        else_block = node['children'][1]['children'][0]
    else:
        expression = node['children'][0]
        if_block = node['children'][1]
    generate_expression(expression, place)
    text[place] += '\t' + "cmp eax,  0" + '\n'
    text[place] += '\t' + "je .L" + str(label_index) + '\n'
    generate_text(if_block, place)
    if else_block:
        text[place] += '\t' + "jmp .L" + str(label_index + 1) + '\n'
    text[place] += ".L" + str(label_index) + ':' + '\n'
    if else_block:
        generate_text(else_block, place)
        text[place] += ".L" + str(label_index + 1) + ':' + '\n'
    label_index += 2 if else_block else 1

def generate_call_to_print(node, place):
    arg_list = node['children'][1]['children'] #array of expressions
    for argument in arg_list:
        param_type = analyzer.type_check(argument)
        generate_expression(argument, place)
        #now the item to print is in register eax
        text[place] += '\t' + "push eax" + '\n' #pass the parameter to the print function onto the stack
        if param_type == 'integer':
            text[place] += '\t' + "call print_number" + '\n'
            text[place] += '\t' + "add esp,  4" + '\n'
        elif param_type == 'string': #if it's a string, evaluating the expression will put its length in ebx
            text[place] += '\t' + "push ebx" + '\n'
            text[place] += '\t' + "call print_text" + '\n'
            text[place] += '\t' + "add esp,  8" + '\n'

# TODO generate all other expressions
#Expression is evaluated and its value is put in the accumulator (eax)
def generate_expression(node, place):
    global rodata, rodata_index
    if not isinstance(node, dict): #if node is not a dictionary then it's an explicit value
        if isinstance(node, bool): #text for bool first since its a subclass of int
            if node: #True
                text[place] += '\t' + "mov eax,  1" + '\n'
            else: #False
                text[place] += '\t' + "mov eax,  0" + '\n'
        elif isinstance(node, int):
                text[place] += '\t' + "mov eax,  " + str(node) + '\n'
        elif isinstance(node, str):
            rodata += "Label" + str(rodata_index) + ": db " + '"' + str(node)+ '",10' + '\n'
            #this might not be necessary since we can get the info using len(str)
            text[place] += '\t' + "mov eax,  " + "Label" + str(rodata_index) + '\n'
            text[place] += '\t' + "mov ebx,  " + str(len(node) + 1) + '\n'
            rodata_index += 1
    elif node['type'] == 'ID':
        id = table.find_symbol(node['children'][0])
        if id.kind == 'parameter':
            #parameters always have a positive offset
            text[place] += '\t' + "mov eax,  DWORD [ebp+" + str(id.offset) +']' + '\n'
        else:
            text[place] += '\t' + "mov eax,  DWORD [ebp-" + str(id.offset) +']' + '\n'

    elif node['type'] == "func_call":
        generate_func_call(node, place)
    elif node['type'] == "modulo": #max dividend 2^(32-1)
        generate_expression(node['children'][0], place)
        text[place] += '\t' + "push eax" + '\n'
        generate_expression(node['children'][1], place)
        text[place] += '\t' + "mov ecx,  eax" + '\n'
        text[place] += '\t' + "pop eax" + '\n'
        text[place] += '\t' + "mov edx,  0" + '\n' #make sure edx is cleared as it can mess the division up
        text[place] += '\t' + "div ecx" + '\n'
        text[place] += '\t' + "mov eax,  edx" +'\n' #remainder is in edx but we return values in eax
    elif node['type'] == '+' or node['type'] == '-':
        generate_expression(node['children'][0], place)
        text[place] += '\t' + "push eax" + '\n'
        generate_expression(node['children'][1], place)
        text[place] += '\t' + "pop ebx" + '\n'
        if node['type'] == '+':
            #there's no overflow flag checking
            text[place] += '\t' + "add eax, ebx" + '\n'
        else:
            text[place] += '\t' + "sub eax,  ebx" + '\n'
    elif node['type'] == '*' or node['type'] == '/':
        generate_expression(node['children'][0], place)
        text[place] += '\t' + "push eax" +'\n'
        generate_expression(node['children'][1], place)
        text[place] += '\t' + "pop ebx" + '\n'
        if node['type'] == '*':
            #again no overflow checking is done for now, the value in edx is ignored
            text[place] += '\t' + "mul ebx" + '\n'
        else:
            text[place] += '\t' + "div ebx" + '\n'
    elif node['type'] == "not":
        generate_expression(node['children'][0], place)
        text[place] += '\t' + "xor ax,  1" + '\n'
    elif node['type'] == "and":
        generate_expression(node['children'][0], place)
        text[place] += '\t' + "push eax" + '\n'
        generate_expression(node['children'][1], place)
        text[place] += '\t' + "pop ebx" + '\n'
        text[place] += '\t' + "and eax,  ebx" + '\n'
    elif node['type'] == "or":
        generate_expression(node['children'][0], place)
        text[place] += '\t' + "push eax" + '\n'
        generate_expression(node['children'][1], place)
        text[place] += '\t' + "pop ebx" + '\n'
        text[place] += '\t' + "or eax,  ebx" + '\n'
    elif node['type'] == '>' or node['type'] == '<' or node['type'] == '>='\
            or node['type'] == '<=' or node['type'] == '==' or node['type'] == '!=':
        generate_expression(node['children'][0], place)
        text[place] += '\t' + "push eax" + '\n'
        generate_expression(node['children'][1], place)
        text[place] += '\t' + "pop ebx" + '\n'
        text[place] += '\t' + "cmp eax,  ebx" +'\n'
        if node['type'] == '>':
            text[place] += '\t' + "setg bl" +'\n'
        elif node['type'] == '<':
            text[place] += '\t' + "setl bl" +'\n'
        elif node['type'] == '>=':
            text[place] += '\t' + "setge bl" +'\n'
        elif node['type'] == '<=':
            text[place] += '\t' + "setle bl" + '\n'
        elif node['type'] == '!=':
            text[place] += '\t' + "setne bl" + '\n'
        elif node['type'] == '==':
            text[place] += '\t' + "sete bl" + '\n'
        text[place] += '\t' + "movsx eax,  bl" + '\n'


def delete_ar():
    text['functions'] += '\t' + "mov esp,  ebp" + '\n'
    text['functions'] += '\t' + "pop ebp" + '\n'
    text['functions'] += '\t' + "ret" + '\n'