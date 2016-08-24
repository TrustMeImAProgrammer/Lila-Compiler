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
text = text + "global _start" + '\n'
text = text + "_start:" + '\n'

rodata_index = 0
data_index = 0

builtin = ""

def generate(node):
    generate_builtin_functions()
    if node['type'] == 'translation_unit':	generate_translation_unit(node)
    if node['type'] == 'assignment':		generate_assignment(node)
    return rodata + data + bss + text + builtin;


def generate_builtin_functions:
    printf = open('print.asm', 'r')
    builtin += printf.read()
    printf.close()
    
def generate_translation_unit(node):
    for child in node['children']:
        generate(child)


def generate_assignment(node):
    if node['var_type']:
        generate_declaration(node)
    else:
        generate_reassignment(node)

def generate_declaration(node):
    #TODO handle constants
    generate_expression(node['children'][1])
    #    if node['var_type'] == 'integer': THIS MIGHT ACTUALLY WORK FOR ALL EXPRESSION TYPES
    text += '\t' + "sub esp,  4"
    text += '\t' + "mov [ebp-4], eax"
    var = table.find_symbol(node['children'][0])
    var.offset = 0
    for symbol in table.symbols:
        
        

def generate_reassignment(node):

def generate_call_to_print(node):
    arg_list = node['children'][1][0] #array of expressions
    arg_number = len(node['children'][1][0])
    # TODO accept expressions other than values as parameters
    for argument in arg_list:
        param_type = analyzer.type_check(node)
        generate_expression(argument)
        #now the item to print is in register eax
        text += '\t' + "push eax" + '\n' #pass the parameter to the print function onto the stack
        if param_type == 'integer':
            text += '\t' + "call PrintNumber"
            text += '\t' + "add esp,  4" + '\n'
        elif param_type == 'string':
            text += '\t' + "mov ebx,  " + len(node) + 1 #+1 for EOL
            text += '\t' + "push ebx"
            text += '\t' + "call PrintText"
            text += '\t' + "add esp,  8" + '\n'
        


# TODO generate all other expressions
#Expression is evaluated and its value is put in the accumulator (eax)
def generate_expression(node):
    if not isinstance(node, dict): #if node is not a dictionary then it's an explicit value
        if type(node) == 'int':
                text += '\t' + "mov eax,  " + node + '\n'
        elif type(node) == 'string' :
            rodata += "Label" + rodata_index + ": db " + '"' + node + '",0' + '\n'
            #this might not be neccesary since we can get the info using len(str)
            rodata += "Label" + rodata_index + "Len: equ $-Label" + rodata_index + '\n'
            text += '\t' + "mov eax,  " + Label + rodata_index + '\n'
            rodata_index += 1
