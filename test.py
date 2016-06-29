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
x = ProgramNode("carlos", [])
print x.name
print x.children
