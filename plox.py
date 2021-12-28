import re
import sys
import scanner

had_error = False

def main():
    if len(sys.argv) > 2:
        print("Usage: plox [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()

def run_file(file: str) -> None:
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
    sc = scanner.Scanner(source)
    tokens = sc.scan_tokens()
    for token in tokens:
        print(token)

def error(line: int, message: str) -> None:
    report(line, "", message)

def report(line: int, where: str, message: str) -> None:
    global had_error
    print("[line %s] Error %s: %s" % (line, where, message), file=sys.stderr)
    had_error = True


if __name__ == "__main__":
    main()