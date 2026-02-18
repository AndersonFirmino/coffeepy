from __future__ import annotations

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
    GetterDecl,
    Identifier,
    IfExpr,
    ImportAllStmt,
    ImportItem,
    ImportName,
    ImportStmt,
    InExpr,
    IndexExpr,
    InterpolatedString,
    Literal,
    LogicalAssignStmt,
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
    SetterDecl,
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
from .errors import CoffeeParseError
from .tokens import (
    AND,
    ANDAND,
    ANDAND_EQ,
    ARROW,
    AS,
    AT,
    BREAK,
    BY,
    CATCH,
    CLASS,
    COLON,
    COMMA,
    CONTINUE,
    DO,
    DOT,
    DOTDOT,
    DOTDOTDOT,
    ELSE,
    EOF,
    EQ,
    EQEQ,
    EXTENDS,
    FAT_ARROW,
    FALSE,
    FINALLY,
    FOR,
    FROM,
    GET,
    GT,
    GTE,
    IDENT,
    IF,
    IMPORT,
    IN,
    INDENT,
    IS,
    ISNT,
    LBRACE,
    LBRACKET,
    LPAREN,
    LT,
    LTE,
    MINUS,
    MINUSMINUS,
    MINUS_EQ,
    NEQ,
    NEW,
    NEWLINE,
    NOT,
    NULL,
    NUMBER,
    OF,
    OR,
    OROR,
    OROR_EQ,
    OUTDENT,
    PERCENT,
    PLUS,
    PLUSPLUS,
    PLUS_EQ,
    PROTO,
    QUESTION,
    QUESTIONDOT,
    QUESTIONEQ,
    RBRACE,
    RBRACKET,
    RETURN,
    RPAREN,
    SEMICOLON,
    SET,
    SLASH,
    STAR,
    STARSTAR,
    STRING,
    SUPER,
    SWITCH,
    THEN,
    THIS,
    THROW,
    TRUE,
    TRY,
    Token,
    UNDEFINED,
    UNTIL,
    UNLESS,
    WHEN,
    WHILE,
    YIELD,
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

        if self._match(BREAK):
            return BreakStmt()

        if self._match(CONTINUE):
            return ContinueStmt()

        if self._match(THROW):
            value = self._expression()
            return ThrowStmt(value)

        if self._match(YIELD):
            if self._check(NEWLINE, SEMICOLON, OUTDENT, EOF):
                return ExprStmt(YieldExpr(None))
            return ExprStmt(YieldExpr(self._expression()))

        if self._match(TRY):
            return self._try_statement()

        if self._match(WHILE, UNTIL):
            is_until = self._previous().kind == UNTIL
            condition = self._logical_or()
            if is_until:
                condition = Unary(NOT, condition)
            body = self._parse_clause_body()
            return WhileStmt(condition, body)

        if self._match(FOR):
            return self._for_in_statement()

        if self._match(CLASS):
            return self._class_declaration()

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

        if self._match(QUESTIONEQ):
            value = self._expression()
            return ExistentialAssignStmt(target, value)

        if self._match(PLUS_EQ, MINUS_EQ):
            operator = self._previous().kind
            value = self._expression()
            return AugAssignStmt(target, operator, value)

        if self._match(OROR_EQ):
            value = self._expression()
            return LogicalAssignStmt(target, OROR, value)

        if self._match(ANDAND_EQ):
            value = self._expression()
            return LogicalAssignStmt(target, ANDAND, value)

        if self._match(PLUSPLUS, MINUSMINUS):
            operator = self._previous().kind
            return UpdateStmt(target, operator, prefix=False)

        self.current = checkpoint
        return None

    def _parse_assignment_target(self) -> Expression | None:
        if self._check(LBRACKET):
            checkpoint = self.current
            self._advance()
            result = self._try_parse_array_destructuring_target()
            if result is None:
                self.current = checkpoint
                return None
            return result

        if self._check(LBRACE):
            checkpoint = self.current
            self._advance()
            result = self._try_parse_object_destructuring_target()
            if result is None:
                self.current = checkpoint
                return None
            return result

        if self._match(AT):
            prop_name = self._consume(IDENT, "Expected property name after '@'.").lexeme
            target: Expression = GetAttr(ThisExpr(), prop_name)
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

        if self._match(THIS):
            if not self._match(DOT):
                return None
            prop_name = self._consume(IDENT, "Expected property name after 'this.'.").lexeme
            target = GetAttr(ThisExpr(), prop_name)
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

        if not self._match(IDENT):
            return None

        target = Identifier(self._previous().lexeme)

        while True:
            if self._match(DOT):
                name = self._consume(IDENT, "Expected property name after '.'.").lexeme
                target = GetAttr(target, name)
                continue

            if self._match(LBRACKET):
                target = self._parse_index_or_slice_for_target(target)
                continue

            break

        return target

    def _parse_index_or_slice_for_target(self, target: Expression) -> Expression:
        if self._check(DOTDOT, DOTDOTDOT):
            start = None
            if self._match(DOTDOT):
                exclusive = False
            else:
                self._advance()
                exclusive = True
            if not self._check(RBRACKET):
                end = self._additive()
            else:
                end = None
            self._consume(RBRACKET, "Expected ']' after slice.")
            return SliceExpr(target, None, end, exclusive)
        
        index = self._additive()
        
        if self._match(DOTDOT):
            if not self._check(RBRACKET):
                end = self._additive()
            else:
                end = None
            self._consume(RBRACKET, "Expected ']' after slice.")
            return SliceExpr(target, index, end, exclusive=False)
        
        if self._match(DOTDOTDOT):
            if not self._check(RBRACKET):
                end = self._additive()
            else:
                end = None
            self._consume(RBRACKET, "Expected ']' after slice.")
            return SliceExpr(target, index, end, exclusive=True)
        
        if self._match(COMMA):
            self._consume(RBRACKET, "Expected ']' after index.")
            return IndexExpr(target, index)
        
        self._consume(RBRACKET, "Expected ']' after index expression.")
        return IndexExpr(target, index)

    def _try_parse_array_destructuring_target(self) -> ArrayDestructuring | None:
        elements: list[Expression] = []
        splat_index = -1

        if not self._check(RBRACKET):
            element, is_splat = self._try_parse_destructuring_element_with_splat()
            if element is None:
                return None
            elements.append(element)
            if is_splat:
                splat_index = 0
            
            while self._match(COMMA):
                if self._check(RBRACKET):
                    break
                element, is_splat = self._try_parse_destructuring_element_with_splat()
                if element is None:
                    return None
                elements.append(element)
                if is_splat:
                    if splat_index >= 0:
                        raise self._error(self._previous(), "Only one splat allowed in destructuring.")
                    splat_index = len(elements) - 1

        if not self._match(RBRACKET):
            return None
        return ArrayDestructuring(elements, splat_index)

    def _try_parse_destructuring_element_with_splat(self) -> tuple[Expression | None, bool]:
        if self._check(LBRACKET):
            checkpoint = self.current
            self._advance()
            result = self._try_parse_array_destructuring_target()
            if result is not None:
                return result, False
            self.current = checkpoint
            return None, False

        if self._check(LBRACE):
            checkpoint = self.current
            self._advance()
            result = self._try_parse_object_destructuring_target()
            if result is not None:
                return result, False
            self.current = checkpoint
            return None, False

        if self._match(IDENT):
            ident = Identifier(self._previous().lexeme)
            if self._match(DOTDOTDOT):
                return ident, True
            return ident, False

        return None, False

    def _try_parse_object_destructuring_target(self) -> ObjectDestructuring | None:
        properties: list[tuple[str, Expression | None, Expression | None]] = []

        if not self._check(RBRACE):
            result = self._try_parse_object_destructuring_property()
            if result is None:
                return None
            key, alias, default = result
            properties.append((key, alias, default))
            while self._match(COMMA):
                if self._check(RBRACE):
                    break
                result = self._try_parse_object_destructuring_property()
                if result is None:
                    return None
                key, alias, default = result
                properties.append((key, alias, default))

        if not self._match(RBRACE):
            return None
        return ObjectDestructuring(properties)

    def _try_parse_destructuring_element(self) -> Expression | None:
        if self._check(LBRACKET):
            checkpoint = self.current
            self._advance()
            result = self._try_parse_array_destructuring_target()
            if result is not None:
                return result
            self.current = checkpoint
            return None

        if self._check(LBRACE):
            checkpoint = self.current
            self._advance()
            result = self._try_parse_object_destructuring_target()
            if result is not None:
                return result
            self.current = checkpoint
            return None

        if self._match(IDENT):
            return Identifier(self._previous().lexeme)

        return None

    def _try_parse_object_destructuring_property(self) -> tuple[str, Expression | None, Expression | None] | None:
        if not self._match(IDENT):
            return None
        key = self._previous().lexeme
        alias: Expression | None = None
        default: Expression | None = None
        
        if self._match(COLON):
            if not self._match(IDENT):
                return None
            alias = Identifier(self._previous().lexeme)
        
        if self._match(EQ):
            default = self._logical_or()
        
        return key, alias, default

    def _for_in_statement(self) -> Statement:
        first_var = self._consume(IDENT, "Expected loop variable after 'for'.").lexeme

        second_var: str | None = None
        if self._match(COMMA):
            second_var = self._consume(IDENT, "Expected variable after ','.").lexeme

        if self._match(IN):
            iterable = self._expression()
            body = self._parse_clause_body()
            return ForInStmt(first_var, iterable, body)

        if self._match(OF):
            iterable = self._expression()
            body = self._parse_clause_body()
            return ForOfStmt(first_var, second_var, iterable, body)

        raise self._error(self._peek(), "Expected 'in' or 'of' in for-loop.")

    def _class_declaration(self) -> ClassDecl:
        name_token = self._consume(IDENT, "Expected class name.")
        name = name_token.lexeme

        parent: Expression | None = None
        if self._match(EXTENDS):
            parent = self._expression()

        body: list[tuple[str, Expression]] = []

        if self._match(NEWLINE):
            self._consume_statement_breaks()
            if self._match(INDENT):
                while not self._check(OUTDENT, EOF):
                    method_name_token = self._consume(IDENT, "Expected method name.")
                    method_name = method_name_token.lexeme
                    self._consume(COLON, "Expected ':' after method name.")
                    method_value = self._expression()
                    body.append((method_name, method_value))
                    self._consume_statement_breaks()
                self._consume(OUTDENT, "Expected end of class body.")

        return ClassDecl(name, parent, body)

    def _try_statement(self) -> TryStmt:
        try_block = self._parse_clause_body()

        catch_var: str | None = None
        catch_block: Expression | None = None
        if self._match(CATCH):
            if self._match(IDENT):
                catch_var = self._previous().lexeme
            catch_block = self._parse_clause_body()

        finally_block: Expression | None = None
        if self._match(FINALLY):
            finally_block = self._parse_clause_body()

        return TryStmt(try_block, catch_var, catch_block, finally_block)

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

        if self._match(STAR):
            alias: str | None = None
            if self._match(AS):
                alias = self._consume(IDENT, "Expected identifier after 'as'.").lexeme
            return FromImportStmt(module, [ImportName("*", alias)])

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
        return self._switch_expression()

    def _switch_expression(self) -> Expression:
        if self._match(SWITCH):
            value = self._expression()
            cases: list[tuple[list[Expression], Expression]] = []
            default: Expression | None = None

            self._consume_statement_breaks()
            self._consume(INDENT, "Expected indented block after switch.")

            while not self._check(OUTDENT, EOF):
                if self._match(WHEN):
                    conditions = [self._expression()]
                    while self._match(COMMA):
                        conditions.append(self._expression())
                    body = self._parse_clause_body()
                    cases.append((conditions, body))
                elif self._match(ELSE):
                    default = self._parse_clause_body()
                else:
                    raise self._error(self._peek(), "Expected 'when' or 'else' in switch.")
                self._consume_statement_breaks()

            self._consume(OUTDENT, "Expected end of switch block.")
            return SwitchExpr(value, cases, default)

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
        expr = self._existential()
        while self._match(OR):
            operator = self._previous().kind
            right = self._existential()
            expr = Binary(expr, operator, right)
        return expr

    def _existential(self) -> Expression:
        expr = self._logical_and()
        while self._match(QUESTION):
            right = self._logical_and()
            expr = ExistentialExpr(expr, right)
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
        while self._match(EQEQ, NEQ, IS, ISNT):
            operator = self._previous().kind
            if operator == IS:
                if self._match(NOT):
                    operator = NEQ
                else:
                    operator = EQEQ
            elif operator == ISNT:
                operator = NEQ
            right = self._comparison()
            expr = Binary(expr, operator, right)
        return expr

    def _comparison(self) -> Expression:
        operands = [self._range()]
        operators = []
        
        while self._match(LT, LTE, GT, GTE):
            operator = self._previous().kind
            operators.append(operator)
            operands.append(self._range())
        
        if len(operators) == 0:
            expr = operands[0]
        elif len(operators) == 1:
            expr = Binary(operands[0], operators[0], operands[1])
        else:
            expr = ChainedComparison(operands, operators)
        
        if self._match(IN):
            right = self._range()
            expr = InExpr(expr, right)
        
        if self._match(OF):
            right = self._range()
            expr = OfExpr(expr, right)
        
        return expr

    def _range(self) -> Expression:
        expr = self._additive()
        if self._match(DOTDOT):
            end = self._additive()
            step = None
            if self._match(BY):
                step = self._additive()
            return RangeLiteral(expr, end, exclusive=False, step=step)
        if self._check(DOTDOTDOT):
            next_is_end = (self._check_next(RPAREN) or self._check_next(COMMA) or 
                          self._check_next(NEWLINE) or self._check_next(OUTDENT) or 
                          self._check_next(EOF))
            if not next_is_end:
                self._advance()
                end = self._additive()
                step = None
                if self._match(BY):
                    step = self._additive()
                return RangeLiteral(expr, end, exclusive=True, step=step)
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

            if self._match(PROTO):
                name = self._consume(IDENT, "Expected property name after '::'.").lexeme
                expr = ProtoAccessExpr(expr, name)
                continue

            if self._match(QUESTIONDOT):
                name = self._consume(IDENT, "Expected property name after '?.'.").lexeme
                expr = SafeAccessExpr(expr, name)
                continue

            if self._match(LBRACKET):
                expr = self._parse_index_or_slice(expr)
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
        
        expr = self._if_expression()
        
        if self._match(DOTDOTDOT):
            expr = SpreadExpr(expr)
        
        return None, expr

    def _parse_index_or_slice(self, target: Expression) -> Expression:
        start: Expression | None = None
        end: Expression | None = None
        exclusive = False
        
        if self._check(DOTDOT):
            self._advance()
            if not self._check(RBRACKET):
                end = self._additive()
            self._consume(RBRACKET, "Expected ']' after slice.")
            return SliceExpr(target, None, end, exclusive=False)
        
        if self._check(DOTDOTDOT):
            self._advance()
            if not self._check(RBRACKET):
                end = self._additive()
            self._consume(RBRACKET, "Expected ']' after slice.")
            return SliceExpr(target, None, end, exclusive=True)
        
        start = self._additive()
        
        if self._match(DOTDOT):
            if not self._check(RBRACKET):
                end = self._additive()
            self._consume(RBRACKET, "Expected ']' after slice.")
            return SliceExpr(target, start, end, exclusive=False)
        
        if self._match(DOTDOTDOT):
            if not self._check(RBRACKET):
                end = self._additive()
            self._consume(RBRACKET, "Expected ']' after slice.")
            return SliceExpr(target, start, end, exclusive=True)
        
        self._consume(RBRACKET, "Expected ']' after index expression.")
        return IndexExpr(target, start)

    def _primary(self) -> Expression:
        if self._check(IDENT) and self._check_next(ARROW):
            name = self._advance().lexeme
            self._consume(ARROW, "Expected '->' in function literal.")
            body = self._parse_function_body()
            return FunctionLiteral([name], body, bound=False)

        if self._check(IDENT) and self._check_next(FAT_ARROW):
            name = self._advance().lexeme
            self._consume(FAT_ARROW, "Expected '=>' in fat arrow function.")
            body = self._parse_function_body()
            return FunctionLiteral([name], body, bound=True)

        if self._match(ARROW):
            body = self._parse_function_body()
            return FunctionLiteral([], body, bound=False)

        if self._match(FAT_ARROW):
            body = self._parse_function_body()
            return FunctionLiteral([], body, bound=True)

        if self._match(DO):
            return DoExpr(self._expression())

        if self._match(YIELD):
            if self._check(NEWLINE, SEMICOLON, OUTDENT, EOF, RPAREN, RBRACKET, RBRACE, COMMA):
                return YieldExpr(None)
            return YieldExpr(self._expression())

        if self._match(AT):
            prop_name = self._consume(IDENT, "Expected property name after '@'.").lexeme
            return GetAttr(ThisExpr(), prop_name)

        if self._match(PROTO):
            name = self._consume(IDENT, "Expected property name after '::'.").lexeme
            return ProtoAccessExpr(None, name)

        if self._match(NUMBER):
            return Literal(self._previous().literal)

        if self._match(STRING):
            return self._parse_string_literal(self._previous().literal)

        if self._match(TRUE):
            return Literal(True)

        if self._match(FALSE):
            return Literal(False)

        if self._match(NULL, UNDEFINED):
            return Literal(None)

        if self._match(THIS):
            return ThisExpr()

        if self._match(SUPER):
            return SuperExpr()

        if self._match(NEW):
            class_expr = self._call()
            if isinstance(class_expr, Call):
                return NewExpr(class_expr.callee, class_expr.args, class_expr.kwargs)
            return NewExpr(class_expr, [], [])

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
            if self._match(INDENT):
                return self._parse_indented_block_expression()
            # Empty body after newline - return null
            return Literal(None)

        # Check for empty inline body (EOF, NEWLINE, or statement terminators)
        if self._check(EOF, NEWLINE, OUTDENT, SEMICOLON):
            return Literal(None)

        return self._if_expression()

    def _try_parse_parenthesized_function_literal(self) -> FunctionLiteral | None:
        params: list[str] = []
        splat_param = False
        defaults: dict = {}
        this_params: list[str] = []

        if self._match(RPAREN):
            if not self._match(ARROW):
                return None
            body = self._parse_function_body()
            return FunctionLiteral(params, body, splat_param, tuple(defaults.items()), tuple(this_params))

        first_param = self._try_parse_function_param()
        if first_param is None:
            return None
        
        param_name, is_this_param, default_value = first_param
        params.append(param_name)
        if is_this_param:
            this_params.append(param_name)
        if default_value is not None:
            defaults[param_name] = default_value
        if self._match(DOTDOTDOT):
            splat_param = True

        while self._match(COMMA):
            param = self._try_parse_function_param()
            if param is None:
                return None
            param_name, is_this_param, default_value = param
            params.append(param_name)
            if is_this_param:
                this_params.append(param_name)
            if default_value is not None:
                defaults[param_name] = default_value
            if self._match(DOTDOTDOT):
                splat_param = True

        if not self._match(RPAREN):
            return None
        if not self._match(ARROW):
            return None

        body = self._parse_function_body()
        return FunctionLiteral(params, body, splat_param, tuple(defaults.items()), tuple(this_params))

    def _try_parse_function_param(self) -> tuple[str, bool, Expression | None] | None:
        is_this_param = False
        if self._match(AT):
            is_this_param = True
        
        if not self._check(IDENT):
            return None
        
        param_name = self._advance().lexeme
        default_value: Expression | None = None
        
        if self._match(EQ):
            default_value = self._logical_or()
        
        return param_name, is_this_param, default_value

    def _array_literal(self) -> Expression:
        items: list[Expression] = []
        if self._match(RBRACKET):
            return ArrayLiteral(items)

        first_expr = self._expression()
        
        if self._match(FOR):
            var_name_token = self._consume(IDENT, "Expected variable name after 'for'.")
            var_name = var_name_token.lexeme
            
            if self._match(IN):
                iterable = self._expression()
            elif self._match(OF):
                iterable = self._expression()
            else:
                raise self._error(self._peek(), "Expected 'in' or 'of' in comprehension.")
            
            filter_condition: Expression | None = None
            if self._check(WHEN):
                self._advance()
                filter_condition = self._expression()
            
            self._consume(RBRACKET, "Expected ']' after comprehension.")
            return ComprehensionExpr(var_name, iterable, first_expr, filter_condition)
        
        items.append(first_expr)
        while self._match(COMMA):
            if self._check(RBRACKET):
                break
            items.append(self._expression())

        self._consume(RBRACKET, "Expected ']' after array literal.")
        return ArrayLiteral(items)

    def _object_literal(self) -> Expression:
        if self._check(RBRACE):
            self._advance()
            return ObjectLiteral([])

        # Parse first key-value pair as expressions
        key_expr = self._expression()
        self._consume(COLON, "Expected ':' after object key.")
        value_expr = self._expression()
        
        # Check for object comprehension
        if self._match(FOR):
            return self._parse_object_comprehension(key_expr, value_expr)
        
        # Regular object literal
        items: list[tuple[str, Expression]] = []
        
        # Convert key_expr to string key
        if isinstance(key_expr, Identifier):
            key_str = key_expr.name
        elif isinstance(key_expr, Literal) and isinstance(key_expr.value, str):
            key_str = key_expr.value
        else:
            raise self._error(self._peek(), "Object literal keys must be identifiers or strings.")
        
        items.append((key_str, value_expr))

        while self._match(COMMA):
            if self._check(RBRACE):
                break
            key = self._object_key()
            self._consume(COLON, "Expected ':' after object key.")
            value = self._expression()
            items.append((key, value))

        self._consume(RBRACE, "Expected '}' after object literal.")
        return ObjectLiteral(items)

    def _parse_object_comprehension(self, key_expr: Expression, value_expr: Expression) -> ObjectComprehensionExpr:
        # Parse: for k, v of/in iterable when condition
        
        if not self._match(IDENT):
            raise self._error(self._peek(), "Expected variable after 'for' in object comprehension.")
        var1 = self._previous().lexeme
        
        var2: str | None = None
        if self._match(COMMA):
            if not self._match(IDENT):
                raise self._error(self._peek(), "Expected second variable after ',' in object comprehension.")
            var2 = self._previous().lexeme
        
        if self._match(IN):
            iterable = self._expression()
        elif self._match(OF):
            iterable = self._expression()
        else:
            raise self._error(self._peek(), "Expected 'in' or 'of' in object comprehension.")
        
        filter_condition: Expression | None = None
        if self._check(WHEN):
            self._advance()
            filter_condition = self._expression()
        
        self._consume(RBRACE, "Expected '}' after object comprehension.")
        
        return ObjectComprehensionExpr(key_expr, value_expr, var1, var2, iterable, filter_condition)

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

    def _parse_string_literal(self, value) -> Expression:
        if value is None:
            return Literal("")
        
        import re
        from .lexer import Lexer
        
        if "#{" not in str(value):
            return Literal(value)
        
        str_value = str(value)
        parts: list[Expression] = []
        pattern = re.compile(r'#\{([^}]+)\}')
        last_end = 0
        
        for match in pattern.finditer(str_value):
            if match.start() > last_end:
                parts.append(Literal(str_value[last_end:match.start()]))
            
            expr_str = match.group(1)
            sub_lexer = Lexer(expr_str)
            sub_tokens = sub_lexer.tokenize()
            sub_parser = Parser(sub_tokens)
            try:
                expr = sub_parser._expression()
                parts.append(expr)
            except Exception:
                parts.append(Literal(expr_str))
            
            last_end = match.end()
        
        if last_end < len(str_value):
            parts.append(Literal(str_value[last_end:]))
        
        if len(parts) == 1:
            return parts[0]
        
        return InterpolatedString(parts)

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
