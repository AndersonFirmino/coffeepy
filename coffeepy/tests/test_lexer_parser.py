from __future__ import annotations

import unittest
from typing import cast

from coffeepy.ast_nodes import AssignStmt, Call, ExprStmt, FunctionLiteral, GetAttr, Identifier, IfExpr, IndexExpr
from coffeepy.errors import CoffeeLexerError, CoffeeParseError
from coffeepy.lexer import Lexer
from coffeepy.parser import Parser
from coffeepy.tokens import INDENT, OUTDENT


class LexerParserTests(unittest.TestCase):
    def test_lexer_emits_indent_outdent(self):
        source = """if true
  x = 1
y = 2
"""
        tokens = Lexer(source).tokenize()
        kinds = [token.kind for token in tokens]
        self.assertIn(INDENT, kinds)
        self.assertIn(OUTDENT, kinds)

    def test_parser_parses_function_literal_multiline(self):
        source = """double = (x) ->
  y = x * 2
  y
double 4
"""
        program = Parser(Lexer(source).tokenize()).parse()
        assign_stmt = program.statements[0]
        self.assertIsInstance(assign_stmt, AssignStmt)
        assign_stmt = cast(AssignStmt, assign_stmt)
        self.assertIsInstance(assign_stmt.target, Identifier)
        target = cast(Identifier, assign_stmt.target)
        self.assertEqual(target.name, "double")
        self.assertIsInstance(assign_stmt.value, FunctionLiteral)

    def test_parser_parses_prefix_if_block(self):
        source = """if true
  1
else
  2
"""
        program = Parser(Lexer(source).tokenize()).parse()
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ExprStmt)
        stmt = cast(ExprStmt, stmt)
        self.assertIsInstance(stmt.expression, IfExpr)

    def test_parser_parses_kwargs_in_explicit_call(self):
        source = "f(a=1, b=2)"
        program = Parser(Lexer(source).tokenize()).parse()
        stmt = program.statements[0]
        self.assertIsInstance(stmt, ExprStmt)
        stmt = cast(ExprStmt, stmt)
        call = stmt.expression
        self.assertIsInstance(call, Call)
        call = cast(Call, call)
        self.assertEqual(len(call.kwargs), 2)
        self.assertEqual(call.kwargs[0][0], "a")
        self.assertEqual(call.kwargs[1][0], "b")

    def test_parser_parses_attribute_assignment_target(self):
        source = "obj.name = 3"
        program = Parser(Lexer(source).tokenize()).parse()
        stmt = program.statements[0]
        self.assertIsInstance(stmt, AssignStmt)
        stmt = cast(AssignStmt, stmt)
        self.assertIsInstance(stmt.target, GetAttr)

    def test_parser_parses_index_assignment_target(self):
        source = "arr[0] = 9"
        program = Parser(Lexer(source).tokenize()).parse()
        stmt = program.statements[0]
        self.assertIsInstance(stmt, AssignStmt)
        stmt = cast(AssignStmt, stmt)
        self.assertIsInstance(stmt.target, IndexExpr)

    def test_parser_rejects_positional_after_keyword(self):
        with self.assertRaises(CoffeeParseError):
            Parser(Lexer("f(a=1, 2)").tokenize()).parse()

    def test_lexer_rejects_inconsistent_indentation(self):
        source = """if true
  x = 1
 y = 2
"""
        with self.assertRaises(CoffeeLexerError):
            Lexer(source).tokenize()

    def test_parser_rejects_invalid_assignment_target(self):
        with self.assertRaises(CoffeeParseError):
            Parser(Lexer("f(1) = 2").tokenize()).parse()


if __name__ == "__main__":
    unittest.main()
