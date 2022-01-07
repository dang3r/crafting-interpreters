class Stmt:
    pass

class Print(Stmt):
    def __init__(self, expr):
        self.expr = expr

class Expression(Stmt):
    def __init__(self, expr):
        self.expr = expr

class Var(Stmt):
    def __init__(self, name, initializer=None):
        self.name = name
        self.initializer = initializer

class Block(Stmt):
    def __init__(self, stmts):
        self.stmts = stmts
