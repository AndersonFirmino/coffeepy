# CoffeePy - Future Improvements (WIP)

> **Status:** These are hobby improvements for the uncertain future. CoffeePy is currently a functional toy language.

## Completed Features ✅

### Safe Access (`?.`) Full Support - DONE
- [x] `?.` returns `null` when property doesn't exist (not throw error)

```coffee
user = {age: 30}
user?.name          # → null ✅ (was ERROR before)
user?.age           # → 30 ✅
user = null
user?.name          # → null ✅
```

### Better Error Messages - DONE
- [x] Runtime errors show line number and column
- [x] Error context (show the offending line)

```coffee
x = undefined_var

# Output:
Undefined identifier 'undefined_var'.
  at line 1, column 5
    x = undefined_var
        ^^^^^^^^^^^^^
```

### Generators - IMPLEMENTED (has bug)
- [x] `yield` creates Python generators
- [ ] BUG: `for i in [1..3]` doesn't work correctly (preexisting parser bug)
- [ ] `yield from` equivalent
- [ ] Generator expressions

```coffee
# Works:
gen = ->
  yield 1
  yield 2
  yield 3

for x in gen()
  print x
# → 1, 2, 3 ✅

# BUG - doesn't work:
gen = ->
  for i in [1..3]
    yield i
# → yields [1,2,3] instead of 1, 2, 3
```

---

## High Priority (When Bored)

### Fix Range in For Loop - BUG
- [ ] `for i in [1..3]` should iterate 1, 2, 3 not [1,2,3]

```coffee
# Current (BUG):
for i in [1..3]
  print i
# → [1, 2, 3] (single value)

# Expected:
for i in [1..3]
  print i
# → 1, 2, 3 (three values)
```

**Root cause:** Parser wraps `RangeLiteral` in `ArrayLiteral` when inside `[]`.

### Generator Enhancements
- [ ] Fix generators with for loops (depends on range bug fix)
- [ ] `yield from` equivalent
- [ ] Generator expressions

---

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

---

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
