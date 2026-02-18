from __future__ import annotations

import builtins as py_builtins
import importlib
import operator
import sys
from types import BuiltinFunctionType
from typing import Any, cast

from .ast_nodes import (
    ArrayDestructuring,
    ArrayLiteral,
    AssignStmt,
    AugAssignStmt,
    Binary,
    BlockExpr,
    BreakStmt,
    Call,
    ChainedComparison,
    ClassDecl,
    ComprehensionExpr,
    ContinueStmt,
    DoExpr,
    ExistentialAssignStmt,
    ExistentialExpr,
    ExprStmt,
    Expression,
    ForInStmt,
    ForOfStmt,
    FromImportStmt,
    FunctionLiteral,
    GetAttr,
    Identifier,
    IfExpr,
    ImportStmt,
    InExpr,
    IndexExpr,
    InterpolatedString,
    Literal,
    LogicalAssignStmt,
    MultiAssignStmt,
    NewExpr,
    ObjectComprehensionExpr,
    ObjectDestructuring,
    ObjectLiteral,
    OfExpr,
    Program,
    ProtoAccessExpr,
    RangeLiteral,
    ReturnStmt,
    SafeAccessExpr,
    SliceExpr,
    SplatExpr,
    SpreadExpr,
    Statement,
    SuperExpr,
    SwitchExpr,
    ThisExpr,
    ThrowStmt,
    TryStmt,
    Unary,
    UpdateStmt,
    WhileStmt,
    YieldExpr,
)
from .environment import Environment
from .errors import CoffeeRuntimeError
from .lexer import Lexer
from .parser import Parser
from .tokens import (
    AND,
    ANDAND,
    EQEQ,
    GT,
    GTE,
    LT,
    LTE,
    MINUS,
    MINUSMINUS,
    MINUS_EQ,
    NEQ,
    NOT,
    OR,
    OROR,
    PERCENT,
    PLUS,
    PLUSPLUS,
    PLUS_EQ,
    SLASH,
    STAR,
    STARSTAR,
)


class _ReturnSignal(Exception):
    def __init__(self, value):
        super().__init__("function return")
        self.value = value


class _BreakSignal(Exception):
    pass


class _ContinueSignal(Exception):
    pass


class _ThrowSignal(Exception):
    def __init__(self, value):
        super().__init__("throw")
        self.value = value


class CoffeeClass:
    def __init__(self, name: str, parent, methods: dict, interpreter: "Interpreter"):
        self.name = name
        self.parent = parent
        self.methods = methods
        self.interpreter = interpreter

    def __call__(self, *args, **kwargs):
        instance = CoffeeInstance(self)

        constructor = self._find_method("constructor")
        if constructor:
            bound_constructor = BoundMethod(instance, constructor)
            bound_constructor(*args, **kwargs)

        return instance

    def _find_method(self, name: str):
        if name in self.methods:
            return self.methods[name]
        if self.parent and hasattr(self.parent, "_find_method"):
            return self.parent._find_method(name)
        return None

    def __repr__(self) -> str:
        return f"<class {self.name}>"


class CoffeeInstance:
    def __init__(self, klass: CoffeeClass):
        self.klass = klass
        self.fields: dict[str, object] = {}

    def get(self, name: str):
        if name in self.fields:
            return self.fields[name]

        method = self.klass._find_method(name)
        if method:
            return BoundMethod(self, method)

        raise CoffeeRuntimeError(f"Undefined property '{name}'.")

    def set(self, name: str, value: object) -> None:
        self.fields[name] = value

    def __repr__(self) -> str:
        return f"<{self.klass.name} instance>"


