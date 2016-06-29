class Node(object):
    def __init__(self, name, left, right):
        self.name = name
        if children:
            self.children = children
        else:
            self.children = [ ]
    def show(self):
        pass

class ProgramNode(Node):
    pass

class BinaryOp(Node):
    pass

class UnaryOp(Node):
    pass

class FuncCall(Node):
    def __init__(self, name, children, id):
        self.id = id
        super(FuncCall, self).__init__(name, children)

class PreIncrExpression(Node):
    pass

class PreDecrExpression(Node):
    pass

class Declaration(Node):
    pass

		   |	REAL ID EQUALS FLOAT
		   | 	STRING ID EQUALS SLITERAL
    		   |	CHARACTER ID EQUALS
		   |	BOOLEAN ID EQUALS TRUE
		   | 	BOOLEAN ID EQUALS FALSE
