from __future__ import annotations

import builtins as py_builtins
import importlib
import operator
import sys
from types import BuiltinFunctionType
from typing import Any, cast

from .ast_nodes import (
    ArrayLiteral,
    AssignStmt,
    Binary,
    BlockExpr,
    Call,
    ExprStmt,
    FromImportStmt,
    FunctionLiteral,
    GetAttr,
    Identifier,
    IfExpr,
    ImportStmt,
    IndexExpr,
    Literal,
    ObjectLiteral,
    Program,
    ReturnStmt,
    Unary,
)
from .environment import Environment
from .errors import CoffeeRuntimeError
from .lexer import Lexer
from .parser import Parser
from .tokens import (
    AND,
    EQEQ,
    GT,
    GTE,
    LT,
    LTE,
    MINUS,
    NEQ,
    NOT,
    OR,
    PERCENT,
    PLUS,
    SLASH,
    STAR,
    STARSTAR,
)


class _ReturnSignal(Exception):
    def __init__(self, value):
        super().__init__("function return")
        self.value = value


class CoffeeFunction:
    def __init__(self, params: list[str], body, closure: Environment, interpreter: "Interpreter"):
        self.params = params
        self.body = body
        self.closure = closure
        self.interpreter = interpreter

    def __call__(self, *args, **kwargs):
        call_env = Environment(parent=self.closure)

        for index, name in enumerate(self.params):
            value = args[index] if index < len(args) else None
            call_env.define(name, value)

        for name, value in kwargs.items():
            call_env.define(name, value)

        previous = self.interpreter.environment
        self.interpreter.environment = call_env
        try:
            try:
                return self.interpreter._evaluate(self.body)
            except _ReturnSignal as signal:
                return signal.value
        finally:
            self.interpreter.environment = previous

    def __repr__(self) -> str:
        params = ", ".join(self.params)
        return f"<CoffeeFunction ({params})>"


