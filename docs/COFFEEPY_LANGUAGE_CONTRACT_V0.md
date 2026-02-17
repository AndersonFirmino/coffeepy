# CoffeePy Language Contract v0

This document defines the initial contract for CoffeePy after the Python-first pivot.

## Core principle

- Source syntax: CoffeeScript-style `.coffee`.
- Runtime semantics: Python-first.
- Execution engine: native Python interpreter in this repository.
- JavaScript/Node runtime behavior is not a compatibility target.

## Current semantic rules (v0)

- `null` and `undefined` map to Python `None`.
- Boolean aliases supported in source: `true/false`, `yes/no`, `on/off`.
- `and`, `or`, `not` follow Python truthiness and short-circuit rules.
- `==` and `!=` map to Python equality operations.
- Numeric operators map directly to Python operators.
- Import execution uses Python `importlib`.
- Indentation creates executable blocks for supported constructs.

## Current syntax surface (implemented)

- Statements:
  - `import module`
  - `import module as alias`
  - `from module import name`
  - `from module import name as alias`
  - assignment targets:
    - identifier: `x = expression`
    - attribute: `obj.name = expression`
    - index: `arr[0] = expression`, `obj['k'] = expression`
  - `return` (function body support in current implementation)
  - expression statements
  - indented blocks for:
    - prefix `if/unless`
    - function literal body after `->`

- Expressions:
  - literals: number, string, booleans, `null`, `undefined`
  - identifiers
  - arithmetic: `+`, `-`, `*`, `/`, `%`, `**`
  - comparisons: `<`, `<=`, `>`, `>=`, `==`, `!=`
  - logical: `and`, `or`, `not`
  - unary: `+`, `-`
  - property access: `obj.prop`
  - indexing: `obj[idx]`
  - collection literals:
    - arrays: `[a, b, c]`
    - objects: `{name: value, ...}`
  - call forms:
    - explicit: `fn(...)`
    - implicit simple: `fn x`, `fn x, y`
    - explicit keyword arguments: `fn(a=1, b=2)`
  - conditionals:
    - prefix: `if cond then a else b`
    - postfix: `a if cond`
    - postfix unless: `a unless cond`
  - function literals:
    - `x -> expr`
    - `(x, y) -> expr`
    - `-> expr`

## Runtime interop behavior

- Python module import is first class.
- Attributes are resolved with Python attribute access (`getattr`) and dict key fallback for dict targets.
- Python builtins are available by identifier fallback (e.g. `len`, `str`, `int`).
- Function literals close over the lexical environment.
- `return` inside function literal exits function execution immediately.
- Object literals are currently represented as Python `dict`.
- Array literals are currently represented as Python `list`.

## Current limitations to be refined

- Implicit call argument parsing currently favors unambiguous forms; for signed literal arguments prefer explicit call syntax (`f(-1)`).

## Out of scope for v0

- Full CoffeeScript grammar completeness.
- Class syntax and full block semantics.
- Comprehensions, destructuring, splats/rest.
- Inline Python block syntax (planned).

## Error boundaries

- Lexer errors -> `CoffeeLexerError`
- Parser errors -> `CoffeeParseError`
- Runtime errors -> `CoffeeRuntimeError`
