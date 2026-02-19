# CoffeePy - Future Improvements (WIP)

> **Status:** These are hobby improvements for the uncertain future. CoffeePy is currently a functional toy language.

## High Priority (When Bored)

### Safe Access (`?.`) Full Support
- [ ] `?.` should return `null` when property doesn't exist (not throw error)

```coffee
# Current behavior (BUG):
user = {age: 30}
user?.name          # → ERROR: Attribute 'name' not found.

# Expected behavior:
user = {age: 30}
user?.name          # → null (safe, like JS/CoffeeScript)

# Already works:
user = null
user?.name          # → null ✅
```

### Better Error Messages
- [ ] Runtime errors should show line number and column
- [ ] Stack traces for nested function calls
- [ ] Better error context (show the offending line)
- [ ] Suggested fixes for common mistakes

```coffee
# Current:
Undefined identifier 'undefined_var'.

# Desired:
Undefined identifier 'undefined_var'.
  at line 7, column 5
    undefined_var
    ^^^^^^^^^^^^^
```

### Generators
- [ ] `yield` that actually creates Python generators
- [ ] `yield from` equivalent
- [ ] Generator expressions

```coffee
# Not implemented yet
gen = -> 
  for i in [1..10]
    yield i

for x in gen()
  print x
```

## Medium Priority (Maybe Someday)

### Inline Python Blocks
- [ ] Embed raw Python code in CoffeePy

```coffee
# Not implemented yet
python:
  import numpy as np
  arr = np.array([1, 2, 3])
```

### ES6-style Iteration
- [ ] `for...from` for ES6 iterables

```coffee
# Not implemented yet
for x from iterable
  print x
```

### Splats in Comprehensions
- [ ] Spread inside comprehensions

```coffee
# Not implemented yet
result = [a, rest... for x in items]
```

## Low Priority (Probably Never)

### Source Maps
- [ ] Generate source maps for debugging

### Proper `undefined` vs `null`
- [ ] Distinguish between `undefined` and `null` like JavaScript

### Switch Enhancements
- [ ] `switch` with `then` keyword
- [ ] Fall-through behavior option

### Performance
- [ ] Bytecode compilation
- [ ] JIT compilation hints
- [ ] Optimized loops

---

## Contributing

Feel free to implement any of these! PRs welcome.

## Won't Implement

These are intentionally excluded:

- **JavaScript transpilation** - CoffeePy runs on Python, not JS
- **Node.js compatibility** - Python runtime only
- **Full CoffeeScript compatibility** - Some JS-specific features don't make sense in Python context
