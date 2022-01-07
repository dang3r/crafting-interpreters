from lox.errors import RuntimeError

class Environment:
    def __init__(self, enclosing = None):
        self.values = dict()
        self.enclosing = None

    def define(self, key, value) -> None:
        self.values[key] = value

    def get(self, key):
        if key in self.values:
            return self.values[key]
        if self.enclosing:
            return self.enclosing,get(key)
        raise RuntimeError(key, f"Undefined variable '{key.lexeme}'.")

    def assign(self, key, value) -> None:
        if key in self.values:
            self.values[key] = value
            return
        if self.enclosing:
            self.enclosing.assign(key, value)
        raise RuntimeError(key, f"Undefined variable '{key.lexeme}'.")