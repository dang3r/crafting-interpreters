from lox.lox_types import Expr, Binary, Grouping, Literal, Unary
from lox.tokens import TokenType, Token
from lox.typedispatch import visitor

class AstPrinter:
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal):
        if expr.value == None:
            return ""
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        s = f"({name}"
        for expr in exprs:
            s += " "
            s+= expr.accept(self)
        s += ")"
        return s

class NewAstPrinter:
    def print(self, expr: Expr) -> str:
        return self.visit(expr)

    @visitor(Binary)
    def visit(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    @visitor(Unary)
    def visit(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    @visitor(Grouping)
    def visit(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)

    @visitor(Literal)
    def visit(self, expr: Literal):
        if expr.value == None:
            return ""
        return str(expr.value)

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        s = f"({name}"
        for expr in exprs:
            s += " "
            s+= self.visit(expr)
        s += ")"
        return s

class AstRPNPrinter:
    def print(self, expr: Expr) -> str:
        return self.visit(expr)

    @visitor(Binary)
    def visit(self, expr: Binary) -> str:
        return "{} {} {}".format(self.visit(expr.left), self.visit(expr.right), expr.operator.lexeme)

    @visitor(Unary)
    def visit(self, expr: Unary) -> str:
        return "{} {}".format(self.visit(expr.right), expr.operator.lexeme)

    @visitor(Grouping)
    def visit(self, expr: Grouping):
        return self.visit(expr.expression)

    @visitor(Literal)
    def visit(self, expr: Literal) -> str:
        if expr.value == None:
            return ""
        return str(expr.value)

def main():
    expr: Expr = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123)
        ),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(
            Literal(45.67)
        )
    )
    print(NewAstPrinter().print(expr))
    expr_rpn: Expr = Binary(
        Binary(
            Literal(1),
            Token(TokenType.PLUS, "+", None, -1),
            Literal(2)
        ),
        Token(TokenType.STAR, "*", None, -1),
        Binary(
            Literal(4),
            Token(TokenType.MINUS, "-", None, -1),
            Literal(3)
        ),
    )
    print(AstRPNPrinter().print(expr_rpn))

if __name__ == "__main__":
    main()