# CoffeePy Language Guide

Complete reference for CoffeePy syntax and features.

## Table of Contents

1. [Basics](#basics)
2. [Variables](#variables)
3. [Operators](#operators)
4. [Functions](#functions)
5. [Control Flow](#control-flow)
6. [Data Structures](#data-structures)
7. [Classes](#classes)
8. [Comprehensions](#comprehensions)
9. [Strings](#strings)
10. [Regular Expressions](#regular-expressions)
11. [Python Interop](#python-interop)
12. [REPL](#repl)

---

## Basics

### Comments

```coffee
# Single line comment

###
Multi-line
comment
###
```

### Identifiers

```coffee
# Valid identifiers
name = "John"
user_name = "johndoe"
userName = "johndoe"
private = "accessible"  # not reserved in CoffeePy
```

### Literals

```coffee
# Numbers
integer = 42
float = 3.14
hex = 0xFF
scientific = 1.5e10

# Booleans
yes_value = true
no_value = false
on_value = on
off_value = off

# Null
nothing = null
undefined_value = undefined
```

---

## Variables

### Assignment

```coffee
# Basic assignment
x = 10
name = "Alice"

# Multiple assignment
a = b = c = 0

# Destructuring assignment
[first, second] = [1, 2]
{name, age} = person
```

### Augmented Assignment

```coffee
x = 10
x += 5    # x = 15
x -= 3    # x = 12
x *= 2    # x = 24
x /= 4    # x = 6
```

### Logical Assignment

```coffee
# ||= assigns if falsy
name = ""
name ||= "Anonymous"  # name = "Anonymous"

# &&= assigns if truthy
count = 5
count &&= count * 2   # count = 10

# ?= assigns if null/undefined
value = null
value ?= "default"    # value = "default"
```

### Existential Assignment

```coffee
# Only assigns if currently null/undefined
config ?= {debug: false}
```

---

## Operators

### Arithmetic

```coffee
+   # Addition
-   # Subtraction
*   # Multiplication
/   # Division
%   # Modulo
**  # Power
```

### Comparison

```coffee
==  # Equal
!=  # Not equal
<   # Less than
<=  # Less than or equal
>   # Greater than
>=  # Greater than or equal
is  # Alias for ==
isnt # Alias for !=
```

### Logical

```coffee
and   # Logical AND
or    # Logical OR
not   # Logical NOT
!     # Logical NOT (prefix)
```

### Chained Comparisons

```coffee
# Python-style chained comparisons
1 < x < 10
0 <= y <= 100
a < b < c < d
```

### Membership

```coffee
# in - check if value in array/string
3 in [1, 2, 3, 4, 5]      # true
"a" in "banana"            # true

# of - check if key in object
"name" of {name: "John"}   # true
```

### Existential

```coffee
# ? - returns left if truthy, else right
value = null
result = value ? "default"  # "default"

# ?. - safe property access
user = {name: "John"}
user?.name    # "John"
null?.name    # null (no error)
```

---

## Functions

### Basic Functions

```coffee
# No parameters
greet = -> "Hello!"

# Single parameter
double = (x) -> x * 2

# Multiple parameters
add = (a, b) -> a + b

# Call
greet()        # "Hello!"
double 5       # 10
add(3, 4)      # 7
```

### Multiline Functions

```coffee
calculate = (a, b, c) ->
  sum = a + b
  sum * c

# Or with explicit block
process = (data) ->
  step1 = transform data
  step2 = validate step1
  step2
```

### Default Parameters

```coffee
greet = (name = "World") -> "Hello, #{name}!"

greet()          # "Hello, World!"
greet("Alice")   # "Hello, Alice!"

# Multiple defaults
configure = (host = "localhost", port = 8080, debug = false) ->
  {host, port, debug}
```

### Rest Parameters (Splat)

```coffee
sum = (numbers...) ->
  total = 0
  for n in numbers
    total += n
  total

sum(1, 2, 3, 4, 5)  # 15
sum()               # 0

# With regular parameters
format = (prefix, items...) ->
  "#{prefix}: #{items.join(', ')}"

format("Items", "a", "b", "c")  # "Items: a, b, c"
```

### @param Shorthand

```coffee
class User
  # @name automatically assigns this.name = name
  constructor: (@name, @email) ->
  
  getInfo: -> "#{@name} <#{@email}>"

user = new User("John", "john@example.com")
user.name   # "John"
```

### Fat Arrow (=>)

```coffee
class Button
  constructor: (@label) ->
    # => automatically binds 'this'
    this.onClick = =>
      print @label
  
  # Method also auto-bound
  handleClick: =>
    @label

btn = new Button("Click Me")
callback = btn.onClick
callback()  # "Click Me" - 'this' is preserved
```

### Closures

```coffee
counter = do ->
  count = 0
  ->
    count += 1
    count

counter()  # 1
counter()  # 2
counter()  # 3

# Private state
createWallet = (initial) ->
  balance = initial
  {
    deposit: (amount) -> balance += amount
    withdraw: (amount) -> balance -= amount
    getBalance: -> balance
  }

wallet = createWallet 100
wallet.deposit 50
wallet.getBalance()  # 150
```

### do Keyword (IIFE)

```coffee
# Immediately Invoked Function Expression
result = do -> 1 + 2  # 3

# With parameters
result = do (x = 5) -> x * 2  # 10

# For creating isolated scope
do ->
  private = "only here"
  # ...
```

---

## Control Flow

### if/then/else

```coffee
# Inline
result = if x > 0 then "positive" else "negative"

# Multiline
if x > 100
  "large"
else if x > 10
  "medium"
else
  "small"

# Postfix (guard)
doSomething() if ready
```

### unless

```coffee
# unless = if not
unless error
  proceed()

# Postfix
skipValidation() if isAdmin
validate() unless isAdmin
```

### switch/when/else

```coffee
# With value
switch day
  when "Mon", "Tue", "Wed", "Thu", "Fri" then "weekday"
  when "Sat", "Sun" then "weekend"
  else "unknown"

# Without value (case-like)
switch
  when score >= 90 then "A"
  when score >= 80 then "B"
  when score >= 70 then "C"
  when score >= 60 then "D"
  else "F"

# Multiline body
switch command
  when "start"
    initialize()
    startServer()
  when "stop"
    stopServer()
    cleanup()
  else
    print "Unknown command"
```

### while

```coffee
# Basic
while x < 10
  x += 1

# With then
while condition then process()

# until = while not
until finished
  doWork()
```

### for loops

```coffee
# for...in (arrays/iterables)
for item in [1, 2, 3]
  print item

# for...in with index
for item, index in ["a", "b", "c"]
  print "#{index}: #{item}"

# for...of (objects)
for key, value of {name: "John", age: 30}
  print "#{key} = #{value}"

# for...of (keys only)
for key of object
  print key
```

### break/continue

```coffee
# break - exit loop
for x in [1..100]
  break if x > 10
  print x

# continue - skip iteration
for x in [1..10]
  continue if x % 2 == 0
  print x  # prints odd numbers only
```

### return

```coffee
# Explicit return
findUser = (id) ->
  return null if id < 0
  return users[id]

# Implicit return (last expression)
double = (x) ->
  x * 2
```

### throw/try/catch/finally

```coffee
# throw
throw "Something went wrong"
throw new Error("Failed")

# try/catch
try
  riskyOperation()
catch error
  print "Error: #{error}"

# try/catch/finally
try
  processFile()
catch error
  handleError error
finally
  cleanup()

# try/finally
try
  acquireResource()
finally
  releaseResource()
```

---

## Data Structures

### Arrays

```coffee
# Literal
numbers = [1, 2, 3, 4, 5]
mixed = [1, "two", true, null]

# Access
first = numbers[0]
last = numbers[numbers.length - 1]

# Assignment
numbers[0] = 10

# Range literal
range = [1..5]      # [1, 2, 3, 4, 5]
exclusive = [1...5] # [1, 2, 3, 4]

# With step
evens = [2, 4..10]  # [2, 4, 6, 8, 10]
step = [1..10 by 2] # [1, 3, 5, 7, 9]

# Descending
countdown = [5..1]  # [5, 4, 3, 2, 1]
```

### Slices

```coffee
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Inclusive
arr[2..4]    # [3, 4, 5]

# Exclusive
arr[2...5]   # [3, 4]

# From start
arr[..2]     # [1, 2, 3]

# To end
arr[7..]     # [8, 9, 10]

# With expressions
arr[start..end]
```

### Objects

```coffee
# Literal
person = {name: "John", age: 30}

# Multi-line
config =
  host: "localhost"
  port: 8080
  debug: true

# Access
name = person.name
age = person["age"]

# Assignment
person.name = "Jane"
person.email = "jane@example.com"

# Dynamic keys
key = "status"
obj = {"#{key}": "active"}  # {status: "active"}
```

### Destructuring

```coffee
# Array destructuring
[a, b, c] = [1, 2, 3]
# a = 1, b = 2, c = 3

# Skip elements
[first, , third] = [1, 2, 3]

# Splat (rest)
[head, tail...] = [1, 2, 3, 4, 5]
# head = 1, tail = [2, 3, 4, 5]

# Splat at start
[rest..., last] = [1, 2, 3, 4, 5]
# rest = [1, 2, 3, 4], last = 5

# Splat in middle
[first, middle..., last] = [1, 2, 3, 4, 5]
# first = 1, middle = [2, 3, 4], last = 5

# Object destructuring
{name, age} = {name: "John", age: 30}

# With alias
{name: userName, age} = {name: "John", age: 30}
# userName = "John", age = 30

# With defaults
{x, y = 10} = {x: 5}
# x = 5, y = 10

# Nested destructuring
[{name}, {value}] = [{name: "a"}, {value: 1}]

# In function parameters
process = ({name, age, city = "Unknown"}) ->
  "#{name}, #{age}, from #{city}"

process({name: "John", age: 30})
```

### Spread

```coffee
# In function calls
args = [1, 2, 3]
add(args...)  # add(1, 2, 3)

# Combine with regular args
format("%s: %d", name, values...)

# In arrays (via concat)
arr1 = [1, 2, 3]
arr2 = [4, 5, 6]
combined = arr1.concat(arr2)
```

---

## Classes

### Basic Class

```coffee
class Person
  constructor: (@name, @age) ->
  
  greet: -> "Hello, I'm #{@name}"
  
  birthday: ->
    @age += 1
    "Happy birthday! Now #{@age}"

person = new Person("Alice", 30)
person.greet()     # "Hello, I'm Alice"
person.birthday()  # "Happy birthday! Now 31"
```

### Inheritance

```coffee
class Animal
  constructor: (@name) ->
  
  speak: -> "#{@name} makes a sound"

class Dog extends Animal
  constructor: (@name, @breed) ->
    super @name
  
  speak: -> "#{@name} the #{@breed} barks!"

class Cat extends Animal
  speak: -> "#{@name} meows"

dog = new Dog("Rex", "German Shepherd")
dog.speak()  # "Rex the German Shepherd barks!"

cat = new Cat("Whiskers")
cat.speak()  # "Whiskers meows"
```

### this and @

```coffee
class Counter
  # @ in constructor params auto-assigns
  constructor: (@count = 0) ->
  
  # @ is shorthand for this
  increment: ->
    @count += 1
  
  # @ in methods
  getValue: -> @count
  
  # Accessing other methods
  reset: ->
    @count = 0
    @getValue()

counter = new Counter(10)
counter.increment()
counter.getValue()  # 11
```

### Prototype Access (::)

```coffee
class Array
  @first: -> this[0]

class String
  @isEmpty: -> this.length == 0

# Access prototype methods
Array::map
Array::filter
String::split
String::toUpperCase

# On CoffeePy classes
class Person
  greet: -> "Hello"

Person::greet  # Access the method
```

### Static Methods

```coffee
class Math
  @PI: 3.14159
  
  @square: (x) -> x * x
  
  @cube: (x) -> x * x * x

Math.PI        # 3.14159
Math.square(5) # 25
Math.cube(3)   # 27
```

---

## Comprehensions

### Array Comprehensions

```coffee
# Basic
doubled = [x * 2 for x in [1, 2, 3, 4, 5]]
# [2, 4, 6, 8, 10]

# With filter (when)
evens = [x for x in [1..10] when x % 2 == 0]
# [2, 4, 6, 8, 10]

# With index
indexed = ["#{i}: #{x}" for x, i in ["a", "b", "c"]]
# ["0: a", "1: b", "2: c"]

# Nested
matrix = [[x * y for x in [1, 2, 3]] for y in [1, 2, 3]]

# With range
squares = [x * x for x in [1..10]]

# With step
stepped = [x for x in [1..100 by 10]]
# [1, 11, 21, 31, 41, 51, 61, 71, 81, 91]
```

### Object Comprehensions

```coffee
# Basic
squares = {x: x * x for x in [1, 2, 3, 4, 5]}
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# From object
doubled = {k: v * 2 for k, v of {a: 1, b: 2, c: 3}}
# {a: 2, b: 4, c: 6}

# With filter
active = {k: v for k, v of users when v.active}

# Transform keys
upper = {k.toUpperCase(): v for k, v of data}
```

---

## Strings

### Interpolation

```coffee
name = "Alice"
age = 30

# Basic interpolation
greeting = "Hello, #{name}!"
# "Hello, Alice!"

# Expressions
info = "Next year: #{age + 1}"
# "Next year: 31"

# Complex expressions
sum = "Total: #{[1, 2, 3].reduce((a, b) -> a + b, 0)}"
```

### Block Strings

```coffee
# Triple quotes
text = """
Hello
World
"""
# "Hello\nWorld"

# With interpolation
name = "Alice"
message = """
Dear #{name},

Thank you for joining us!

Best regards,
Team
"""

# Single quotes (no interpolation)
literal = '''
Use #{name} literally
'''
```

### Escape Sequences

```coffee
"\n"    # newline
"\t"    # tab
"\\"    # backslash
"\""    # quote
"#{\"nested\"}"  # nested interpolation
```

---

## Regular Expressions

### Regex Literals

```coffee
# Basic
pattern = /hello/

# With flags
caseInsensitive = /hello/i
global = /hello/g
multiline = /hello/m

# Combined
full = /^hello.*world$/gim
```

### Heregex

```coffee
# Multi-line regex with comments
pattern = ///
  ^             # start of line
  [\d]+         # digits
  \s*           # optional whitespace
  [a-z]+        # letters
  $             # end of line
///

# Ignores whitespace and comments
```

### Using Regex

```coffee
pattern = /hello/i

# test
result = pattern.search("Hello World") isnt null
# true

# match
match = pattern.exec("Hello World")

# With Python interop
import re
pattern = re.compile(r"hello", re.IGNORECASE)
result = pattern.search("Hello World")
```

---

## Python Interop

### Import Statements

```coffee
# Import module
import os
print os.getcwd()

# From import
from os import getcwd, getenv
print getcwd()

# From import with alias
from datetime import datetime as dt
print dt.now()

# Import all
from os.path import *
print join("a", "b")

# Import all as alias
from os import * as os_module
print os_module.name

# Dotted modules
from collections import defaultdict
from urllib.request import urlopen
```

### Using Python Libraries

```coffee
# Standard library
from json import dumps, loads
from datetime import datetime, timedelta
from random import random, randint, choice
from math import sqrt, pi, sin, cos

# Lists
json_str = dumps({name: "John", age: 30})
data = loads('{"key": "value"}')

# Dates
now = datetime.now()
tomorrow = now + timedelta(days=1)

# Random
num = random()
die = randint(1, 6)
item = choice(["a", "b", "c"])

# Math
root = sqrt(16)  # 4.0
```

### Python Objects

```coffee
# All Python objects work
from io import StringIO
buffer = StringIO()
buffer.write("Hello")
print buffer.getvalue()

# Context managers
from contextlib import contextmanager

# Decorators work
from functools import wraps
```

### Error Handling

```coffee
try
  from nonexistent import module
catch error
  print "Import failed: #{error}"
```

---

## REPL

### Starting REPL

```bash
python -m coffeepy -i
```

### REPL Commands

```
coffee> .help
.exit  - Exit the REPL
.help  - Show this help
.clear - Clear the screen

coffee> .exit
Bye!
```

### Using REPL

```
coffee> x = 10
10
coffee> y = 20
20
coffee> x + y
30
coffee> double = (n) -> n * 2
<function>
coffee> double x
20
coffee> from math import sqrt
coffee> sqrt 16
4.0
```

---

## Semantic Differences from JavaScript CoffeeScript

| Feature | JS CoffeeScript | CoffeePy |
|---------|-----------------|----------|
| `null` | JavaScript null | Python None |
| `undefined` | JavaScript undefined | Python None |
| `true/false` | JavaScript boolean | Python bool |
| `yes/no/on/off` | true/false | True/False |
| Arrays | JavaScript Array | Python list |
| Objects | JavaScript Object | Python dict |
| `and/or/not` | JavaScript operators | Python operators |
| `==` | JavaScript coercion | Python equality |
| `in` | Array.includes() | `in` operator / list membership |
| `of` | `in` operator | `in` for dict keys |

---

## Quick Reference Card

```coffee
# Comments
# single line
### multi line ###

# Variables
x = 1
a = b = c = 0

# Functions
fn = -> "hi"
fn = (x) -> x * 2
fn = (x = 10) -> x
fn = (args...) -> args
fn = => @bound

# Classes
class Name extends Parent
  constructor: (@x) ->
  method: -> @x

# Operators
+, -, *, /, %, **
==, !=, <, <=, >, >=
is, isnt
and, or, not
?, ?., ?=
||=, &&=
in, of

# Ranges
[1..5]      # inclusive
[1...5]     # exclusive
[1..10 by 2] # with step

# Slices
arr[1..3]
arr[..2]
arr[3..]

# Control
if x then y else z
unless x
switch x when y then z

# Loops
for x in arr
for k, v of obj
while x
until x
break
continue

# Destructuring
[a, b] = arr
{k, v} = obj
[head, rest...] = arr

# Comprehensions
[x for x in arr]
{x: v for k, v of obj}

# Strings
"#{interpolation}"
"""block"""

# Regex
/pattern/flags
///heregex///

# Python
import os
from os import getcwd
from os import * as os
```
