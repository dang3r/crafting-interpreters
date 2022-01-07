import sys

from lox import scanner
from lox.tokens import Token, TokenType
from lox.parser import Parser
from lox.ast_printer import NewAstPrinter, AstRPNPrinter
from lox.interpreter import Interpreter

had_error = False
had_runtime_error = False

def run_file(file: str) -> None:
    global had_error
    with open(file, "r") as f:
        bytes = f.read()
    run(bytes)
    if had_error:
        sys.exit(65)
    if had_runtime_error:
        sys.exit(70)

def run_prompt() -> None:
    global had_error
    while True:
        print("> ", end="")
        line = input()
        if not line:
            break
        run(line)
        had_error = False

def run(source: str) -> None:
    global had_error
    sc = scanner.Scanner(source)
    tokens = sc.scan_tokens()
    p = Parser(tokens)
    stmts = p.parse()
    if had_error:
        return
    i = Interpreter()
    i.interpret(stmts)

def error(line: int, message: str) -> None:
    report(line, "", message)

def error_token(token: Token, message: str):
    if token.type == TokenType.EOF:
        report(token.line, "at end", message)
    else:
        report(token.line,  f"at '{token.lexeme}'", message)

def report(line: int, where: str, message: str) -> None:
    print("[line %s] Error %s: %s" % (line, where, message), file=sys.stderr)
    global had_error
    had_error = True
    print()

def runtime_error(error):
    print(f"{error.message}\n[line {error.token.line}]+ ")
    had_runtime_error = True
