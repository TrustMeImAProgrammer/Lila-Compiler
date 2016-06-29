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
    def __init__(self, name, id, children):
        self.id = id
        super(FuncCall, self).__init__(name, children)

class Declaration(Node):
    pass
