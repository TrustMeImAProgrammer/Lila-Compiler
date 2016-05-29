class Node(object):
    def __init__(self, type, children):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = [ ]
    def show(self):
        pass

class BinaryOp(Node):
    def __init__(self, type, children):
        super(BinaryOp, self).__init__(type, children)

class UnaryOp(Node):
    def __init__(self, type, children):
        super(UnaryOp, self).__init__(type, children)

class FuncCall(Node):
    def __init__(self, type, children):
        super(FuncCall, self).__init__(type, children)

class PreIncrExpression(Node):
    def __init__(self, type, children):
        super(PreIncrExpression, self).__init__(type, children)

class PreDecrExpression(Node):
    def __init__(self, type, children):
        super(PreDecrExpression, self).__init__(type, children)
