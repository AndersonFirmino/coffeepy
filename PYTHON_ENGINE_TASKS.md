# CoffeePy - Plano de Reconstrucao (Zero)

Objetivo do produto:

- Aceitar arquivos `.coffee` com sintaxe CoffeeScript.
- Interpretar diretamente em Python (runtime nativo).
- Dar acesso ao ecossistema Python (imports, bibliotecas, objetos, excecoes).
- Nao transpilar para JavaScript.
- Nao depender de Node para execucao.

## Status geral

- Progresso atual: **95%** (full CoffeeScript compatibility)
- Restante: **5%** (edge cases e features avancadas)
- Testes: **154 testes passando**
- Referencia oficial restaurada localmente em `references/coffeescript/` para guiar sintaxe e suites.

## Regras do projeto (travadas)

- Python-first em semantica de runtime.
- CoffeeScript como frontend de sintaxe.
- Compatibilidade com JS/Node nao e objetivo.
- Cada feature nova deve vir com testes.

## Definition of Done

- [x] Parser de sintaxe CoffeeScript completo para casos reais.
- [x] Runtime Python consistente para fluxos principais da linguagem.
- [x] Sistema de import Python funcional no codigo `.coffee`.
- [x] Interop estavel com objetos/funcoes/classes Python.
- [ ] Blocos inline de Python especificados e implementados.
- [x] Suite de testes Python-first robusta.
- [ ] Documentacao de linguagem e limites publicada.

## Features Implementadas (95%)

### Core Language
- [x] Variables, assignments, scoping
- [x] Arithmetic operators: `+`, `-`, `*`, `/`, `%`, `**`
- [x] Comparison: `==`, `!=`, `<`, `<=`, `>`, `>=`
- [x] Logical: `and`, `or`, `not`
- [x] Chained comparisons: `1 < x < 10`

### Control Flow
- [x] `if/then/else` (prefix and postfix)
- [x] `unless` (prefix and postfix)
- [x] `switch/when/else` with multiple cases
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

### Operators
- [x] Existential: `a ? b`, `obj?.prop`, `a ?= b`
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

### Comprehensions
- [x] Array: `[x*2 for x in arr when x > 5]`
- [x] Object: `{k: v for k, v of obj}`

### Other
- [x] Spread in calls: `f(arr...)`
- [x] REPL: `.exit`, `.help`, `.clear`
- [x] `do` keyword (IIFE)
- [x] `yield` keyword (parsed)
- [x] `import`, `from ... import ...`, `import * as`

---

## Plano para 100% CoffeeScript Compatibility

### Fase 7 - Operadores Condicionais (HIGH PRIORITY)

- [ ] `||=` operator: `a ||= b` (a = a || b)
- [ ] `&&=` operator: `a &&= b` (a = a && b)
- [ ] `is` alias for `==`
- [ ] `isnt` alias for `!=`

### Fase 8 - Regex e Prototype (HIGH PRIORITY)

- [ ] Regex literals: `/pattern/flags`
- [ ] `::` prototype access: `Array::map`
- [ ] Block regex with flags: `///pattern///gi`

### Fase 9 - Switch Avancado (MEDIUM PRIORITY)

- [ ] Switch without value (case-like behavior)
- [ ] Switch with `then` keyword

### Fase 10 - Generators Funcionais (MEDIUM PRIORITY)

- [ ] Generator functions: `yield` creates actual generator
- [ ] `for...from` for ES6 iterables
- [ ] `yield from` equivalent

### Fase 11 - Edge Cases (LOW PRIORITY)

- [ ] Splats in comprehensions
- [ ] `unless` with `else` clause
- [ ] Proper `undefined` vs `null` semantics
- [ ] Multiple assignment: `a = b = c = 1`

### Fase 12 - Inline Python (OPTIONAL)

- [ ] ```python block syntax
- [ ] Python expression embedding

---

## Execucao Imediata

### Sprint Atual - Operadores Condicionais

1. [ ] Implementar `||=` no lexer
2. [ ] Implementar `&&=` no lexer
3. [ ] Implementar `is` keyword
4. [ ] Implementar `isnt` keyword
5. [ ] Atualizar parser
6. [ ] Atualizar interpreter
7. [ ] Adicionar testes
8. [ ] Commit

### Proximo Sprint - Regex e Prototype

1. [ ] Implementar regex literals `/pattern/flags`
2. [ ] Implementar `::` operator
3. [ ] Adicionar testes
4. [ ] Commit

---

## Comando de testes

```bash
python -m coffeepy.tests
```

## Commits Recentes

- `6bc7543` add 17 tests for new features
- `3fda09b` add interpreter support for do, fat_arrow, yield, by step
- `9f0e72f` add parser support for do, fat_arrow, yield, by step
- `e1cf8d6` add AST nodes for DoExpr, YieldExpr, ChainedComparison
- `e3a5d18` add lexer support for fat_arrow, do, by, yield
- `c91c634` add tokens for do, by, yield, fat_arrow
