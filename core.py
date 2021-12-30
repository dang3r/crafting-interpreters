import sys

import scanner

had_error = False

def run_file(file: str) -> None:
    global had_error
    with open(file, "r") as f:
        bytes = f.read()
    run(bytes)
    if had_error:
        sys.exit(65)

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
    for token in tokens:
        print(token)

def error(line: int, message: str) -> None:
    report(line, "", message)

def report(line: int, where: str, message: str) -> None:
    print("[line %s] Error %s: %s" % (line, where, message), file=sys.stderr)
    global had_error
    had_error = True
    print()

