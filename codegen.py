import analyzer
table = analyzer.symboltable


rodata = "SECTION .rodata" + '\n'

data = "SECTION .data" + '\n'
data = data + 'True: db "True",10' + '\n'
data = data + 'TrueLen: equ $-True' + '\n'
data = data + 'False: db "False",10' + '\n'
data = data + 'FalseLen: equ $-False' + '\n'

bss = "SECTION .bss" + '\n'

text = "_start:" + '\n'

rodata_index = 0
data_index = 0

builtin = "SECTION .text" + '\n'
builtin += "global _start" + '\n'
builtin_functions = ['print', 'str']

def generate(node):
    initialize_code()
    generate_text(node)
    terminate_code()
    return rodata + data + bss + builtin + text

def initialize_code():
    generate_builtin_functions()
    global text
    text += '\t' + "mov ebp, esp" + '\n'

def terminate_code():
    global text
    text += '\t' + "mov eax,  1" + '\n'
    text += '\t' + "mov ebx,  0" + '\n'
    text += '\t' + "int 0x80"
def generate_builtin_functions():
    global builtin
    printf = open('print.asm', 'r')
    builtin += printf.read()
    printf.close()

def generate_text(node):
    if node['type'] == 'translation_unit':	generate_translation_unit(node)
    elif node['type'] == 'assignment':		generate_assignment(node)
    elif node['type'] == 'func_call':       generate_func_call(node)
    
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
        for param in function.params:
            if param['children'][0] == "integer":
                text += '\t' + "push " + str(param['children'][1]['children'][0]) + '\n'
            elif param['children'][0] == "string":
                rodata += "Label" + str(rodata_index) + ": db " + '"' + node + '",0' + '\n'
                text += '\t' + "push " + "Label" + str(rodata_index) + '\n'
            #TODO pop params off stack




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
