import sys
from typing import List


def main():
    if len(sys.argv) != 1:
        print("Usage: python3 generate_ast.py")
        sys.exit(64)
    types = [
        "Binary   : Expr left, Token operator, Expr right",
        "Grouping : Expr expression",
        "Literal  : Any value",
        "Unary    : Token operator, Expr right",
    ]

    define_ast("Expr", types)


def define_ast(base_class: str, types: List[str]):
    print(f"""from abc import ABC, abstractmethod
from typing import Any

from tokens import Token, TokenType

class {base_class}(ABC):
    @abstractmethod
    def accept(self, visitor) -> Any:
        pass""") 

    for type in types:
       define_type(type, base_class)

    define_visitor(base_class, types)

def define_visitor(base_class: str, types: List[str]):
    print()
    print("class Visitor(ABC):")
    for type in types:
        cls = type.split(":")[0].strip()
        print(f"   @abstractmethod")
        print(f"   def visit_{cls.lower()}_{base_class.lower()}(self, expr: {cls}):")
        print(f"        pass")
        print()



def define_type(type: str, base_class: str):
    cls, attrs = [item.strip() for item in type.split(":")]
    print()
    print(f"class {cls}({base_class}):")
    vars = [tuple(attr.strip().split(" ")) for attr in attrs.split(",")]

    s = "   def __init__(self"
    for (_type, val) in vars:
        s += f", {val}: {_type}"
    s += "):"
    print(s)
    for _type, val in vars:
        print(f"      self.{val} = {val}")
    print()
    print(f"""   def accept(self, visitor):
        return visitor.visit_{cls.lower()}_expr(self)
""")




if __name__ == "__main__":
    main()
