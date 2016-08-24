class Symbol:
    def __init__(self, name, type, kind = 'var', constant = False, params = None, offset = None, strlen = None):
        self.name = name
        self.type = type
        self.kind = kind # kind = function, var, or parameter
        self.is_constant = constant
        self.params = params #parameters needed in case its a function
        self.offset = offset #offset from esp in case its a local variable, used only in code generation
        self.length = strlen #length of strings
#--------------------------------
#This is a stack of scopes, 
#the stack is implemented as a list
#symbols is a list of lists, 
#each list contains all symbols in a scope
#--------------------------------
class SymbolTable:
    def __init__(self, symbols = None):
        #by default there's just one scope with no symbols
        self.scope = 0
        self.symbols = [] #symbols is an array of arrays, each array is the symbols in a scope
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

    def count_scopes(self):
        return self.scope


st = SymbolTable()
x = Symbol("x", "int")
y = Symbol("y", "bool")
st.add_symbol(x)
st.add_symbol(y)
print st.check_scope("x")
st.enter_scope()
yy = Symbol("y", "float")
st.add_symbol(yy)
result = st.find_symbol("y")
if result:
    print result.name
    print result.type

print "size of symbols = " + str(len(st.symbols))
