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
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
    def children(self):
        nodelist = []
        if self.expr is not None:
            nodelist.append(("expr", self.expr))
        return tuple(nodelist)

class FuncCall(Node):
    def __init__(self, type, children):
        super(FuncCall, self).__init__(type, children)
