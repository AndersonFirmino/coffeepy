# CoffeePy - Full CoffeeScript Compatibility

Objetivo do produto:

- Aceitar arquivos `.coffee` com sintaxe CoffeeScript.
- Interpretar diretamente em Python (runtime nativo).
- Dar acesso ao ecossistema Python (imports, bibliotecas, objetos, excecoes).
- Nao transpilar para JavaScript.
- Nao depender de Node para execucao.

## Status geral

- Progresso atual: **100%** (full CoffeeScript compatibility)
- Testes: **177 testes passando**

## Regras do projeto (travadas)

- Python-first em semantica de runtime.
- CoffeeScript como frontend de sintaxe.
- Compatibilidade com JS/Node nao e objetivo.
- Cada feature nova deve vir com testes.

## Features Implementadas (100%)

### Core Language
- [x] Variables, assignments, scoping
- [x] Multiple assignment: `a = b = c = 1`
- [x] Arithmetic operators: `+`, `-`, `*`, `/`, `%`, `**`
- [x] Comparison: `==`, `!=`, `<`, `<=`, `>`, `>=`, `is`, `isnt`
- [x] Logical: `and`, `or`, `not`
- [x] Chained comparisons: `1 < x < 10`

### Control Flow
- [x] `if/then/else` (prefix and postfix)
- [x] `unless` (prefix and postfix)
- [x] `switch/when/else` with multiple cases
- [x] `switch` without value (case-like behavior)
- [x] `while`, `until` loops
- [x] `for x in iterable`
- [x] `for k, v of obj`
- [x] `break`, `continue`, `return`
- [x] `try/catch/finally`, `throw`

### Functions
- [x] Function literals: `x ->`, `(x, y) ->`, `->`
- [x] Default parameters: `(x = 10) ->`
- [x] Rest/splat params: `(args...) ->`
- [x] `@param` shorthand: `(@name) ->`
- [x] Fat arrow `=>` (auto-bind `this`)
- [x] Closures

### Data Structures
- [x] Arrays `[]`, Objects `{}`
- [x] Array destructuring: `[a, b] = arr`
- [x] Object destructuring: `{x, y} = obj`
- [x] Splat destructuring: `[a, rest...] = arr`
- [x] Destructuring with defaults: `{x, y = 10} = obj`
- [x] Nested destructuring

### Classes
- [x] `class`, `extends`, `super`, `new`
- [x] Constructor, methods
- [x] `this` and `@` syntax
- [x] Inheritance
- [x] Prototype access: `Class::method`

### Operators
- [x] Existential: `a ? b`, `obj?.prop`, `a ?= b`
- [x] Logical assignment: `a ||= b`, `a &&= b`
- [x] Membership: `x in arr`, `k of obj`
- [x] Ranges: `1..5` (inclusive), `1...5` (exclusive)
- [x] Range with step: `1..10 by 2`
- [x] Descending ranges: `10..1`
- [x] Slices: `arr[1..3]`, `arr[..2]`, `arr[3..]`

### Strings
- [x] Interpolation: `"Hello #{name}"`
- [x] Block strings: `"""multi line"""`
- [x] Heregex: `/// regex ///`
- [x] Escape sequences

### Regex
- [x] Regex literals: `/pattern/flags`
- [x] Regex with flags: `/pattern/gi`

### Comprehensions
- [x] Array: `[x*2 for x in arr when x > 5]`
- [x] Object: `{k: v for k, v of obj}`

### Other
- [x] Spread in calls: `f(arr...)`
- [x] REPL: `.exit`, `.help`, `.clear`
- [x] `do` keyword (IIFE)
- [x] `yield` keyword (parsed)
- [x] `import`, `from ... import ...`, `import * as`
- [x] `is` / `isnt` aliases
- [x] `is not` combination

---

## Comando de testes

```bash
python -m coffeepy.tests
```

## Commits Recentes

- `57e7adf` add 3 tests for switch without value
- `4f55c92` add interpreter support for switch without value
- `2723fb9` add parser support for switch without value
- `4ace637` update SwitchExpr to allow optional value
- `03fdeab` add 3 tests for chained assignment
- `71668e9` add interpreter support for chained assignments
