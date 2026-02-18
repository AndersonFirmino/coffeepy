# CoffeePy

**CoffeeScript that runs on Python.**

Write CoffeeScript syntax, execute with Python runtime, use the entire Python ecosystem.

- No JavaScript transpilation
- No Node.js dependency
- Full Python interop

## Installation

```bash
pip install coffeepy
```

Or clone and install:

```bash
git clone https://github.com/your-repo/coffe-py.git
cd coffe-py
pip install -e .
```

## Quick Start

```bash
# Run a file
python -m coffeepy script.coffee

# Interactive REPL
python -m coffeepy -i

# Evaluate expression
python -m coffeepy --eval "print 'Hello, World!'"
```

## Examples

### Python Imports

```coffee
from os import getcwd
from datetime import datetime
import json

print getcwd()
print datetime.now()
```

### Functions

```coffee
# Basic function
add = (a, b) -> a + b

# Default parameters
greet = (name = "World") -> "Hello, #{name}!"

# Rest parameters
sum = (numbers...) ->
  total = 0
  for n in numbers
    total += n
  total

# Fat arrow (auto-bind this)
class Counter
  constructor: ->
    this.count = 0
  increment: => this.count += 1
```

### Classes

```coffee
class Animal
  constructor: (@name) ->
  speak: -> "#{@name} makes a sound"

class Dog extends Animal
  constructor: (@name, @breed) ->
    super @name
  speak: -> "#{@name} the #{@breed} barks!"

dog = new Dog "Rex", "German Shepherd"
dog.speak()
```

### Destructuring

```coffee
# Array
[first, second, rest...] = [1, 2, 3, 4, 5]

# Object
{name, age} = {name: "John", age: 30}

# With defaults
{x, y = 10} = {x: 5}
```

### Comprehensions

```coffee
# Array comprehension
doubled = [x * 2 for x in [1, 2, 3, 4, 5]]
evens = [x for x in [1..10] when x % 2 == 0]

# Object comprehension
squares = {x: x * x for x in [1, 2, 3, 4, 5]}
```

### Control Flow

```coffee
# If/unless
result = if x > 0 then "positive" else "negative"
do_something() unless skip

# Switch
switch day
  when "Mon", "Tue", "Wed", "Thu", "Fri" then "weekday"
  when "Sat", "Sun" then "weekend"
  else "unknown"

# Switch without value (case-like)
switch
  when x < 0 then "negative"
  when x == 0 then "zero"
  else "positive"
```

### Operators

```coffee
# Existential
name = user?.name ? "Anonymous"
value ?= "default"

# Logical assignment
a ||= b  # a = a || b
a &&= b  # a = a && b

# Comparison aliases
x is y   # x == y
x isnt y # x != y

# Chained comparisons
1 < x < 10

# Ranges
[1..5]      # [1, 2, 3, 4, 5]
[1...5]     # [1, 2, 3, 4]
[1..10 by 2] # [1, 3, 5, 7, 9]
```

### Strings

```coffee
# Interpolation
greeting = "Hello, #{name}!"

# Block strings
text = """
  This is a
  multi-line
  string
"""

# Regex
pattern = /hello/i
result = pattern.search("Hello World")
```

### Try/Catch

```coffee
try
  risky_operation()
catch error
  print "Error: #{error}"
finally
  cleanup()
```

## REPL Commands

```
.exit   - Exit the REPL
.help   - Show help
.clear  - Clear the screen
```

## Features

| Category | Features |
|----------|----------|
| **Core** | Variables, scoping, arithmetic, comparison, logical operators |
| **Functions** | Literals, default params, rest params, fat arrow `=>`, closures |
| **Classes** | `class`, `extends`, `super`, `new`, `::` prototype access |
| **Control** | `if/unless`, `switch/when`, `while/until`, `for in/of` |
| **Data** | Arrays, objects, destructuring, splats, comprehensions |
| **Operators** | `?`, `?.`, `?=`, `||=`, `&&=`, `is`, `isnt`, ranges, slices |
| **Strings** | Interpolation, block strings, regex literals |
| **Python** | `import`, `from ... import`, `import * as`, full interop |

## Running Tests

```bash
python -m coffeepy.tests
```

## Language Contract

CoffeePy uses Python semantics:

- `null` and `undefined` → Python `None`
- `true/false/yes/no/on/off` → Python `True/False`
- Arrays → Python `list`
- Objects → Python `dict`
- `and/or/not` → Python `and/or/not`

## License

MIT

## Contributing

Contributions welcome! Please read the language contract before submitting PRs.

---

**CoffeePy v1.0.0** - Full CoffeeScript compatibility on Python runtime.
