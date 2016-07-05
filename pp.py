import parser
import lex

source_code = open("data.txt", 'r').read()
ast = parser.parse(source_code)

def pretty_print(node):
    if node:
        if isinstance(node, dict):
            print node['type']
            if len(node['children']) > 0 :
                for child in node['children']:
                    pretty_print(child)
        elif isinstance(node, lex.LexToken):
            print "this is a token at lineno {0}".format(node.lineno)
        else:
            print "this is not a node nor a lextoken " + str(node)

pretty_print(ast)
