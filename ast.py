class Node(object):
    def __init__(self, name, children):
        self.name = name
        if children:
            self.children = children
        else:
            self.children = [ ]
    def show(self):
        pass

class ProgramNode(Node):
    pass

class TranslationUnit(Node):
    pass

class BinaryOp(Node):
    pass

class UnaryOp(Node):
    pass

class FuncCall(Node):
    #type will be looked up during code generation in the symbol table
    pass

class Assignment(Node):
    def __init__(self, name, type, children): #type is the type of the variable being assigned
        self.type = type
        super(Assignment, self).__init__(name, children)

class Return(Node):
    pass

class FuncDecl(Node):
    def __init__(self, name, params, children):
        self.params = params
        super(FuncDecl, self).__init__(name, children)

class ParamsList(Node):
    pass

class ParamDecl(Node):
    pass

class ArgList(Node):
    pass

class If(Node):
    pass

class While(Node):
    pass
