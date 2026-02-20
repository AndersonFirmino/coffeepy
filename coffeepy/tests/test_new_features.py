#!/usr/bin/env python
"""
Test script for CoffeePy new features.
Run: python tests/test_new_features.py
"""

import unittest
import sys
import os

from coffeepy.lexer import Lexer
from coffeepy.parser import Parser
from coffeepy.interpreter import Interpreter


class TestSafeAccess(unittest.TestCase):
    """Test safe access operator (?.)"""
    
    def run_code(self, source):
        return Interpreter().interpret(source)
    
    def test_existing_property(self):
        """user?.name should return value when property exists"""
        source = '''
user = {name: "Alice", age: 30}
user?.name
'''
        result = self.run_code(source)
        self.assertEqual(result, "Alice")
    
    def test_missing_property(self):
        """user?.email should return None when property doesn't exist"""
        source = '''
user = {name: "Alice"}
user?.email
'''
        result = self.run_code(source)
        self.assertIsNone(result)
    
    def test_null_object(self):
        """user?.name should return None when user is null"""
        source = '''
user = null
user?.name
'''
        result = self.run_code(source)
        self.assertIsNone(result)
    
    def test_chained_safe_access(self):
        """data?.user?.name should work for nested access"""
        source = '''
data = {user: {name: "Bob"}}
data?.user?.name
'''
        result = self.run_code(source)
        self.assertEqual(result, "Bob")
    
    def test_chained_safe_access_with_null(self):
        """data?.user?.name should return None if any part is null"""
        source = '''
data = {user: null}
data?.user?.name
'''
        result = self.run_code(source)
        self.assertIsNone(result)


class TestBetterErrors(unittest.TestCase):
    """Test better error messages with line/column info"""
    
    def run_code(self, source):
        return Interpreter().interpret(source)
    
    def test_undefined_identifier_shows_location(self):
        """Error should show line and column"""
        source = '''x = undefined_var'''
        try:
            self.run_code(source)
            self.fail("Should have raised error")
        except Exception as e:
            error_msg = str(e)
            self.assertIn("line", error_msg.lower())
            self.assertIn("column", error_msg.lower())
    
    def test_undefined_identifier_shows_source(self):
        """Error should show source code snippet"""
        source = '''x = undefined_var'''
        try:
            self.run_code(source)
            self.fail("Should have raised error")
        except Exception as e:
            error_msg = str(e)
            self.assertIn("undefined_var", error_msg)
            self.assertIn("^", error_msg)
    
    def test_multiline_error_shows_correct_line(self):
        """Error on line 3 should show line 3"""
        source = '''
x = 1
y = 2
z = undefined_var
'''
        try:
            self.run_code(source)
            self.fail("Should have raised error")
        except Exception as e:
            error_msg = str(e)
            self.assertIn("line 4", error_msg)


class TestGenerators(unittest.TestCase):
    """Test generator functions with yield"""
    
    def run_code(self, source):
        return Interpreter().interpret(source)
    
    def test_simple_generator(self):
        """Generator with simple yields"""
        source = '''
gen = ->
  yield 1
  yield 2
  yield 3

g = gen()
[g.__next__(), g.__next__(), g.__next__()]
'''
        result = self.run_code(source)
        self.assertEqual(result, [1, 2, 3])
    
    def test_generator_in_for_loop(self):
        """Iterating over generator with for loop"""
        source = '''
gen = ->
  yield 1
  yield 2
  yield 3

result = []
for x in gen()
  result = result + [x]
result
'''
        result = self.run_code(source)
        self.assertEqual(result, [1, 2, 3])
    
    def test_generator_with_for_in_range(self):
        """Generator with for loop over range"""
        source = '''
gen = ->
  for i in [1..3]
    yield i * 2

result = []
for x in gen()
  result = result + [x]
result
'''
        result = self.run_code(source)
        self.assertEqual(result, [2, 4, 6])
    
    def test_generator_yields_each_value(self):
        """Generator should yield each value separately"""
        source = '''
gen = ->
  for i in [1..5]
    yield i

count = 0
for x in gen()
  count += 1
count
'''
        result = self.run_code(source)
        self.assertEqual(result, 5)


class TestRangeInForLoop(unittest.TestCase):
    """Test range iteration in for loops"""
    
    def run_code(self, source):
        return Interpreter().interpret(source)
    
    def test_inclusive_range(self):
        """for i in [1..3] should iterate 1, 2, 3"""
        source = '''
result = []
for i in [1..3]
  result = result + [i]
result
'''
        result = self.run_code(source)
        self.assertEqual(result, [1, 2, 3])
    
    def test_exclusive_range(self):
        """for i in [1...3] should iterate 1, 2"""
        source = '''
result = []
for i in [1...3]
  result = result + [i]
result
'''
        result = self.run_code(source)
        self.assertEqual(result, [1, 2])
    
    def test_range_with_step(self):
        """for i in [1..5 by 2] should iterate 1, 3, 5"""
        source = '''
result = []
for i in [1..5 by 2]
  result = result + [i]
result
'''
        result = self.run_code(source)
        self.assertEqual(result, [1, 3, 5])
    
    def test_range_sum(self):
        """Sum values from range iteration"""
        source = '''
total = 0
for i in [1..5]
  total += i
total
'''
        result = self.run_code(source)
        self.assertEqual(result, 15)
    
    def test_range_count(self):
        """Count iterations from range"""
        source = '''
count = 0
for i in [1..10]
  count += 1
count
'''
        result = self.run_code(source)
        self.assertEqual(result, 10)


class TestAllFeaturesIntegration(unittest.TestCase):
    """Test features working together"""
    
    def run_code(self, source):
        return Interpreter().interpret(source)
    
    def test_generator_with_safe_access(self):
        """Generator yielding safe access results"""
        source = '''
users = [{name: "Alice"}, {name: "Bob"}, {age: 30}]

gen = ->
  for user in users
    yield user?.name

result = []
for name in gen()
  result = result + [name]
result
'''
        result = self.run_code(source)
        self.assertEqual(result, ["Alice", "Bob", None])
    
    def test_generator_with_safe_access_filtered(self):
        """Generator with safe access and filter"""
        source = '''
users = [{name: "Alice"}, {age: 30}, {name: "Bob"}]

gen = ->
  for user in users
    name = user?.name
    if name isnt null
      yield name

result = []
for name in gen()
  result = result + [name]
result
'''
        result = self.run_code(source)
        self.assertEqual(result, ["Alice", "Bob"])
    
    def test_range_with_comprehension(self):
        """Comprehension over range"""
        source = '''
[x * 2 for x in [1..5]]
'''
        result = self.run_code(source)
        self.assertEqual(result, [2, 4, 6, 8, 10])
    
    def test_safe_access_with_comprehension(self):
        """Safe access in comprehension"""
        source = '''
users = [{name: "A"}, {age: 20}, {name: "B"}]
[user?.name for user in users when user?.name isnt null]
'''
        result = self.run_code(source)
        self.assertEqual(result, ["A", "B"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
