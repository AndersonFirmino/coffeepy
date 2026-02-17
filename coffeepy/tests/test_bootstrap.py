from __future__ import annotations

import io
import unittest

from coffeepy.errors import CoffeeRuntimeError
from coffeepy.interpreter import Interpreter


class BootstrapRuntimeTests(unittest.TestCase):
    def run_code(self, source: str, stdout=None):
        return Interpreter(stdout=stdout).interpret(source)

    def test_assignment_and_arithmetic(self):
        result = self.run_code("x = 2 + 3 * 4\nx")
        self.assertEqual(result, 14)

    def test_import_and_explicit_call(self):
        result = self.run_code("import math\nmath.sqrt(9)")
        self.assertEqual(result, 3.0)

    def test_from_import_alias_and_implicit_call(self):
        result = self.run_code("from math import sqrt as root\nroot 16")
        self.assertEqual(result, 4.0)

    def test_dotted_import_binds_root_module(self):
        result = self.run_code("import urllib.parse\nurllib.parse.quote('a b')")
        self.assertEqual(result, "a%20b")

    def test_implicit_print_writes_stdout(self):
        stdout = io.StringIO()
        result = self.run_code("x = 7\nprint x\nx", stdout=stdout)
        self.assertEqual(result, 7)
        self.assertEqual(stdout.getvalue(), "7\n")

    def test_builtin_len_implicit_call(self):
        result = self.run_code("len 'abc'")
        self.assertEqual(result, 3)

    def test_comments_are_ignored(self):
        result = self.run_code("import math # ok\nmath.sqrt 9")
        self.assertEqual(result, 3.0)

    def test_if_then_else_expression(self):
        result = self.run_code("if 2 > 1 then 10 else 20")
        self.assertEqual(result, 10)

    def test_postfix_if_and_unless(self):
        self.assertEqual(self.run_code("10 if true"), 10)
        self.assertIsNone(self.run_code("10 unless true"))

    def test_logical_operators(self):
        self.assertEqual(self.run_code("x = true and 7\nx"), 7)
        self.assertEqual(self.run_code("x = false or 9\nx"), 9)
        self.assertEqual(self.run_code("x = not false\nx"), True)

    def test_function_literal_and_call(self):
        result = self.run_code("square = (x) -> x * x\nsquare 6")
        self.assertEqual(result, 36)

    def test_zero_arg_function_literal(self):
        result = self.run_code("answer = -> 42\nanswer()")
        self.assertEqual(result, 42)

    def test_function_closure_reads_outer_scope(self):
        result = self.run_code("n = 40\nadd = x -> x + n\nadd 2")
        self.assertEqual(result, 42)

    def test_comparison_and_grouping(self):
        self.assertEqual(self.run_code("(2 + 3) * 4"), 20)
        self.assertEqual(self.run_code("3 == 3"), True)
        self.assertEqual(self.run_code("3 != 4"), True)

    def test_multiline_if_block(self):
        source = """if 3 > 2
  a = 10
  a + 1
else
  0
"""
        self.assertEqual(self.run_code(source), 11)

    def test_multiline_unless_block(self):
        source = """unless false
  a = 2
  a * 3
else
  0
"""
        self.assertEqual(self.run_code(source), 6)

    def test_multiline_function_body(self):
        source = """double_then_add = (x, y) ->
  z = x * 2
  z + y
double_then_add 5, 3
"""
        self.assertEqual(self.run_code(source), 13)

    def test_explicit_call_with_kwargs(self):
        result = self.run_code("from urllib.parse import quote\nquote('a/b', safe='')")
        self.assertEqual(result, "a%2Fb")

    def test_array_object_and_index(self):
        source = """arr = [1, 2, 3]
obj = {name: 'coffee', score: arr[1]}
obj.name
"""
        self.assertEqual(self.run_code(source), "coffee")

    def test_index_chain(self):
        source = """x = [[10, 20], [30, 40]]
x[1][0]
"""
        self.assertEqual(self.run_code(source), 30)

    def test_function_then_following_if_statement(self):
        source = """double = (x) ->
  y = x * 2
  y
if true
  double 4
else
  0
"""
        self.assertEqual(self.run_code(source), 8)

    def test_attribute_assignment_on_object(self):
        source = """obj = {}
obj.name = 'coffeepy'
obj.name
"""
        self.assertEqual(self.run_code(source), "coffeepy")

    def test_index_assignment_on_array(self):
        source = """arr = [1, 2, 3]
arr[1] = 99
arr[1]
"""
        self.assertEqual(self.run_code(source), 99)

    def test_index_assignment_on_dict(self):
        source = """obj = {'name': 'old'}
obj['name'] = 'new'
obj['name']
"""
        self.assertEqual(self.run_code(source), "new")

    def test_return_inside_function(self):
        source = """choose = (x) ->
  if x > 0
    return x * 2
  return 0
choose(-5)
"""
        self.assertEqual(self.run_code(source), 0)

    def test_return_none_inside_function(self):
        source = """f = ->
  return
  99
f()
"""
        self.assertIsNone(self.run_code(source))

    def test_return_outside_function_raises(self):
        with self.assertRaises(CoffeeRuntimeError):
            self.run_code("return 3")

    def test_augmented_assignment_identifier(self):
        source = """x = 10
x += 5
x -= 3
x
"""
        self.assertEqual(self.run_code(source), 12)

    def test_augmented_assignment_attribute(self):
        source = """obj = {count: 1}
obj.count += 4
obj.count
"""
        self.assertEqual(self.run_code(source), 5)

    def test_augmented_assignment_index(self):
        source = """arr = [2, 3]
arr[1] += 7
arr[1]
"""
        self.assertEqual(self.run_code(source), 10)

    def test_postfix_and_prefix_update(self):
        source = """x = 1
x++
++x
x
"""
        self.assertEqual(self.run_code(source), 3)

    def test_update_attribute_and_index(self):
        source = """obj = {n: 2}
arr = [5]
obj.n++
--arr[0]
[obj.n, arr[0]]
"""
        self.assertEqual(self.run_code(source), [3, 4])


if __name__ == "__main__":
    unittest.main()