class Interpreter:
    def __init__(self, stdout=None):
        self.stdout = stdout if stdout is not None else sys.stdout
        self.environment = Environment()
        self._install_builtins()

    def interpret(self, source: str):
        tokens = Lexer(source).tokenize()
        program = Parser(tokens).parse()
        return self.execute_program(program)

    def execute_program(self, program: Program):
        result = None
        try:
            for statement in program.statements:
                result = self._execute(statement)
        except _ReturnSignal as signal:
            raise CoffeeRuntimeError("'return' used outside function.") from signal
        return result

    def _install_builtins(self) -> None:
        self.environment.define("print", self._builtin_print)

    def _builtin_print(self, *args):
        text = " ".join(str(arg) for arg in args)
        self.stdout.write(text + "\n")
        return None

    def _execute(self, statement):
        if isinstance(statement, ImportStmt):
            self._execute_import(statement)
            return None

        if isinstance(statement, FromImportStmt):
            self._execute_from_import(statement)
            return None

        if isinstance(statement, AssignStmt):
            value = self._evaluate(statement.value)
            self._assign_target(statement.target, value)
            return value

        if isinstance(statement, ReturnStmt):
            if statement.value is None:
                raise _ReturnSignal(None)
            raise _ReturnSignal(self._evaluate(statement.value))

        if isinstance(statement, ExprStmt):
            return self._evaluate(statement.expression)

        raise CoffeeRuntimeError("Unsupported statement.")

    def _execute_import(self, statement: ImportStmt) -> None:
        for item in statement.items:
            module_obj = importlib.import_module(item.module)

            if item.alias is not None:
                self.environment.define(item.alias, module_obj)
                continue

            if "." in item.module:
                root_name = item.module.split(".", 1)[0]
                root_module = importlib.import_module(root_name)
                self.environment.define(root_name, root_module)
            else:
                self.environment.define(item.module, module_obj)

    def _execute_from_import(self, statement: FromImportStmt) -> None:
        module_obj = importlib.import_module(statement.module)
        for imported in statement.names:
            if not hasattr(module_obj, imported.name):
                raise CoffeeRuntimeError(
                    f"Module '{statement.module}' has no attribute '{imported.name}'."
                )

            value = getattr(module_obj, imported.name)
            bind_name = imported.alias if imported.alias is not None else imported.name
            self.environment.define(bind_name, value)

    def _assign_target(self, target, value) -> None:
        if isinstance(target, Identifier):
            self.environment.assign(target.name, value)
            return

        if isinstance(target, GetAttr):
            container = self._evaluate(target.target)
            self._set_attr(container, target.name, value)
            return

        if isinstance(target, IndexExpr):
            container = self._evaluate(target.target)
            index = self._evaluate(target.index)
            if not hasattr(container, "__setitem__"):
                raise CoffeeRuntimeError("Target does not support index assignment.")

            try:
                cast(Any, container)[index] = value
            except Exception as exc:
                raise CoffeeRuntimeError(f"Index assignment failed: {exc}") from exc
            return

        raise CoffeeRuntimeError("Invalid assignment target.")

    @staticmethod
    def _set_attr(container, name: str, value) -> None:
        if isinstance(container, dict):
            container[name] = value
            return

        try:
            setattr(container, name, value)
        except Exception as exc:
            raise CoffeeRuntimeError(f"Attribute assignment failed: {exc}") from exc

    def _evaluate(self, expression):
        if isinstance(expression, Literal):
            return expression.value

        if isinstance(expression, BlockExpr):
            block_result = None
            for statement in expression.statements:
                block_result = self._execute(statement)
            return block_result

        if isinstance(expression, Identifier):
            return self._lookup_identifier(expression.name)

        if isinstance(expression, Unary):
            right = self._evaluate(expression.right)
            if expression.operator == MINUS:
                if right is None:
                    raise CoffeeRuntimeError("Unary '-' not supported for None.")
                return -right
            if expression.operator == PLUS:
                if right is None:
                    raise CoffeeRuntimeError("Unary '+' not supported for None.")
                return +right
            if expression.operator == NOT:
                return not right
            raise CoffeeRuntimeError("Unsupported unary operator.")

        if isinstance(expression, Binary):
            return self._evaluate_binary(expression)

        if isinstance(expression, IfExpr):
            condition = self._evaluate(expression.condition)
            if condition:
                return self._evaluate(expression.then_branch)
            return self._evaluate(expression.else_branch)

        if isinstance(expression, FunctionLiteral):
            return CoffeeFunction(expression.params, expression.body, self.environment, self)

        if isinstance(expression, ArrayLiteral):
            return [self._evaluate(item) for item in expression.items]

        if isinstance(expression, ObjectLiteral):
            object_value: dict[str, object] = {}
            for key, value_expr in expression.items:
                object_value[key] = self._evaluate(value_expr)
            return object_value

        if isinstance(expression, GetAttr):
            target = self._evaluate(expression.target)
            if isinstance(target, dict) and expression.name in target:
                return target[expression.name]
            if hasattr(target, expression.name):
                return getattr(target, expression.name)
            raise CoffeeRuntimeError(f"Attribute '{expression.name}' not found.")

        if isinstance(expression, IndexExpr):
            target = self._evaluate(expression.target)
            index = self._evaluate(expression.index)
            try:
                return target[index]
            except Exception as exc:
                raise CoffeeRuntimeError(f"Index operation failed: {exc}") from exc

        if isinstance(expression, Call):
            callee = self._evaluate(expression.callee)
            args = [self._evaluate(arg) for arg in expression.args]
            kwargs = {name: self._evaluate(value_expr) for name, value_expr in expression.kwargs}

            if not callable(callee):
                raise CoffeeRuntimeError("Target is not callable.")

            try:
                return callee(*args, **kwargs)
            except CoffeeRuntimeError:
                raise
            except Exception as exc:
                raise CoffeeRuntimeError(f"Call failed: {exc}") from exc

        raise CoffeeRuntimeError("Unsupported expression.")

    def _lookup_identifier(self, name: str):
        try:
            return self.environment.get(name)
        except CoffeeRuntimeError:
            pass

        if hasattr(py_builtins, name):
            value = getattr(py_builtins, name)
            if isinstance(value, (BuiltinFunctionType, type)) or callable(value):
                return value
            return value

        raise CoffeeRuntimeError(f"Undefined identifier '{name}'.")

    def _evaluate_binary(self, expression: Binary):
        if expression.operator == OR:
            left = self._evaluate(expression.left)
            if left:
                return left
            return self._evaluate(expression.right)

        if expression.operator == AND:
            left = self._evaluate(expression.left)
            if not left:
                return left
            return self._evaluate(expression.right)

        left = self._evaluate(expression.left)
        right = self._evaluate(expression.right)

        if expression.operator == EQEQ:
            return left == right
        if expression.operator == NEQ:
            return left != right
        if expression.operator == LT:
            return left < right
        if expression.operator == LTE:
            return left <= right
        if expression.operator == GT:
            return left > right
        if expression.operator == GTE:
            return left >= right

        binary_ops = {
            PLUS: operator.add,
            MINUS: operator.sub,
            STAR: operator.mul,
            SLASH: operator.truediv,
            PERCENT: operator.mod,
            STARSTAR: operator.pow,
        }

        fn = binary_ops.get(expression.operator)
        if fn is None:
            raise CoffeeRuntimeError("Unsupported binary operator.")

        try:
            return fn(left, right)
        except Exception as exc:
            raise CoffeeRuntimeError(f"Binary operation failed: {exc}") from exc
