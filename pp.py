import parser
from ast import *


source_code = open("data.txt", 'r').read()
ast = parser.parse(source_code)

def pretty_print(node):
    if node:
        if isinstance(node, Node):
            print node.name
            if len(node.children) > 0 :
                for child in node.children:
                    pretty_print(child)
        else:
            print "this is not a node " + str(node)

pretty_print(ast)
