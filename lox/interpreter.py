from typing import List

from lox import core
from lox.lox_types import Expr, Binary, Grouping, Literal, Unary, Variable, Assignment
from lox.tokens import TokenType, Token
from lox.typedispatch import visitor, _methods
from lox.statements import Print, Expression, Var, Stmt, Block
from lox.environment import Environment
from lox.errors import RuntimeError

class Interpreter:
    def __init__(self):
        self.environment = Environment()

    def interpret(self, stmts: List[Stmt]):
        try:
            for stmt in stmts:
                val = self.visit(stmt)
        except RuntimeError as error:
            core.runtime_error(error)

    def stringify(self, val) -> str:
        if val is None:
            return "nil"

        if type(val) == float and val.is_integer():
            return str(int(val))
        return str(val)

    @visitor(Block)
    def visit(self, block: Block):
        self.execute_block(block.stmts, Environment(self.environment))

    def execute_block(self, stmts, environment):
        prev = environment
        try:
            for stmt in stmts:
                self.visit(stmt)
        except:
            pass
        finally:
            self.environment = prev


    @visitor(Print)
    def visit(self, expr: Print):
        val = self.visit(expr.expr)
        print(self.stringify(val))

    @visitor(Expression)
    def visit(self, expr: Expression):
        self.visit(expr.expr)

    @visitor(Var)
    def visit(self, var: Var) -> None:
        value = None
        if var.initializer is not None:
            value = self.visit(var.initializer)
        self.environment.define(var.name.lexeme, value)

    @visitor(Variable)
    def visit(self, var: Variable):
        return self.environment.get(var.name)

    @visitor(Assignment)
    def visit(self, expr):
        val = self.visit(expr.value)
        self.environment.assign(expr.name, val)
        return val
        
    @visitor(Binary)
    def visit(self, expr: Binary):
        left = self.visit(expr.left)
        right = self.visit(expr.right)
        if expr.operator.type == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return left - right
        elif expr.operator.type == TokenType.PLUS:
            self.check_number_operands(expr.operator, left, right)
            return left + right
        elif expr.operator.type == TokenType.STAR:
            self.check_number_operands(expr.operator, left, right)
            return left * right
        elif expr.operator.type == TokenType.SLASH:
            self.check_number_operands(expr.operator, left, right)
            if right == 0:
                raise RuntimeError(expr.operator, "Right operand must be non-zero")
            return left / right
        elif expr.operator.type == TokenType.PLUS:
            # TODO: Redundant?
            if type(right) == type(left) == str:
                return left + right
            elif type(right) == type(left) == type(float):
                return left + right
            elif (type(right) == str and type(left) == float) or (type(left) == float and type(right) == str):
                return str(left) + str(right)
            raise RuntimeError(expr.operator, "Operands must be two numbers or two strings.")
        elif expr.operator.type == TokenType.GREATER:
            self.check_number_operands(expr.operator, left, right)
            return left > right
        elif expr.operator.type == TokenType.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left >= right
        elif expr.operator.type == TokenType.LESS:
            self.check_number_operands(expr.operator, left, right)
            return left < right
        elif expr.operator.type == TokenType.LESS_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left <= right
        elif expr.operator.type == TokenType.BANG_EQUAL:
            return left != right
        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            return left == right
 

    @visitor(Unary)
    def visit(self, expr: Unary):
        right = self.visit(expr.right)
        if expr.operator.type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -1*right
        elif expr.operator.type == TokenType.BANG:
            return not self.is_truthy(right)

    @visitor(Grouping)
    def visit(self, expr: Grouping):
        return self.visit(expr)

    @visitor(Literal)
    def visit(self, expr: Literal):
        return expr.value

    def is_tuthy(self, expr) -> bool:
        if expr == None: return False
        if type(expr) == bool: return expr
        return True

    def is_equal(self, a, b) -> bool:
        #TODO: Is this redundant?
        if a is None and b is None:
            return True
        elif a is None:
            return False
        return a == b

    def check_number_operand(self, operator: Token, operand):
        if type(operand) == float:
            return
        raise RuntimeError(operator, "Operand must be a number")

    def check_number_operands(self, operator: Token, left, right):
        if type(left) == float and type(right) == float:
            return
        raise RuntimeError(operator, "Operands must be numbers.")
