from __future__ import annotations

from dataclasses import dataclass


class Statement:
    pass


class Expression:
    pass


@dataclass(frozen=True)
class Program:
    statements: list[Statement]


@dataclass(frozen=True)
class ImportItem:
    module: str
    alias: str | None


@dataclass(frozen=True)
class ImportName:
    name: str
    alias: str | None


@dataclass(frozen=True)
class ImportStmt(Statement):
    items: list[ImportItem]


@dataclass(frozen=True)
class FromImportStmt(Statement):
    module: str
    names: list[ImportName]


@dataclass(frozen=True)
class AssignStmt(Statement):
    target: Expression
    value: Expression


@dataclass(frozen=True)
class ReturnStmt(Statement):
    value: Expression | None


@dataclass(frozen=True)
class WhileStmt(Statement):
    condition: Expression
    body: Expression


@dataclass(frozen=True)
class BreakStmt(Statement):
    pass


@dataclass(frozen=True)
class ContinueStmt(Statement):
    pass


@dataclass(frozen=True)
class ForInStmt(Statement):
    var_name: str
    iterable: Expression
    body: Expression


@dataclass(frozen=True)
class ForOfStmt(Statement):
    key_var: str
    value_var: str | None
    iterable: Expression
    body: Expression


@dataclass(frozen=True)
class RangeLiteral(Expression):
    start: Expression
    end: Expression
    exclusive: bool
    step: Expression | None = None


@dataclass(frozen=True)
class DoExpr(Expression):
    body: Expression


@dataclass(frozen=True)
class YieldExpr(Expression):
    value: Expression | None


@dataclass(frozen=True)
class ChainedComparison(Expression):
    operands: list[Expression]
    operators: list[str]


@dataclass(frozen=True)
class ImportAllStmt(Statement):
    module: str
    alias: str | None


@dataclass(frozen=True)
class GetterDecl(Statement):
    name: str
    body: Expression


@dataclass(frozen=True)
class SetterDecl(Statement):
    name: str
    param: str
    body: Expression


@dataclass(frozen=True)
class AugAssignStmt(Statement):
    target: Expression
    operator: str
    value: Expression


@dataclass(frozen=True)
class ExistentialAssignStmt(Statement):
    target: Expression
    value: Expression


@dataclass(frozen=True)
class UpdateStmt(Statement):
    target: Expression
    operator: str
    prefix: bool


@dataclass(frozen=True)
class ExprStmt(Statement):
    expression: Expression


@dataclass(frozen=True)
class BlockExpr(Expression):
    statements: list[Statement]


@dataclass(frozen=True)
class Literal(Expression):
    value: object


@dataclass(frozen=True)
class Identifier(Expression):
    name: str


@dataclass(frozen=True)
class Unary(Expression):
    operator: str
    right: Expression


@dataclass(frozen=True)
class Binary(Expression):
    left: Expression
    operator: str
    right: Expression


@dataclass(frozen=True)
class IfExpr(Expression):
    condition: Expression
    then_branch: Expression
    else_branch: Expression


@dataclass(frozen=True)
class GetAttr(Expression):
    target: Expression
    name: str


@dataclass(frozen=True)
class Call(Expression):
    callee: Expression
    args: list[Expression]
    kwargs: list[tuple[str, Expression]]
    implicit: bool = False


@dataclass(frozen=True)
class FunctionLiteral(Expression):
    params: list[str]
    body: Expression
    splat_param: bool = False
    defaults: dict = None
    this_params: tuple = ()
    bound: bool = False
    
    def __post_init__(self):
        if self.defaults is None:
            object.__setattr__(self, 'defaults', {})


@dataclass(frozen=True)
class ArrayLiteral(Expression):
    items: list[Expression]


@dataclass(frozen=True)
class ObjectLiteral(Expression):
    items: list[tuple[str, Expression]]


@dataclass(frozen=True)
class IndexExpr(Expression):
    target: Expression
    index: Expression


@dataclass(frozen=True)
class SliceExpr(Expression):
    target: Expression
    start: Expression | None
    end: Expression | None
    exclusive: bool = False


@dataclass(frozen=True)
class ArrayDestructuring(Expression):
    elements: list[Expression]
    splat_index: int = -1  # -1 means no splat


@dataclass(frozen=True)
class ObjectDestructuring(Expression):
    properties: list[tuple[str, Expression | None, Expression | None]]  # (key, alias, default)


@dataclass(frozen=True)
class ClassDecl(Statement):
    name: str
    parent: Expression | None
    body: list[tuple[str, Expression]]


@dataclass(frozen=True)
class ThisExpr(Expression):
    pass


@dataclass(frozen=True)
class SuperExpr(Expression):
    pass


@dataclass(frozen=True)
class NewExpr(Expression):
    class_expr: Expression
    args: list[Expression]
    kwargs: list[tuple[str, Expression]]


@dataclass(frozen=True)
class TryStmt(Statement):
    try_block: Expression
    catch_var: str | None
    catch_block: Expression | None
    finally_block: Expression | None


@dataclass(frozen=True)
class ThrowStmt(Statement):
    value: Expression


@dataclass(frozen=True)
class SwitchExpr(Expression):
    value: Expression
    cases: list[tuple[list[Expression], Expression]]
    default: Expression | None


@dataclass(frozen=True)
class ExistentialExpr(Expression):
    left: Expression
    right: Expression


@dataclass(frozen=True)
class SafeAccessExpr(Expression):
    target: Expression
    name: str


@dataclass(frozen=True)
class SplatExpr(Expression):
    value: Expression


@dataclass(frozen=True)
class InterpolatedString(Expression):
    parts: list[Expression]


@dataclass(frozen=True)
class InExpr(Expression):
    value: Expression
    container: Expression


@dataclass(frozen=True)
class OfExpr(Expression):
    key: Expression
    container: Expression


@dataclass(frozen=True)
class ComprehensionExpr(Expression):
    var_name: str
    iterable: Expression
    body: Expression
    filter_condition: Expression | None = None


@dataclass(frozen=True)
class ObjectComprehensionExpr(Expression):
    key_expr: Expression
    value_expr: Expression
    key_var: str
    value_var: str | None
    iterable: Expression
    filter_condition: Expression | None = None


@dataclass(frozen=True)
class SpreadExpr(Expression):
    value: Expression
