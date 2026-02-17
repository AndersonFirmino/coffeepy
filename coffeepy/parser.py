from __future__ import annotations

from .ast_nodes import (
    ArrayLiteral,
    AssignStmt,
    AugAssignStmt,
    Binary,
    BlockExpr,
    Call,
    ExprStmt,
    Expression,
    FromImportStmt,
    FunctionLiteral,
    GetAttr,
    Identifier,
    IfExpr,
    ImportItem,
    ImportName,
    ImportStmt,
    IndexExpr,
    Literal,
    ObjectLiteral,
    Program,
    ReturnStmt,
    Statement,
    Unary,
    UpdateStmt,
    WhileStmt,
)
from .errors import CoffeeParseError
from .tokens import (
    AND,
    ARROW,
    AS,
    COLON,
    COMMA,
    DOT,
    ELSE,
    EOF,
    EQ,
    EQEQ,
    FALSE,
    FROM,
    GT,
    GTE,
    IDENT,
    IF,
    IMPORT,
    INDENT,
    LBRACE,
    LBRACKET,
    LPAREN,
    LT,
    LTE,
    MINUS,
    MINUSMINUS,
    MINUS_EQ,
    NEQ,
    NEWLINE,
    NOT,
    NULL,
    NUMBER,
    OR,
    OUTDENT,
    PERCENT,
    PLUS,
    PLUSPLUS,
    PLUS_EQ,
    RBRACE,
    RBRACKET,
    RETURN,
    RPAREN,
    SEMICOLON,
    SLASH,
    STAR,
    STARSTAR,
    STRING,
    THEN,
    TRUE,
    Token,
    UNDEFINED,
    UNTIL,
    UNLESS,
    WHILE,
)


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        statements: list[Statement] = []
        self._consume_statement_breaks()

        while not self._is_at_end():
            statements.append(self._statement())
            self._consume_statement_breaks()

        return Program(statements)

    def _statement(self) -> Statement:
        if self._match(IMPORT):
            return self._import_statement()

        if self._match(FROM):
            return self._from_import_statement()

        if self._match(RETURN):
            if self._check(NEWLINE, SEMICOLON, OUTDENT, EOF):
                return ReturnStmt(None)
            return ReturnStmt(self._expression())

        if self._match(WHILE, UNTIL):
            is_until = self._previous().kind == UNTIL
            condition = self._logical_or()
            if is_until:
                condition = Unary(NOT, condition)
            body = self._parse_clause_body()
            return WhileStmt(condition, body)

        assignment = self._maybe_assignment_or_update_statement()
        if assignment is not None:
            return assignment

        return ExprStmt(self._expression())

    def _maybe_assignment_or_update_statement(self) -> Statement | None:
        checkpoint = self.current

        if self._match(PLUSPLUS, MINUSMINUS):
            operator = self._previous().kind
            target = self._parse_assignment_target()
            if target is None:
                raise self._error(self._peek(), "Expected assignment target after update operator.")
            return UpdateStmt(target, operator, prefix=True)

        checkpoint = self.current
        target = self._parse_assignment_target()
        if target is None:
            self.current = checkpoint
            return None

        if self._match(EQ):
            value = self._expression()
            return AssignStmt(target, value)

        if self._match(PLUS_EQ, MINUS_EQ):
            operator = self._previous().kind
            value = self._expression()
            return AugAssignStmt(target, operator, value)

        if self._match(PLUSPLUS, MINUSMINUS):
            operator = self._previous().kind
            return UpdateStmt(target, operator, prefix=False)

        self.current = checkpoint
        return None

    def _parse_assignment_target(self) -> Expression | None:
        if not self._match(IDENT):
            return None

        target: Expression = Identifier(self._previous().lexeme)

        while True:
            if self._match(DOT):
                name = self._consume(IDENT, "Expected property name after '.'.").lexeme
                target = GetAttr(target, name)
                continue

            if self._match(LBRACKET):
                index = self._expression()
                self._consume(RBRACKET, "Expected ']' after index expression.")
                target = IndexExpr(target, index)
                continue

            break

        return target

    def _import_statement(self) -> ImportStmt:
        items = [self._import_item()]
        while self._match(COMMA):
            items.append(self._import_item())
        return ImportStmt(items)

    def _import_item(self) -> ImportItem:
        module = self._module_path()
        alias: str | None = None
        if self._match(AS):
            alias = self._consume(IDENT, "Expected identifier after 'as'.").lexeme
        return ImportItem(module, alias)

    def _from_import_statement(self) -> FromImportStmt:
        module = self._module_path()
        self._consume(IMPORT, "Expected 'import' in from-import statement.")

        names = [self._import_name()]
        while self._match(COMMA):
            names.append(self._import_name())

        return FromImportStmt(module, names)

    def _import_name(self) -> ImportName:
        name = self._consume(IDENT, "Expected imported name.").lexeme
        alias: str | None = None
        if self._match(AS):
            alias = self._consume(IDENT, "Expected alias name after 'as'.").lexeme
        return ImportName(name, alias)

    def _module_path(self) -> str:
        token = self._consume(IDENT, "Expected module path.")
        module = token.lexeme
        while self._match(DOT):
            part = self._consume(IDENT, "Expected module segment after '.'.").lexeme
            module += f".{part}"
        return module

    def _expression(self) -> Expression:
        return self._if_expression()

    def _if_expression(self) -> Expression:
        if self._match(IF, UNLESS):
            is_unless = self._previous().kind == UNLESS
            condition = self._logical_or()
            if is_unless:
                condition = Unary(NOT, condition)

            then_branch = self._parse_clause_body()
            else_branch: Expression = Literal(None)

            if self._match_else_marker():
                else_branch = self._parse_clause_body()

            return IfExpr(condition, then_branch, else_branch)

        expr = self._logical_or()
        if self._can_take_postfix_if():
            is_unless = self._advance().kind == UNLESS
            condition = self._logical_or()
            if is_unless:
                condition = Unary(NOT, condition)
            return IfExpr(condition, expr, Literal(None))

        return expr

    def _parse_clause_body(self) -> Expression:
        if self._match(THEN):
            return self._if_expression()

        if self._match(NEWLINE):
            self._consume_statement_breaks()
            if self._match(INDENT):
                return self._parse_indented_block_expression()
            raise self._error(self._peek(), "Expected indented block.")

        return self._if_expression()

    def _parse_indented_block_expression(self) -> Expression:
        statements: list[Statement] = []
        self._consume_statement_breaks()

        while not self._check(OUTDENT, EOF):
            statements.append(self._statement())
            self._consume_statement_breaks()

        self._consume(OUTDENT, "Expected end of indented block.")
        return BlockExpr(statements)

    def _match_else_marker(self) -> bool:
        if self._match(ELSE):
            return True

        checkpoint = self.current
        if self._match(NEWLINE):
            self._consume_statement_breaks()
            if self._match(ELSE):
                return True

        self.current = checkpoint
        return False

    def _logical_or(self) -> Expression:
        expr = self._logical_and()
        while self._match(OR):
            operator = self._previous().kind
            right = self._logical_and()
            expr = Binary(expr, operator, right)
        return expr

    def _logical_and(self) -> Expression:
        expr = self._equality()
        while self._match(AND):
            operator = self._previous().kind
            right = self._equality()
            expr = Binary(expr, operator, right)
        return expr

    def _equality(self) -> Expression:
        expr = self._comparison()
        while self._match(EQEQ, NEQ):
            operator = self._previous().kind
            right = self._comparison()
            expr = Binary(expr, operator, right)
        return expr

    def _comparison(self) -> Expression:
        expr = self._additive()
        while self._match(LT, LTE, GT, GTE):
            operator = self._previous().kind
            right = self._additive()
            expr = Binary(expr, operator, right)
        return expr

    def _additive(self) -> Expression:
        expr = self._multiplicative()
        while self._match(PLUS, MINUS):
            operator = self._previous().kind
            right = self._multiplicative()
            expr = Binary(expr, operator, right)
        return expr

    def _multiplicative(self) -> Expression:
        expr = self._power()
        while self._match(STAR, SLASH, PERCENT):
            operator = self._previous().kind
            right = self._power()
            expr = Binary(expr, operator, right)
        return expr

    def _power(self) -> Expression:
        expr = self._unary()
        if self._match(STARSTAR):
            operator = self._previous().kind
            right = self._power()
            expr = Binary(expr, operator, right)
        return expr

    def _unary(self) -> Expression:
        if self._match(NOT, MINUS, PLUS):
            operator = self._previous().kind
            right = self._unary()
            return Unary(operator, right)
        return self._call()

    def _call(self) -> Expression:
        expr = self._primary()

        while True:
            if self._match(DOT):
                name = self._consume(IDENT, "Expected property name after '.'.").lexeme
                expr = GetAttr(expr, name)
                continue

            if self._match(LBRACKET):
                index = self._expression()
                self._consume(RBRACKET, "Expected ']' after index expression.")
                expr = IndexExpr(expr, index)
                continue

            if self._match(LPAREN):
                args, kwargs = self._argument_list()
                expr = Call(expr, args, kwargs, implicit=False)
                continue

            if self._can_parse_implicit_call(expr):
                args = [self._if_expression()]
                while self._match(COMMA):
                    args.append(self._if_expression())
                expr = Call(expr, args, [], implicit=True)
                continue

            break

        return expr

    def _argument_list(self) -> tuple[list[Expression], list[tuple[str, Expression]]]:
        args: list[Expression] = []
        kwargs: list[tuple[str, Expression]] = []

        if self._match(RPAREN):
            return args, kwargs

        seen_kwargs = False
        while True:
            name, value = self._parse_call_argument()
            if name is None:
                if seen_kwargs:
                    raise self._error(self._peek(), "Positional argument after keyword argument.")
                args.append(value)
            else:
                seen_kwargs = True
                kwargs.append((name, value))

            if not self._match(COMMA):
                break

        self._consume(RPAREN, "Expected ')' after arguments.")
        return args, kwargs

    def _parse_call_argument(self) -> tuple[str | None, Expression]:
        if self._check(IDENT) and self._check_next(EQ):
            name = self._advance().lexeme
            self._consume(EQ, "Expected '=' after keyword argument name.")
            return name, self._if_expression()
        return None, self._if_expression()

    def _primary(self) -> Expression:
        if self._check(IDENT) and self._check_next(ARROW):
            name = self._advance().lexeme
            self._consume(ARROW, "Expected '->' in function literal.")
            body = self._parse_function_body()
            return FunctionLiteral([name], body)

        if self._match(ARROW):
            body = self._parse_function_body()
            return FunctionLiteral([], body)

        if self._match(NUMBER):
            return Literal(self._previous().literal)

        if self._match(STRING):
            return Literal(self._previous().literal)

        if self._match(TRUE):
            return Literal(True)

        if self._match(FALSE):
            return Literal(False)

        if self._match(NULL, UNDEFINED):
            return Literal(None)

        if self._match(IDENT):
            return Identifier(self._previous().lexeme)

        if self._match(LBRACKET):
            return self._array_literal()

        if self._match(LBRACE):
            return self._object_literal()

        if self._match(LPAREN):
            checkpoint = self.current
            fn_literal = self._try_parse_parenthesized_function_literal()
            if fn_literal is not None:
                return fn_literal

            self.current = checkpoint
            expr = self._expression()
            self._consume(RPAREN, "Expected ')' after expression.")
            return expr

        token = self._peek()
        raise self._error(token, "Expected expression.")

    def _parse_function_body(self) -> Expression:
        if self._match(NEWLINE):
            self._consume_statement_breaks()
            self._consume(INDENT, "Expected indented function body.")
            return self._parse_indented_block_expression()

        return self._if_expression()

    def _try_parse_parenthesized_function_literal(self) -> FunctionLiteral | None:
        params: list[str] = []

        if self._match(RPAREN):
            if not self._match(ARROW):
                return None
            body = self._parse_function_body()
            return FunctionLiteral(params, body)

        if not self._check(IDENT):
            return None

        params.append(self._advance().lexeme)
        while self._match(COMMA):
            if not self._check(IDENT):
                return None
            params.append(self._advance().lexeme)

        if not self._match(RPAREN):
            return None
        if not self._match(ARROW):
            return None

        body = self._parse_function_body()
        return FunctionLiteral(params, body)

    def _array_literal(self) -> ArrayLiteral:
        items: list[Expression] = []
        if self._match(RBRACKET):
            return ArrayLiteral(items)

        items.append(self._expression())
        while self._match(COMMA):
            if self._check(RBRACKET):
                break
            items.append(self._expression())

        self._consume(RBRACKET, "Expected ']' after array literal.")
        return ArrayLiteral(items)

    def _object_literal(self) -> ObjectLiteral:
        items: list[tuple[str, Expression]] = []
        if self._match(RBRACE):
            return ObjectLiteral(items)

        key = self._object_key()
        self._consume(COLON, "Expected ':' after object key.")
        value = self._expression()
        items.append((key, value))

        while self._match(COMMA):
            if self._check(RBRACE):
                break
            key = self._object_key()
            self._consume(COLON, "Expected ':' after object key.")
            value = self._expression()
            items.append((key, value))

        self._consume(RBRACE, "Expected '}' after object literal.")
        return ObjectLiteral(items)

    def _object_key(self) -> str:
        if self._match(IDENT):
            return self._previous().lexeme
        if self._match(STRING):
            literal = self._previous().literal
            if not isinstance(literal, str):
                raise self._error(self._previous(), "Object key must be a string.")
            return literal
        raise self._error(self._peek(), "Expected object key.")

    def _can_parse_implicit_call(self, expr: Expression) -> bool:
        if not isinstance(expr, (Identifier, GetAttr, IndexExpr, Call)):
            return False

        if self._check(
            NEWLINE,
            EOF,
            RPAREN,
            RBRACKET,
            RBRACE,
            COMMA,
            SEMICOLON,
            THEN,
            ELSE,
            OUTDENT,
            EQ,
            EQEQ,
            NEQ,
            LT,
            LTE,
            GT,
            GTE,
            COLON,
        ):
            return False

        return self._check(
            NUMBER,
            STRING,
            IDENT,
            TRUE,
            FALSE,
            NULL,
            UNDEFINED,
            LPAREN,
            LBRACKET,
            LBRACE,
            NOT,
            IF,
            UNLESS,
            ARROW,
        )

    def _consume_statement_breaks(self) -> None:
        while self._match(NEWLINE, SEMICOLON):
            pass

    def _can_take_postfix_if(self) -> bool:
        if not self._check(IF, UNLESS):
            return False

        token = self._peek()
        return token.column > 1

    def _match(self, *kinds: str) -> bool:
        for kind in kinds:
            if self._check(kind):
                self._advance()
                return True
        return False

    def _consume(self, kind: str, message: str) -> Token:
        if self._check(kind):
            return self._advance()
        raise self._error(self._peek(), message)

    def _check(self, *kinds: str) -> bool:
        if self._is_at_end():
            return EOF in kinds
        return self._peek().kind in kinds

    def _check_next(self, kind: str) -> bool:
        if self.current + 1 >= len(self.tokens):
            return False
        return self.tokens[self.current + 1].kind == kind

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self.tokens[self.current - 1]

    def _is_at_end(self) -> bool:
        return self._peek().kind == EOF

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]

    @staticmethod
    def _error(token: Token, message: str) -> CoffeeParseError:
        return CoffeeParseError(f"{message} (line {token.line}, column {token.column})")
