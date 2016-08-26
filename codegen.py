import analyzer
import symbol_table
table = analyzer.symboltable


rodata = "SECTION .rodata" + '\n'

data = "SECTION .data" + '\n'
data = data + 'True: db "True",10' + '\n'
data = data + 'TrueLen: equ $-True' + '\n'
data = data + 'False: db "False",10' + '\n'
data = data + 'FalseLen: equ $-False' + '\n'

bss = "SECTION .bss" + '\n'

text = "SECTION .text" + '\n'
text += "EXTERN print_number, print_text" + '\n'
text += "global _start" + '\n'
text += "_start:" + '\n'

rodata_index = 0
data_index = 0

builtin_functions = ['print']

def generate(node):
    initialize_code()
    generate_text(node)
    terminate_code()
    return rodata + data + bss + text

def initialize_code():
    global text
    text += '\t' + "mov ebp, esp" + '\n'

def terminate_code():
    global text
    text += '\t' + "mov eax,  1" + '\n'
    text += '\t' + "mov ebx,  0" + '\n'
    text += '\t' + "int 0x80" + '\n'

def generate_text(node):
    if node['type'] == 'translation_unit':		generate_translation_unit(node)
    elif node['type'] == 'assignment':			generate_assignment(node)
    elif node['type'] == 'func_call':       	generate_func_call(node)
    elif node['type'] == 'func_declaration':	generate_function_declaration(node)
    elif node['type'] == 'return':              generate_return_statement(node)


def generate_translation_unit(node):
    for child in node['children']:
        generate_text(child)

def generate_assignment(node):
    if node['var_type']:
        generate_declaration(node)
    else:
       generate_reassignment(node)

def generate_declaration(node):
    #TODO handle constants
    generate_expression(node['children'][1])
    #    if node['var_type'] == 'integer': THIS MIGHT ACTUALLY WORK FOR ALL EXPRESSION TYPES
    global text
    text += '\t' + "sub esp,  4" + '\n'
    text += '\t' + "mov [ebp-4], eax" + '\n'
    for symbol in table.scopes[len(table.scopes) - 1]:
        symbol.offset += 4
    var = table.find_symbol(node['children'][0]['children'][0])
    var.offset = 4

#TODO
def generate_reassignment(node):
    pass

def generate_function_declaration(node):
    global text
    id = node['children'][0]['children'][0]
    text += id + ':' + '\n'
    #first of all create the stack frame
    text += '\t' + "push ebp" + '\n'
    text += '\t' + "mov ebp,  esp" + '\n'
    #function assumes parameters are available since these will be pushed by the function call
    function = table.find_symbol(id)
    parameters = node['parameters']['children']
    table.enter_scope()
    i = 0
    for param in parameters:
        table.add_symbol(symbol_table.Symbol(param['children'][1]['children'][0], param['children'][0],
                                             'parameter', False, offset = (len(function.params)-i) * 4))
        i += 1
    generate(node['children'][1])
    #if function is void the stack frame must be destroyed here, otherwise it's
    #done by the return statement(s)
    if node['func_type'] == "void":
        delete_ar()
    table.exit_scope()
    text += '\n'

def generate_func_call(node):
    id = node['children'][0]['children'][0]
    #first check if the call is to a built in function
    for function in builtin_functions:
        if id == function:
            calling_builtin = "generate_call_to_" + id
            globals()[calling_builtin](node)
            return
    #we're calling a self defined function, start the function prologue
    function = table.find_symbol(id)
    global text, rodata, rodata_index
    if function.params:
        #push parameters in the stack
        found_params = node['children'][1]['children']
        for param in found_params:
            generate_expression(param)
            text += '\t' + "push eax" + '\n'
    text += '\t' + "call " + function.name + '\n'
    if function.params:
        text += '\t' + "add esp,  " + str(len(function.params) * 4) + '\n'

def generate_return_statement(node):
    #return values are passed on eax
    generate_expression(node['children'][0])
    delete_ar()

def generate_call_to_print(node):
    arg_list = node['children'][1]['children'] #array of expressions
    # TODO accept expressions other than values as parameters
    for argument in arg_list:
        param_type = analyzer.type_check(argument)
        generate_expression(argument)
        #now the item to print is in register eax
        global text
        text += '\t' + "push eax" + '\n' #pass the parameter to the print function onto the stack
        if param_type == 'integer':
            text += '\t' + "call print_number" + '\n'
            text += '\t' + "add esp,  4" + '\n'
        elif param_type == 'string':
            text += '\t' + "mov ebx,  " + str(len(node) + 1) + '\n' #+1 for EOL
            text += '\t' + "push ebx" + '\n'
            text += '\t' + "call print_text" + '\n'
            text += '\t' + "add esp,  8" + '\n'


# TODO generate all other expressions
#Expression is evaluated and its value is put in the accumulator (eax)
def generate_expression(node):
    global text, rodata, rodata_index
    if not isinstance(node, dict): #if node is not a dictionary then it's an explicit value
        if isinstance(node, int):
                text += '\t' + "mov eax,  " + str(node) + '\n'
        elif isinstance(node, str):
            rodata += "Label" + str(rodata_index) + ": db " + '"' + str(node)+ '",0' + '\n'
            #this might not be necessary since we can get the info using len(str)
            rodata += "Label" + str(rodata_index) + "Len: equ $-Label" + str(rodata_index) + '\n'
            text += '\t' + "mov eax,  " + "Label" + str(rodata_index) + '\n'
            rodata_index += 1
        #TODO generate code for other types
    elif node['type'] == 'ID':
        id = table.find_symbol(node['children'][0])
        if id.type == 'integer' or id.type == 'string':
            text += '\t' + "mov eax,  DWORD [ebp-" + str(id.offset) +']' + '\n'
    elif node['type'] == "func_call":
        generate_func_call(node)
    elif node['type'] == "modulo": #max dividend 2^(32-1)
        generate_expression(node['children'][0])
        text += '\t' + "push eax" + '\n'
        generate_expression(node['children'][1])
        text += '\t' + "mov ecx,  eax" + '\n'
        text += '\t' + "pop eax" + '\n'
        text += '\t' + "mov edx,  0" + '\n' #make sure edx is cleared as it can mess the division up
        text += '\t' + "div ecx" + '\n'
        text += '\t' + "mov eax,  edx" +'\n' #remainder is in edx but we return values in eax
    elif node['type'] == '+' or node['type'] == '-':
        generate_expression(node['children'][0])
        text += '\t' + "push eax" + '\n'
        generate_expression(node['children'][1])
        text += '\t' + "pop ebx" + '\n'
        if node['type'] == '+':
            #there's no overflow flag checking
            text += '\t' + "add eax, ebx" + '\n'
        else:
            text += '\t' + "sub eax,  ebx" + '\n'
    elif node['type'] == '*' or node['type'] == '/':
        generate_expression(node['children'][0])
        text += '\t' + "push eax" +'\n'
        generate_expression(node['children'][1])
        text += '\t' + "pop ebx" + '\n'
        if node['type'] == '*':
            #again no overflow checking is done for now, the value in edx is ignored
            text += '\t' + "mul ebx" + '\n'
        else:
            text += '\t' + "div ebx" + '\n'
    #TODO implement booleans
    elif node['type'] == "not":
        pass
    elif node['type'] == "and":
        pass
    elif node['type'] == "or":
        pass



def delete_ar():
    global text
    text += '\t' + "mov esp,  ebp" + '\n'
    text += '\t' + "pop ebp" + '\n'
    text += '\t' + "ret" + '\n'