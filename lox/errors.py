from lox.tokens import Token

class RuntimeError(Exception):
    def __init__(self, token: Token, message: str):
        self.message = message
        self.token = token