class BoundMethod:
    def __init__(self, instance: CoffeeInstance, method: "CoffeeFunction"):
        self.instance = instance
        self.method = method

    def __call__(self, *args, **kwargs):
        call_env = Environment(parent=self.method.closure)
        call_env.define("this", self.instance)

        if self.method.params and self.method.params[0] == "super":
            if self.instance.klass.parent:
                call_env.define("super", self.instance.klass.parent)

        for index, name in enumerate(self.method.params):
            if name not in ("this", "super"):
                value = args[index] if index < len(args) else None
                call_env.define(name, value)

        for name, value in kwargs.items():
            call_env.define(name, value)

        # Handle @param shorthand - auto-assign this.param = param
        if self.method.this_params:
            for param_name in self.method.this_params:
                param_value = call_env.get(param_name)
                self.instance.set(param_name, param_value)

        previous = self.method.interpreter.environment
        self.method.interpreter.environment = call_env
        try:
            try:
                return self.method.interpreter._evaluate(self.method.body)
            except _ReturnSignal as signal:
                return signal.value
        finally:
            self.method.interpreter.environment = previous


class CoffeeFunction:
    def __init__(self, params: list[str], body, closure: Environment, interpreter: "Interpreter", splat_param: bool = False, defaults: dict = None, this_params: tuple = (), bound: bool = False):
        self.params = params
        self.body = body
        self.closure = closure
        self.interpreter = interpreter
        self.splat_param = splat_param
        self.defaults = defaults if defaults else {}
        self.this_params = this_params
        self.bound = bound
        self.bound_this = None
        if bound:
            try:
                self.bound_this = closure.get("this")
            except CoffeeRuntimeError:
                pass

    def __call__(self, *args, **kwargs):
        call_env = Environment(parent=self.closure)

        if self.bound and self.bound_this is not None:
            call_env.define("this", self.bound_this)

        if self.splat_param and self.params:
            splat_index = len(self.params) - 1
            for index, name in enumerate(self.params[:-1]):
                if index < len(args):
                    value = args[index]
                elif name in kwargs:
                    value = kwargs.pop(name)
                elif name in self.defaults:
                    value = self.interpreter._evaluate(self.defaults[name])
                else:
                    value = None
                call_env.define(name, value)
            splat_name = self.params[-1]
            rest_args = list(args[splat_index:]) if len(args) > splat_index else []
            call_env.define(splat_name, rest_args)
        else:
            for index, name in enumerate(self.params):
                if index < len(args):
                    value = args[index]
                elif name in kwargs:
                    value = kwargs.pop(name)
                elif name in self.defaults:
                    value = self.interpreter._evaluate(self.defaults[name])
                else:
                    value = None
                call_env.define(name, value)

        for name, value in kwargs.items():
            call_env.define(name, value)

        if self.this_params:
            try:
                this_value = call_env.get("this")
                for param_name in self.this_params:
                    param_value = call_env.get(param_name)
                    if isinstance(this_value, CoffeeInstance):
                        this_value.set(param_name, param_value)
            except CoffeeRuntimeError:
                pass

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
        except _BreakSignal:
            raise CoffeeRuntimeError("'break' used outside loop.") from None
        except _ContinueSignal:
            raise CoffeeRuntimeError("'continue' used outside loop.") from None
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

        if isinstance(statement, MultiAssignStmt):
            value = self._evaluate(statement.value)
            for target in statement.targets:
                self._assign_target(target, value)
            return value

        if isinstance(statement, AugAssignStmt):
            current = self._read_target(statement.target)
            right = self._evaluate(statement.value)
            new_value = self._apply_augmented_operator(statement.operator, current, right)
            self._assign_target(statement.target, new_value)
            return new_value

        if isinstance(statement, UpdateStmt):
            current = self._read_target(statement.target)
            new_value = self._apply_update_operator(statement.operator, current)
            self._assign_target(statement.target, new_value)
            return new_value if statement.prefix else current

        if isinstance(statement, ExistentialAssignStmt):
            try:
                current = self._read_target(statement.target)
                if current is None:
                    value = self._evaluate(statement.value)
                    self._assign_target(statement.target, value)
                    return value
                return current
            except CoffeeRuntimeError:
                value = self._evaluate(statement.value)
                self._assign_target(statement.target, value)
                return value

        if isinstance(statement, LogicalAssignStmt):
            current = self._read_target(statement.target)
            if statement.operator == OROR:
                if not current:
                    value = self._evaluate(statement.value)
                    self._assign_target(statement.target, value)
                    return value
                return current
            elif statement.operator == ANDAND:
                if current:
                    value = self._evaluate(statement.value)
                    self._assign_target(statement.target, value)
                    return value
                return current
            raise CoffeeRuntimeError(f"Unknown logical assignment operator: {statement.operator}")

        if isinstance(statement, WhileStmt):
            loop_result = None
            try:
                while self._evaluate(statement.condition):
                    try:
                        loop_result = self._evaluate(statement.body)
                    except _ContinueSignal:
                        continue
            except _BreakSignal:
                pass
            return loop_result

        if isinstance(statement, ForInStmt):
            iterable = self._evaluate(statement.iterable)
            loop_result = None
            try:
                for item in iterable:
                    self.environment.define(statement.var_name, item)
                    try:
                        loop_result = self._evaluate(statement.body)
                    except _ContinueSignal:
                        continue
            except _BreakSignal:
                pass
            return loop_result

        if isinstance(statement, ForOfStmt):
            iterable = self._evaluate(statement.iterable)
            loop_result = None
            try:
                if isinstance(iterable, dict):
                    items = iterable.items()
                else:
                    items = iterable
                for key, value in items:
                    self.environment.define(statement.key_var, key)
                    if statement.value_var:
                        self.environment.define(statement.value_var, value)
                    try:
                        loop_result = self._evaluate(statement.body)
                    except _ContinueSignal:
                        continue
            except _BreakSignal:
                pass
            return loop_result

        if isinstance(statement, BreakStmt):
            raise _BreakSignal()

        if isinstance(statement, ContinueStmt):
            raise _ContinueSignal()

        if isinstance(statement, ClassDecl):
            parent_class = None
            if statement.parent:
                parent_class = self._evaluate(statement.parent)

            methods: dict[str, CoffeeFunction] = {}
            for method_name, method_expr in statement.body:
                if isinstance(method_expr, FunctionLiteral):
                    methods[method_name] = CoffeeFunction(
                        method_expr.params, method_expr.body, self.environment, self,
                        method_expr.splat_param,
                        dict(method_expr.defaults) if method_expr.defaults else {},
                        method_expr.this_params,
                        method_expr.bound
                    )
                else:
                    methods[method_name] = self._evaluate(method_expr)

            klass = CoffeeClass(statement.name, parent_class, methods, self)
            self.environment.define(statement.name, klass)
            return klass

        if isinstance(statement, TryStmt):
            result = None
            try:
                result = self._evaluate(statement.try_block)
            except _ThrowSignal as signal:
                if statement.catch_block:
                    if statement.catch_var:
                        self.environment.define(statement.catch_var, signal.value)
                    result = self._evaluate(statement.catch_block)
                else:
                    raise
            finally:
                if statement.finally_block:
                    self._evaluate(statement.finally_block)
            return result

        if isinstance(statement, ThrowStmt):
            value = self._evaluate(statement.value)
            raise _ThrowSignal(value)

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
            if imported.name == "*":
                alias = imported.alias if imported.alias is not None else statement.module.split(".")[-1]
                self.environment.define(alias, module_obj)
                continue

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

        if isinstance(target, ArrayDestructuring):
            if not hasattr(value, "__iter__"):
                raise CoffeeRuntimeError("Cannot destructure non-iterable value.")
            values = list(value)
            
            splat_idx = target.splat_index
            
            if splat_idx < 0:
                # No splat - simple destructuring
                for i, element in enumerate(target.elements):
                    element_value = values[i] if i < len(values) else None
                    self._assign_target(element, element_value)
            else:
                # With splat - elements before splat get first N values
                # Splat element gets the middle values as a list
                # Elements after splat get the last N values
                
                num_before = splat_idx
                num_after = len(target.elements) - splat_idx - 1
                
                # Assign elements before splat
                for i in range(num_before):
                    element = target.elements[i]
                    element_value = values[i] if i < len(values) else None
                    self._assign_target(element, element_value)
                
                # Assign splat element (middle values)
                splat_start = num_before
                splat_end = len(values) - num_after
                if splat_end < splat_start:
                    splat_end = splat_start
                splat_values = values[splat_start:splat_end]
                self._assign_target(target.elements[splat_idx], splat_values)
                
                # Assign elements after splat (from the end)
                for i, j in enumerate(range(num_after)):
                    element = target.elements[splat_idx + 1 + i]
                    value_idx = len(values) - num_after + j
                    element_value = values[value_idx] if value_idx >= splat_end else None
                    self._assign_target(element, element_value)
            return

        if isinstance(target, ObjectDestructuring):
            if not isinstance(value, dict):
                raise CoffeeRuntimeError("Cannot object-destructure non-object value.")
            for key, alias, default in target.properties:
                if key in value:
                    prop_value = value[key]
                elif default is not None:
                    prop_value = self._evaluate(default)
                else:
                    raise CoffeeRuntimeError(f"Property '{key}' not found in object.")
                if alias is not None:
                    self._assign_target(alias, prop_value)
                else:
                    self.environment.assign(key, prop_value)
            return

        raise CoffeeRuntimeError("Invalid assignment target.")

    def _read_target(self, target):
        if isinstance(target, Identifier):
            return self.environment.get(target.name)

        if isinstance(target, GetAttr):
            container = self._evaluate(target.target)
            return self._get_attr_value(container, target.name)

        if isinstance(target, IndexExpr):
            container = self._evaluate(target.target)
            index = self._evaluate(target.index)
            try:
                return container[index]
            except Exception as exc:
                raise CoffeeRuntimeError(f"Index read failed: {exc}") from exc

        raise CoffeeRuntimeError("Invalid assignment target.")

    @staticmethod
    def _set_attr(container, name: str, value) -> None:
        if isinstance(container, CoffeeInstance):
            container.set(name, value)
            return
        if isinstance(container, dict):
            container[name] = value
            return

        try:
            setattr(container, name, value)
        except Exception as exc:
            raise CoffeeRuntimeError(f"Attribute assignment failed: {exc}") from exc

    @staticmethod
    def _get_attr_value(container, name: str):
        if isinstance(container, CoffeeInstance):
            return container.get(name)
        if isinstance(container, dict) and name in container:
            return container[name]
        if hasattr(container, name):
            return getattr(container, name)
        raise CoffeeRuntimeError(f"Attribute '{name}' not found.")

    def _apply_augmented_operator(self, operator_name: str, left, right):
        try:
            if operator_name == PLUS_EQ:
                return left + right
            if operator_name == MINUS_EQ:
                return left - right
        except Exception as exc:
            raise CoffeeRuntimeError(f"Augmented assignment failed: {exc}") from exc

        raise CoffeeRuntimeError("Unsupported augmented assignment operator.")

    def _apply_update_operator(self, operator_name: str, value):
        try:
            if operator_name == PLUSPLUS:
                return value + 1
            if operator_name == MINUSMINUS:
                return value - 1
        except Exception as exc:
            raise CoffeeRuntimeError(f"Update operator failed: {exc}") from exc

        raise CoffeeRuntimeError("Unsupported update operator.")

    def _evaluate(self, expression):
        if isinstance(expression, Literal):
            value = expression.value
            if isinstance(value, tuple) and len(value) == 3 and value[0] == "regex":
                import re
                pattern, flags_str = value[1], value[2]
                flags = 0
                if "i" in flags_str:
                    flags |= re.IGNORECASE
                if "m" in flags_str:
                    flags |= re.MULTILINE
                if "s" in flags_str:
                    flags |= re.DOTALL
                return re.compile(pattern, flags)
            return value

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
            return CoffeeFunction(expression.params, expression.body, self.environment, self, expression.splat_param, dict(expression.defaults) if expression.defaults else {}, expression.this_params, expression.bound)

        if isinstance(expression, ArrayLiteral):
            return [self._evaluate(item) for item in expression.items]

        if isinstance(expression, ObjectLiteral):
            object_value: dict[str, object] = {}
            for key, value_expr in expression.items:
                object_value[key] = self._evaluate(value_expr)
            return object_value

        if isinstance(expression, RangeLiteral):
            start = self._evaluate(expression.start)
            end = self._evaluate(expression.end)
            step = self._evaluate(expression.step) if expression.step else None
            
            if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
                raise CoffeeRuntimeError("Range bounds must be numbers.")
            
            start_int = int(start)
            end_int = int(end)
            
            if step is not None:
                step_int = int(step)
            elif start_int > end_int:
                step_int = -1
            else:
                step_int = 1
            
            if expression.exclusive:
                if step_int > 0:
                    return list(range(start_int, end_int, step_int))
                else:
                    return list(range(start_int, end_int - 1, step_int))
            else:
                if step_int > 0:
                    return list(range(start_int, end_int + 1, step_int))
                else:
                    return list(range(start_int, end_int - 1, step_int))

        if isinstance(expression, GetAttr):
            target = self._evaluate(expression.target)
            return self._get_attr_value(target, expression.name)

        if isinstance(expression, IndexExpr):
            target = self._evaluate(expression.target)
            index = self._evaluate(expression.index)
            try:
                return target[index]
            except Exception as exc:
                raise CoffeeRuntimeError(f"Index operation failed: {exc}") from exc

        if isinstance(expression, SliceExpr):
            target = self._evaluate(expression.target)
            start = self._evaluate(expression.start) if expression.start else None
            end = self._evaluate(expression.end) if expression.end else None
            
            if start is not None:
                start = int(start)
            if end is not None:
                if expression.exclusive:
                    end = int(end)
                else:
                    end = int(end) + 1
            
            try:
                return target[start:end]
            except Exception as exc:
                raise CoffeeRuntimeError(f"Slice operation failed: {exc}") from exc

        if isinstance(expression, Call):
            callee = self._evaluate(expression.callee)
            
            expanded_args = []
            for arg in expression.args:
                if isinstance(arg, SpreadExpr):
                    spread_value = self._evaluate(arg.value)
                    if spread_value is not None:
                        try:
                            expanded_args.extend(spread_value)
                        except Exception:
                            expanded_args.append(spread_value)
                else:
                    expanded_args.append(self._evaluate(arg))
            
            kwargs = {name: self._evaluate(value_expr) for name, value_expr in expression.kwargs}

            if not callable(callee):
                raise CoffeeRuntimeError("Target is not callable.")

            try:
                return callee(*expanded_args, **kwargs)
            except CoffeeRuntimeError:
                raise
            except Exception as exc:
                raise CoffeeRuntimeError(f"Call failed: {exc}") from exc

        if isinstance(expression, ThisExpr):
            try:
                return self.environment.get("this")
            except CoffeeRuntimeError:
                raise CoffeeRuntimeError("'this' used outside of class method.")

        if isinstance(expression, SuperExpr):
            try:
                return self.environment.get("super")
            except CoffeeRuntimeError:
                raise CoffeeRuntimeError("'super' used outside of class method.")

        if isinstance(expression, NewExpr):
            klass = self._evaluate(expression.class_expr)
            args = [self._evaluate(arg) for arg in expression.args]
            kwargs = {name: self._evaluate(value_expr) for name, value_expr in expression.kwargs}

            if not isinstance(klass, CoffeeClass):
                raise CoffeeRuntimeError("Can only instantiate classes.")

            return klass(*args, **kwargs)

        if isinstance(expression, SwitchExpr):
            if expression.value is not None:
                switch_value = self._evaluate(expression.value)

                for conditions, body in expression.cases:
                    for condition in conditions:
                        cond_value = self._evaluate(condition)
                        if switch_value == cond_value:
                            return self._evaluate(body)

                if expression.default:
                    return self._evaluate(expression.default)

                return None
            else:
                for conditions, body in expression.cases:
                    for condition in conditions:
                        cond_value = self._evaluate(condition)
                        if cond_value:
                            return self._evaluate(body)

                if expression.default:
                    return self._evaluate(expression.default)

                return None

        if isinstance(expression, ExistentialExpr):
            left = self._evaluate(expression.left)
            if left is not None:
                return left
            return self._evaluate(expression.right)

        if isinstance(expression, SafeAccessExpr):
            target = self._evaluate(expression.target)
            if target is None:
                return None
            return self._get_attr_value(target, expression.name)

        if isinstance(expression, ProtoAccessExpr):
            if expression.target is None:
                raise CoffeeRuntimeError("Prototype access '::' requires a target (e.g., Array::map).")
            target = self._evaluate(expression.target)
            if hasattr(target, '_find_method'):
                method = target._find_method(expression.name)
                if method:
                    return method
            if hasattr(target, 'methods') and expression.name in target.methods:
                return target.methods[expression.name]
            if hasattr(target, '__class__'):
                return self._get_attr_value(target.__class__, expression.name)
            raise CoffeeRuntimeError(f"Cannot access prototype of non-class value.")

        if isinstance(expression, SplatExpr):
            return self._evaluate(expression.value)

        if isinstance(expression, InterpolatedString):
            result = ""
            for part in expression.parts:
                value = self._evaluate(part)
                result += str(value) if value is not None else ""
            return result

        if isinstance(expression, InExpr):
            value = self._evaluate(expression.value)
            container = self._evaluate(expression.container)
            try:
                return value in container
            except Exception:
                return False

        if isinstance(expression, OfExpr):
            key = self._evaluate(expression.key)
            container = self._evaluate(expression.container)
            if isinstance(container, dict):
                return key in container
            try:
                return key in container
            except Exception:
                return False

        if isinstance(expression, ComprehensionExpr):
            iterable = self._evaluate(expression.iterable)
            result = []
            for item in iterable:
                self.environment.define(expression.var_name, item)
                if expression.filter_condition:
                    if not self._evaluate(expression.filter_condition):
                        continue
                result.append(self._evaluate(expression.body))
            return result

        if isinstance(expression, ObjectComprehensionExpr):
            iterable = self._evaluate(expression.iterable)
            result = {}
            
            if isinstance(iterable, dict):
                items = list(iterable.items())
            else:
                items = [(i, item) for i, item in enumerate(iterable)]
            
            for key, value in items:
                self.environment.define(expression.key_var, key)
                if expression.value_var:
                    self.environment.define(expression.value_var, value)
                
                if expression.filter_condition:
                    if not self._evaluate(expression.filter_condition):
                        continue
                
                result_key = self._evaluate(expression.key_expr)
                result_value = self._evaluate(expression.value_expr)
                result[result_key] = result_value
            
            return result

        if isinstance(expression, SpreadExpr):
            return self._evaluate(expression.value)

        if isinstance(expression, DoExpr):
            func = self._evaluate(expression.body)
            if not callable(func):
                raise CoffeeRuntimeError("'do' requires a callable expression.")
            return func()

        if isinstance(expression, YieldExpr):
            raise CoffeeRuntimeError("'yield' used outside generator function.")

        if isinstance(expression, ChainedComparison):
            for i in range(len(expression.operators)):
                left = self._evaluate(expression.operands[i])
                right = self._evaluate(expression.operands[i + 1])
                op = expression.operators[i]
                
                if op == LT and not (left < right):
                    return False
                if op == LTE and not (left <= right):
                    return False
                if op == GT and not (left > right):
                    return False
                if op == GTE and not (left >= right):
                    return False
            return True

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
