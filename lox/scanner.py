from typing import Any

from lox import core
from lox.tokens import Token, TokenType

KEYWORDS = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "fun": TokenType.FUN,
    "for": TokenType.FOR,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}

class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> None:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self) -> None:
        char = self.advance()
        if char == "(": self.add_token(TokenType.LEFT_PAREN)
        elif char == ")": self.add_token(TokenType.RIGHT_PAREN)
        elif char == "{": self.add_token(TokenType.LEFT_BRACE)
        elif char == "}": self.add_token(TokenType.RIGHT_BRACE)
        elif char == ",": self.add_token(TokenType.COMMA)
        elif char == ".": self.add_token(TokenType.DOT)
        elif char == "-": self.add_token(TokenType.MINUS)
        elif char == "+": self.add_token(TokenType.PLUS)
        elif char == ";": self.add_token(TokenType.SEMICOLON)
        elif char == "*": self.add_token(TokenType.STAR)
        elif char == "!": self.add_token(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
        elif char == "=": self.add_token(TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL)
        elif char == "<": self.add_token(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
        elif char == ">": self.add_token(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER)
        elif char == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()

            # Support nested C-style multiline comments
            elif self.match("*"):
                count = 1
                while not self.is_at_end() and count > 0:
                    char = self.advance()
                    if char == "\n":
                        self.line += 1                        
                    elif char == "/" and self.peek() == "*":
                        count += 1
                        self.advance()
                    elif char == "*" and self.peek() == "/":
                        count -= 1
                        self.advance()
                
                if count and self.is_at_end():
                    core.error(self.line, "Unterminated multi-line nested comment")
            else:
                self.add_token(TokenType.SLASH)
        elif char in set([" ", "\r", "\t"]): pass
        elif char == "\n": self.line += 1
        elif char == '"':
            while self.peek() != '"' and not self.is_at_end():
                if self.peek() == "\n":
                    self.line += 1
                self.advance()

            if self.is_at_end():
                core.error(self.line, "Unterminated string.")
                return

            self.advance()
            self.add_token(TokenType.STRING, self.source[self.start + 1: self.current-1])
        elif self.is_digit(char): self.number()
        elif self.is_alpha(char): self.identifier()
        else:
            core.error(self.line, "Unexpected character")

    def add_token(self, type: TokenType, literal: Any = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        return char

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if expected != self.source[self.current]:
            return False

        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()

        while self.is_digit(self.peek()):
            self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start: self.current]))

    def identifier(self) -> None:
        while self.is_alphanumeric(self.peek()):
            self.advance()

        text = self.source[self.start: self.current]
        self.add_token(KEYWORDS.get(text, TokenType.IDENTIFIER))

    def is_digit(self, s: str) -> bool:
        return s in set("0123456789")

    def is_alpha(self, char: str) -> bool:
        return char.upper() in set("ABCDEFGHIJKLMNOPQRSTUVWXYZ_")

    def is_alphanumeric(self, char: str) -> bool:
        return self.is_digit(char) or self.is_alpha(char) or char == "_"