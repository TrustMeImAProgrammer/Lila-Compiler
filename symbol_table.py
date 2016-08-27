class Symbol:
    def __init__(self, name, type, kind = 'var', constant = False, params = None, offset = 0):
        self.name = name
        self.type = type
        self.kind = kind # kind = function, var, or parameter
        self.is_constant = constant
        self.params = params #parameters needed in case its a function
        self.offset = offset #offset from ebp in case its a local variable, used only in code generation
#--------------------------------
#This is a stack of scopes, 
#the stack is implemented as a list
#symbols is a list of lists, 
#each list contains all symbols in a scope
#--------------------------------
class SymbolTable:
    #symbols must be an array containing existing symbols in the first scope
    def __init__(self, symbols = None):
        self.scopes = [] #scopes is an array of arrays, containing all scopes
        if symbols:
            self.scopes.append(symbols)
        else:
            #append an empty scope
            self.scopes.append([])

    def enter_scope(self):
        self.scopes.append([])

    #look for symbol x in all currently
    #available scopes
    def find_symbol(self, x):
        for scope_symbols in reversed(self.scopes):
            for symbol in scope_symbols:
                if symbol.name == x:
                    return symbol
        return None

    def add_symbol(self, x):
        self.scopes[len(self.scopes) - 1].append(x)

    #look for symbol x in current scope
    #returns true if it's found, false otherwise
    def check_scope(self, x):
        for symbol in self.scopes[len(self.scopes) - 1]:
            if symbol.name == x:
                return True
        return False

    def exit_scope(self):
        self.scopes.pop()


# st = SymbolTable()
# x = Symbol("x", "int")
# y = Symbol("y", "bool")
# st.add_symbol(x)
# st.add_symbol(y)
# print st.check_scope("x")
# st.enter_scope()
# yy = Symbol("y", "float")
# st.add_symbol(yy)
# result = st.find_symbol("y")
# if result:
#     print result.name
#     print result.type
#
# print "size of symbols = " + str(len(st.scopes))

