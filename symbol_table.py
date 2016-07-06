class Symbol:
    def __init__(self, name, type, kind, constant, params = None):
        self.name = name
        self.type = type
        self.kind = kind # kind = function, var, or parameter
        self.is_constant = constant
        if params:
            self.params = params
#--------------------------------
#This is a stack of scopes, 
#the stack is implemented as a list
#symbols is a list of lists, 
#each list contains all symbols in a scope
#--------------------------------
class SymbolTable:
    def __init__(self, symbols):
        #by default there's just one scope with no symbols
        self.scope = 0
        self.symbols = []
        if symbols:
            self.symbols.append(symbols)
        else:
            self.symbols.append([])

    def enter_scope(self):
        self.symbols.append([])
        self.scope += 1

    #look for symbol x in all currently
    #available scopes
    def find_symbol(self, x):
        for scope_symbols in reversed(self.symbols):            
            for symbol in scope_symbols:
                if symbol.name == x:
                    return symbol
        return None

    def add_symbol(self, x):
        self.symbols[self.scope].append(x)

    #look for symbol x in current scope
    #returns true if it's found, false otherwise
    def check_scope(self, x):
        for symbol in self.symbols[self.scope]:
            if symbol.name == x:
                return True
        return False

    def exit_scope(self):
        self.symbols.pop()
        self.scope -= 1

# x = Symbol("x", "int")
# y = Symbol("y", "bool")
# st = SymbolTable([x, y])
# print st.check_scope("x")
# st.enter_scope()
# yy = Symbol("y", "float")
# st.add_symbol(yy)
# result = st.find_symbol("y")
# if result:
#     print result.name
#     print result.type
