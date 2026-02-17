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
class AugAssignStmt(Statement):
    target: Expression
    operator: str
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
