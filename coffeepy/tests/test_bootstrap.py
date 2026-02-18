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

    def test_while_loop_with_block(self):
        source = """x = 0
total = 0
while x < 5
  total += x
  x++
total
"""
        self.assertEqual(self.run_code(source), 10)

    def test_until_loop_with_block(self):
        source = """x = 0
until x >= 4
  x++
x
"""
        self.assertEqual(self.run_code(source), 4)

    def test_while_then_inline_expression(self):
        source = """x = 0
inc = ->
  x++
while x < 3 then inc()
x
"""
        self.assertEqual(self.run_code(source), 3)

    def test_while_in_function_with_return(self):
        source = """first_even = (limit) ->
  x = 0
  while x < limit
    if x % 2 == 0 and x > 0
      return x
    x++
  return -1
first_even 6
"""
        self.assertEqual(self.run_code(source), 2)

    def test_break_in_while_loop(self):
        source = """x = 0
result = 0
while x < 100
  if x == 5
    break
  result += x
  x++
result
"""
        self.assertEqual(self.run_code(source), 10)

    def test_continue_in_while_loop(self):
        source = """x = 0
evens = []
while x < 6
  x++
  if x % 2 != 0
    continue
  evens.append x
evens
"""
        self.assertEqual(self.run_code(source), [2, 4, 6])

    def test_break_outside_loop_raises(self):
        with self.assertRaises(CoffeeRuntimeError):
            self.run_code("break")

    def test_continue_outside_loop_raises(self):
        with self.assertRaises(CoffeeRuntimeError):
            self.run_code("continue")

    def test_for_in_loop_with_array(self):
        source = """total = 0
for x in [1, 2, 3, 4, 5]
  total += x
total
"""
        self.assertEqual(self.run_code(source), 15)

    def test_for_in_loop_with_range_builtin(self):
        source = """nums = []
for i in range(3)
  nums.append i
nums
"""
        self.assertEqual(self.run_code(source), [0, 1, 2])

    def test_for_in_with_break(self):
        source = """result = 0
for x in [1, 2, 3, 4, 5]
  if x == 4
    break
  result += x
result
"""
        self.assertEqual(self.run_code(source), 6)

    def test_for_in_with_continue(self):
        source = """result = 0
for x in [1, 2, 3, 4, 5]
  if x % 2 == 0
    continue
  result += x
result
"""
        self.assertEqual(self.run_code(source), 9)

    def test_for_in_nested_in_function(self):
        source = """sumList = (arr) ->
  total = 0
  for x in arr
    total += x
  total
sumList([1, 2, 3])
"""
        self.assertEqual(self.run_code(source), 6)

    def test_for_in_captures_last_value(self):
        source = """last = 0
for x in [10, 20, 30]
  last = x * 2
last
"""
        self.assertEqual(self.run_code(source), 60)

    def test_for_of_loop_keys_only(self):
        source = """obj = {a: 1, b: 2, c: 3}
keys = []
for k of obj
  keys.append k
keys.sort()
keys
"""
        self.assertEqual(self.run_code(source), ["a", "b", "c"])

    def test_for_of_loop_key_value(self):
        source = """obj = {x: 10, y: 20}
pairs = []
for k, v of obj
  pairs.append k + '=' + str(v)
pairs.sort()
pairs
"""
        self.assertEqual(self.run_code(source), ["x=10", "y=20"])

    def test_for_of_with_break(self):
        source = """obj = {a: 1, b: 2, c: 3, d: 4}
found = ''
for k, v of obj
  if v == 3
    found = k
    break
found
"""
        self.assertEqual(self.run_code(source), "c")

    def test_range_inclusive(self):
        source = """1..5"""
        self.assertEqual(self.run_code(source), [1, 2, 3, 4, 5])

    def test_range_exclusive(self):
        source = """1...5"""
        self.assertEqual(self.run_code(source), [1, 2, 3, 4])

    def test_range_with_variables(self):
        source = """start = 2
end = 4
start..end
"""
        self.assertEqual(self.run_code(source), [2, 3, 4])

    def test_range_in_for_loop(self):
        source = """sum = 0
for i in 1..4
  sum += i
sum
"""
        self.assertEqual(self.run_code(source), 10)

    def test_range_with_expression(self):
        source = """x = 3
0..(x - 1)
"""
        self.assertEqual(self.run_code(source), [0, 1, 2])

    def test_array_destructuring_basic(self):
        source = """[a, b] = [10, 20]
[a, b]
"""
        self.assertEqual(self.run_code(source), [10, 20])

    def test_array_destructuring_in_function(self):
        source = """swap = (arr) ->
  [a, b] = arr
  [b, a]
swap([1, 2])
"""
        self.assertEqual(self.run_code(source), [2, 1])

    def test_array_destructuring_with_extra_values(self):
        source = """[a, b, c] = [1, 2, 3, 4, 5]
[a, b, c]
"""
        self.assertEqual(self.run_code(source), [1, 2, 3])

    def test_array_destructuring_with_fewer_values(self):
        source = """[a, b, c] = [1, 2]
[a, b, c]
"""
        self.assertEqual(self.run_code(source), [1, 2, None])

    def test_object_destructuring_basic(self):
        source = """{x, y} = {x: 10, y: 20}
[x, y]
"""
        self.assertEqual(self.run_code(source), [10, 20])

    def test_object_destructuring_with_alias(self):
        source = """{x: a, y: b} = {x: 1, y: 2}
[a, b]
"""
        self.assertEqual(self.run_code(source), [1, 2])

    def test_object_destructuring_partial(self):
        source = """{a} = {a: 100, b: 200}
a
"""
        self.assertEqual(self.run_code(source), 100)

    def test_nested_destructuring(self):
        source = """[[a, b], c] = [[1, 2], 3]
[a, b, c]
"""
        self.assertEqual(self.run_code(source), [1, 2, 3])

    def test_class_basic(self):
        source = """class Animal
  constructor: (name) ->
    this.name = name
  
  speak: ->
    "My name is " + this.name

dog = new Animal("Rex")
dog.speak()
"""
        self.assertEqual(self.run_code(source), "My name is Rex")

    def test_class_with_methods(self):
        source = """class Counter
  constructor: ->
    this.count = 0
  
  increment: ->
    this.count += 1
    
  get: ->
    this.count

c = new Counter()
c.increment()
c.increment()
c.get()
"""
        self.assertEqual(self.run_code(source), 2)

    def test_class_inheritance(self):
        source = """class Animal
  constructor: (name) ->
    this.name = name
  
  speak: ->
    this.name

class Dog extends Animal
  constructor: (name, breed) ->
    this.name = name
    this.breed = breed
  
  speak: ->
    this.name + " the " + this.breed

dog = new Dog("Max", "Labrador")
dog.speak()
"""
        self.assertEqual(self.run_code(source), "Max the Labrador")

    def test_class_super_call(self):
        source = """class Animal
  constructor: (name) ->
    this.name = name
  
  getName: ->
    this.name

class Dog extends Animal
  constructor: (name, sound) ->
    this.name = name
    this.sound = sound
  
  getName: ->
    "Dog: " + this.name

dog = new Dog("Buddy", "woof")
dog.getName()
"""
        self.assertEqual(self.run_code(source), "Dog: Buddy")

    def test_class_with_at_syntax(self):
        source = """class Point
  constructor: (x, y) ->
    this.x = x
    this.y = y

p = new Point(10, 20)
[p.x, p.y]
"""
        self.assertEqual(self.run_code(source), [10, 20])

    def test_try_catch_basic(self):
        source = """result = "no error"
try
  throw "oops"
catch err
  result = "caught: " + err
result
"""
        self.assertEqual(self.run_code(source), "caught: oops")

    def test_try_catch_no_error(self):
        source = """result = "initial"
try
  result = "try block"
catch err
  result = "catch block"
result
"""
        self.assertEqual(self.run_code(source), "try block")

    def test_try_finally(self):
        source = """result = ""
try
  result += "try"
finally
  result += " finally"
result
"""
        self.assertEqual(self.run_code(source), "try finally")

    def test_try_catch_finally(self):
        source = """result = ""
try
  result += "try"
  throw "error"
catch err
  result += " catch"
finally
  result += " finally"
result
"""
        self.assertEqual(self.run_code(source), "try catch finally")

    def test_switch_basic(self):
        source = """x = 2
switch x
  when 1 then "one"
  when 2 then "two"
  when 3 then "three"
  else "other"
"""
        self.assertEqual(self.run_code(source), "two")

    def test_switch_with_default(self):
        source = """x = 99
switch x
  when 1 then "one"
  when 2 then "two"
  else "unknown"
"""
        self.assertEqual(self.run_code(source), "unknown")

    def test_switch_multiple_cases(self):
        source = """x = "b"
switch x
  when "a", "b" then "first group"
  when "c" then "second"
  else "other"
"""
        self.assertEqual(self.run_code(source), "first group")

    def test_switch_with_block_body(self):
        source = """x = 1
switch x
  when 1
    y = 10
    y + 5
  when 2
    20
  else
    0
"""
        self.assertEqual(self.run_code(source), 15)

    def test_existential_operator(self):
        source = """a = null
b = "hello"
a ? "default"
"""
        self.assertEqual(self.run_code(source), "default")

    def test_existential_operator_with_value(self):
        source = """a = "exists"
a ? "default"
"""
        self.assertEqual(self.run_code(source), "exists")

    def test_existential_chained(self):
        source = """a = null
b = null
c = "found"
a ? b ? c ? "none"
"""
        self.assertEqual(self.run_code(source), "found")

    def test_safe_access(self):
        source = """obj = {name: "test"}
obj?.name
"""
        self.assertEqual(self.run_code(source), "test")

    def test_safe_access_null(self):
        source = """obj = null
obj?.name
"""
        self.assertIsNone(self.run_code(source))

    def test_existential_assignment(self):
        source = """x = null
x ?= 10
x
"""
        self.assertEqual(self.run_code(source), 10)

    def test_existential_assignment_no_override(self):
        source = """x = 5
x ?= 10
x
"""
        self.assertEqual(self.run_code(source), 5)

    def test_splat_params(self):
        source = """sum = (nums...) ->
  total = 0
  for n in nums
    total += n
  total
sum(1, 2, 3, 4)
"""
        self.assertEqual(self.run_code(source), 10)

    def test_splat_params_with_regular(self):
        source = """combine = (first, rest...) ->
  result = first
  for r in rest
    result += r
  result
combine("a", "b", "c")
"""
        self.assertEqual(self.run_code(source), "abc")

    def test_splat_params_empty(self):
        source = """collect = (items...) ->
  items
collect()
"""
        self.assertEqual(self.run_code(source), [])

    def test_string_interpolation_basic(self):
        source = """name = "World"
"Hello, #{name}!"
"""
        self.assertEqual(self.run_code(source), "Hello, World!")

    def test_string_interpolation_with_expression(self):
        source = """x = 5
y = 3
"Result: #{x + y}"
"""
        self.assertEqual(self.run_code(source), "Result: 8")

    def test_string_interpolation_multiple(self):
        source = """a = "A"
b = "B"
"#{a} and #{b}"
"""
        self.assertEqual(self.run_code(source), "A and B")

    def test_in_operator_array(self):
        source = """arr = [1, 2, 3]
2 in arr
"""
        self.assertTrue(self.run_code(source))

    def test_in_operator_false(self):
        source = """arr = [1, 2, 3]
5 in arr
"""
        self.assertFalse(self.run_code(source))

    def test_in_operator_string(self):
        source = """"ell" in "hello"
"""
        self.assertTrue(self.run_code(source))

    def test_of_operator_object(self):
        source = """obj = {a: 1, b: 2}
"a" of obj
"""
        self.assertTrue(self.run_code(source))

    def test_of_operator_false(self):
        source = """obj = {a: 1, b: 2}
"c" of obj
"""
        self.assertFalse(self.run_code(source))

    def test_array_comprehension_basic(self):
        source = """arr = [1, 2, 3]
[x * 2 for x in arr]
"""
        self.assertEqual(self.run_code(source), [2, 4, 6])

    def test_array_comprehension_with_range(self):
        source = """[x * x for x in 1..5]
"""
        self.assertEqual(self.run_code(source), [1, 4, 9, 16, 25])

    def test_array_comprehension_with_filter(self):
        source = """arr = [1, 2, 3, 4, 5]
[x for x in arr when x % 2 == 0]
"""
        self.assertEqual(self.run_code(source), [2, 4])

    def test_array_comprehension_with_function(self):
        source = """double = (x) -> x * 2
arr = [1, 2, 3]
[double(x) for x in arr]
"""
        self.assertEqual(self.run_code(source), [2, 4, 6])

    def test_spread_in_call(self):
        source = """sum3 = (a, b, c) -> a + b + c
arr = [1, 2, 3]
sum3(arr...)
"""
        self.assertEqual(self.run_code(source), 6)

    def test_spread_with_regular_args(self):
        source = """sum3 = (a, b, c) -> a + b + c
sum3(1, [2, 3]...)
"""
        self.assertEqual(self.run_code(source), 6)

    def test_default_parameter(self):
        source = """greet = (name = "World") ->
  "Hello, " + name
greet()
"""
        self.assertEqual(self.run_code(source), "Hello, World")

    def test_default_parameter_override(self):
        source = """greet = (name = "World") ->
  "Hello, " + name
greet("Coffee")
"""
        self.assertEqual(self.run_code(source), "Hello, Coffee")

    def test_multiple_default_parameters(self):
        source = """add = (a = 1, b = 2, c = 3) ->
  a + b + c
add()
"""
        self.assertEqual(self.run_code(source), 6)

    def test_partial_default_parameters(self):
        source = """add = (a = 1, b = 2, c = 3) ->
  a + b + c
add(10)
"""
        self.assertEqual(self.run_code(source), 15)

    def test_mixed_params_and_defaults(self):
        source = """combine = (prefix, name = "User") ->
  prefix + ": " + name
combine("Admin")
"""
        self.assertEqual(self.run_code(source), "Admin: User")

    def test_at_param_shorthand(self):
        source = """class User
  constructor: (@name, @email) ->
  getName: -> this.name
  getEmail: -> this.email
u = new User("John", "john@test.com")
u.getName() + " - " + u.getEmail()
"""
        self.assertEqual(self.run_code(source), "John - john@test.com")

    def test_at_param_with_default(self):
        source = """class Config
  constructor: (@name, @debug = false) ->
  isDebug: -> this.debug
c = new Config("test")
c.isDebug()
"""
        self.assertFalse(self.run_code(source))

    def test_at_param_mixed(self):
        source = """class Point
  constructor: (x, @y) ->
    this.x = x
  getX: -> this.x
  getY: -> this.y
p = new Point(10, 20)
[p.getX(), p.getY()]
"""
        self.assertEqual(self.run_code(source), [10, 20])

    def test_object_comprehension_basic(self):
        source = """obj = {a: 1, b: 2, c: 3}
{k: v * 2 for k, v of obj}
"""
        self.assertEqual(self.run_code(source), {"a": 2, "b": 4, "c": 6})

    def test_object_comprehension_with_filter(self):
        source = """obj = {a: 1, b: 2, c: 3, d: 4}
{k: v for k, v of obj when v % 2 == 0}
"""
        self.assertEqual(self.run_code(source), {"b": 2, "d": 4})

    def test_object_comprehension_from_array(self):
        source = """arr = ["zero", "one", "two"]
{i: name for i, name of arr}
"""
        self.assertEqual(self.run_code(source), {0: "zero", 1: "one", 2: "two"})

    def test_array_splat_destructuring(self):
        source = """arr = [1, 2, 3, 4, 5]
[a, b, rest...] = arr
[a, b, rest]
"""
        self.assertEqual(self.run_code(source), [1, 2, [3, 4, 5]])

    def test_array_splat_destructuring_at_start(self):
        source = """arr = [1, 2, 3, 4, 5]
[rest..., last] = arr
[rest, last]
"""
        self.assertEqual(self.run_code(source), [[1, 2, 3, 4], 5])

    def test_array_splat_destructuring_middle(self):
        source = """arr = [1, 2, 3, 4, 5]
[first, middle..., last] = arr
[first, middle, last]
"""
        self.assertEqual(self.run_code(source), [1, [2, 3, 4], 5])

    def test_array_splat_destructuring_empty_rest(self):
        source = """arr = [1, 2]
[a, b, rest...] = arr
[a, b, rest]
"""
        self.assertEqual(self.run_code(source), [1, 2, []])

    def test_array_splat_destructuring_with_fewer_values(self):
        source = """arr = [1]
[a, b..., c] = arr
[a, b, c]
"""
        self.assertEqual(self.run_code(source), [1, [], None])

    def test_block_string_basic(self):
        source = '''text = """
Hello
World
"""
text
'''
        self.assertEqual(self.run_code(source), "Hello\nWorld")

    def test_block_string_with_indent(self):
        source = '''text = """
    Hello
    World
    """
text
'''
        self.assertEqual(self.run_code(source), "Hello\nWorld")

    def test_block_string_single_quotes(self):
        source = """text = '''
Line 1
Line 2
'''
text
"""
        self.assertEqual(self.run_code(source), "Line 1\nLine 2")

    def test_heregex_basic(self):
        source = '''pattern = ///
  hello
  world
///
pattern
'''
        self.assertEqual(self.run_code(source), "helloworld")

    def test_slice_basic(self):
        source = """arr = [1, 2, 3, 4, 5]
arr[1..3]
"""
        self.assertEqual(self.run_code(source), [2, 3, 4])

    def test_slice_exclusive(self):
        source = """arr = [1, 2, 3, 4, 5]
arr[1...3]
"""
        self.assertEqual(self.run_code(source), [2, 3])

    def test_slice_from_start(self):
        source = """arr = [1, 2, 3, 4, 5]
arr[..2]
"""
        self.assertEqual(self.run_code(source), [1, 2, 3])

    def test_slice_to_end(self):
        source = """arr = [1, 2, 3, 4, 5]
arr[3..]
"""
        self.assertEqual(self.run_code(source), [4, 5])

    def test_do_iife(self):
        source = """result = do -> 1 + 2
result
"""
        self.assertEqual(self.run_code(source), 3)

    def test_do_iife_with_args(self):
        source = """result = do (x = 5) -> x * 2
result
"""
        self.assertEqual(self.run_code(source), 10)

    def test_do_iife_multiline(self):
        source = """result = do ->
  x = 10
  y = 20
  x + y
result
"""
        self.assertEqual(self.run_code(source), 30)

    def test_fat_arrow_basic(self):
        source = """class Counter
  constructor: ->
    this.count = 0
  increment: =>
    this.count += 1
  get: -> this.count

c = new Counter()
c.increment()
c.increment()
c.get()
"""
        self.assertEqual(self.run_code(source), 2)

    def test_fat_arrow_preserves_this(self):
        source = """class Button
  constructor: (@label) ->
    this.onClick = =>
      this.label
  click: -> this.onClick()

btn = new Button("Submit")
btn.click()
"""
        self.assertEqual(self.run_code(source), "Submit")

    def test_range_by_step(self):
        source = "1..10 by 2"
        self.assertEqual(self.run_code(source), [1, 3, 5, 7, 9])

    def test_range_by_step_exclusive(self):
        source = "1...10 by 3"
        self.assertEqual(self.run_code(source), [1, 4, 7])

    def test_range_by_step_negative(self):
        source = "10..1 by -2"
        self.assertEqual(self.run_code(source), [10, 8, 6, 4, 2])

    def test_range_by_step_with_variables(self):
        source = """start = 0
end = 10
step = 5
start..end by step
"""
        self.assertEqual(self.run_code(source), [0, 5, 10])

    def test_object_destructuring_with_default(self):
        source = """obj = {a: 1}
{a, b = 10} = obj
[a, b]
"""
        self.assertEqual(self.run_code(source), [1, 10])

    def test_object_destructuring_with_default_override(self):
        source = """obj = {a: 1, b: 2}
{a, b = 10} = obj
[a, b]
"""
        self.assertEqual(self.run_code(source), [1, 2])

    def test_object_destructuring_alias_with_default(self):
        source = """obj = {x: 100}
{x: y, z = 999} = obj
[y, z]
"""
        self.assertEqual(self.run_code(source), [100, 999])

    def test_chained_comparison_true(self):
        source = """x = 5
1 < x < 10
"""
        self.assertTrue(self.run_code(source))

    def test_chained_comparison_false(self):
        source = """x = 15
1 < x < 10
"""
        self.assertFalse(self.run_code(source))

    def test_chained_comparison_multiple(self):
        source = """a = 1
b = 2
c = 3
a < b < c
"""
        self.assertTrue(self.run_code(source))

    def test_chained_comparison_with_equality(self):
        source = """x = 5
y = 5
z = 5
x <= y <= z
"""
        self.assertTrue(self.run_code(source))

    def test_import_star_as_alias(self):
        source = """from os import * as myos
myos.name
"""
        import os
        self.assertEqual(self.run_code(source), os.name)


if __name__ == "__main__":
    unittest.main()
