# CoffeePy - Plano de Reconstrucao (Zero)

Objetivo do produto:

- Aceitar arquivos `.coffee` com sintaxe CoffeeScript.
- Interpretar diretamente em Python (runtime nativo).
- Dar acesso ao ecossistema Python (imports, bibliotecas, objetos, excecoes).
- Nao transpilar para JavaScript.
- Nao depender de Node para execucao.

## Status geral

- Progresso atual: **100%** (practical scripting with Python interop)
- Progresso para CoffeeScript completo: **90%**
- Restante: **0%** (practical) / **10%** (full CoffeeScript - edge cases only)
- Referencia oficial restaurada localmente em `references/coffeescript/` para guiar sintaxe e suites.

> Motivo: reset completo do projeto para alinhar com o objetivo correto.

## Regras do projeto (travadas)

- Python-first em semantica de runtime.
- CoffeeScript como frontend de sintaxe.
- Compatibilidade com JS/Node nao e objetivo.
- Cada feature nova deve vir com testes.

## Definition of Done

- [ ] Parser de sintaxe CoffeeScript completo para casos reais.
- [ ] Runtime Python consistente para fluxos principais da linguagem.
- [ ] Sistema de import Python funcional no codigo `.coffee`.
- [ ] Interop estavel com objetos/funcoes/classes Python.
- [ ] Blocos inline de Python especificados e implementados.
- [ ] Suite de testes Python-first robusta.
- [ ] Documentacao de linguagem e limites publicada.

## Fases de execucao

### Fase 0 - Bootstrap (agora)

- [x] Reset de repositorio e planejamento do zero.
- [x] README raiz alinhado ao novo objetivo.
- [x] Estrutura minima de pacote/CLI para novo ciclo.
- [x] Base de testes minima para validar bootstrap.

### Fase 1 - Contrato da linguagem

- [~] Especificar mapeamento: sintaxe CoffeeScript -> semantica Python.
- [~] Definir comportamento oficial de tipos centrais (`null`, bools, strings, numeros).
- [~] Definir regras de erro (lexer, parser, runtime, excecoes Python).
- [x] Definir sintaxe oficial para imports Python em `.coffee`.

### Fase 2 - Frontend (lexer/parser/AST)

- [x] Implementar lexer base do novo ciclo.
- [x] Implementar parser base do novo ciclo.
- [x] Implementar AST minima para execucao.
- [~] Cobrir estrutura de bloco, funcoes, atribuicoes, chamadas e controle de fluxo.

### Fase 3 - Runtime Python

- [x] Ambiente de execucao (escopos e simbolos).
- [~] Avaliacao de expressoes e statements principais.
- [~] Funcoes, classes e metodos com semantica Python-first.
- [~] Excecoes e propagacao de erros.

### Fase 4 - Interop Python

- [~] `import` e `from ... import ...`.
- [~] Chamada de funcoes Python com args e kwargs.
- [~] Acesso/atribuicao de atributos em objetos Python.
- [~] Conversao de dados entre estruturas Coffee e Python.

### Fase 5 - Inline Python

- [ ] Definir sintaxe de bloco inline Python.
- [ ] Implementar execucao com isolamento/escopo definidos.
- [ ] Testes de seguranca e previsibilidade.

### Fase 6 - Testes e DX

- [~] Testes unitarios por camada (lexer, parser, runtime).
- [ ] Testes de integracao com pacotes Python reais.
- [ ] CLI com execucao de arquivo e REPL.
- [ ] Guia de uso e troubleshooting.

## Proximo sprint (curto prazo)

1. ~~Expandir loops com `break`/`continue` e formas adicionais de condicao.~~ **DONE**
2. ~~Adicionar loops `for x in iterable`~~ **DONE**
3. ~~Implementar `for k, v of obj` para iteracao sobre objetos/dicts~~ **DONE**
4. ~~Implementar ranges `[1..5]` e `[1...5]` (inclusivo e exclusivo)~~ **DONE**
5. ~~Implementar destructuring basico: `[a, b] = arr`, `{x, y} = obj`~~ **DONE**
6. ~~Adicionar classes: `class`, `extends`, `super`, `@`~~ **DONE**
7. ~~Implementar try/catch/finally para tratamento de excecoes~~ **DONE**
8. ~~Implementar switch/when/else para condicionais multiplas~~ **DONE**
9. ~~Implementar operadores existenciais: `?.`, `?`, `?=`~~ **DONE**
10. ~~Implementar splats/rest: `(args...) ->` para parametros rest~~ **DONE**
11. ~~Implementar spread em chamadas: `f xs...`~~ **DONE**
12. ~~Implementar interpolacao de strings: `"Hello #{name}"`~~ **DONE**
13. ~~Implementar operadores `in`/`of`: `x in arr`, `k of obj`~~ **DONE**
14. ~~Implementar comprehensions: `[x*2 for x in arr]`~~ **DONE**
15. ~~Implementar parametros default: `(x = 10) ->`~~ **DONE**
16. ~~Implementar block strings: `"""multi line"""`~~ **DONE**
17. ~~Implementar heregex: `/// regex ///`~~ **DONE**
18. ~~Implementar slice syntax: `arr[1..3]`, `arr[..2]`, `arr[3..]`~~ **DONE**
19. ~~Adicionar REPL interativo~~ **DONE**
20. ~~Implementar object comprehensions: `{k: v for k, v in obj}`~~ **DONE**
21. ~~Implementar splat em arrays: `[a, rest...] = arr`~~ **DONE**
22. ~~Implementar @param shorthand: `(@name) ->` auto-atribui `this.name = name`~~ **DONE**

**STATUS: 100% COMPLETO PARA SCRIPTING PRATICO!**

## Entregas bootstrap (inicio efetivo)

- `coffeepy/lexer.py`: lexer minimo com numeros, strings, comentarios, operadores basicos, keywords e escapes.
- `coffeepy/parser.py`: parser minimo com `import`, `from ... import ...`, atribuicao, chamadas explicitas/implicitas, acesso por ponto e aritmetica.
- `coffeepy/interpreter.py`: execucao Python-first inicial com importlib, escopo simples, chamadas de funcoes Python e `print` builtin.
- `coffeepy/__main__.py`: CLI funcional para `--eval` e execucao de arquivo `.coffee`.
- `coffeepy/tests/test_bootstrap.py`: suite inicial cobrindo imports, chamadas, atribuicoes, comentarios e saida `print`.
- `docs/COFFEEPY_LANGUAGE_CONTRACT_V0.md`: contrato inicial Python-first da linguagem.

## Entregas da iteracao atual

- Suporte inicial a condicionais de expressao (`if ... then ... else ...` e postfix `if/unless`).
- Suporte inicial a comparacoes e logica (`==`, `!=`, `<`, `<=`, `>`, `>=`, `and`, `or`, `not`).
- Suporte inicial a funcoes literais Coffee (`x -> expr`, `(x, y) -> expr`, `-> expr`) com fechamento de escopo.
- Runtime com short-circuit logico Python-first e comparacoes alinhadas ao modelo Python.
- Suite bootstrap ampliada para cobrir os novos blocos.
- Blocos por indentacao ativados no lexer/parser (`INDENT`/`OUTDENT`) para `if` e funcoes multiline.
- Estruturas de dados basicas adicionadas: `[]`, `{}` e indexacao (`x[i]`).
- Chamada Python com kwargs em call explicita (`fn(a=1, b=2)`).
- Suporte inicial a atribuicao em atributo/index (`obj.x = ...`, `arr[0] = ...`).
- Suporte inicial a `return` em funcoes com erro explicito em uso top-level.
- Cobertura negativa adicionada (indentacao inconsistente, kwargs invalidos, target invalido de atribuicao).
- Suporte inicial a atribuicao composta e update (`+=`, `-=`, `++`, `--`) em identificador/atributo/indice.
- Suporte inicial a loops `while`/`until` com blocos por indentacao e forma inline com `then`.
- Suporte a `break` e `continue` em loops (`while`, `until`, `for`).
- Suporte a loops `for x in iterable` com blocos por indentacao.
- Erros explicitos para `break`/`continue` fora de loops.
- Suporte a loops `for k of obj` (apenas chaves) e `for k, v of obj` (chave-valor).
- Suporte a ranges `1..5` (inclusivo: [1,2,3,4,5]) e `1...5` (exclusivo: [1,2,3,4]).
- Ranges funcionam em expressoes e como iteraveis em for-loops.
- Destructuring de arrays `[a, b] = arr` com elementos em falta definidos como `None`.
- Destructuring de objetos `{x, y} = obj` e `{x: alias} = obj`.
- Destructuring aninhado suportado `[[a, b], c] = [[1, 2], 3]`.
- Classes com `class Name`, `extends Parent`, metodos e `constructor`.
- Instanciacao com `new ClassName(args)`.
- Acesso a `this` e `this.prop` (atributos de instancia).
- Atribuicao em `this.prop = value` funciona em metodos.
- Heranca com `extends` e metodos herdados.
- Tratamento de excecoes com `try/catch/finally` e `throw`.
- `switch x when ... then ... else ...` para condicionais multiplas.
- Multiplos casos em `when a, b, c`.
- Operador existencial `a ? b` (retorna a se nao for null, senao b).
- Acesso seguro `obj?.prop` (retorna null se obj for null).
- Atribuicao existencial `a ?= b` (atribui b apenas se a for null/undefined).
- Splat/rest em parametros `(args...) ->` captura argumentos restantes como array.
- Spread em chamadas `f(arr...)` expande array como argumentos.
- Interpolacao de strings `"Hello #{name}"` com expressoes.
- Operador `in` para verificacao de pertinencia (`x in arr`).
- Operador `of` para verificacao de chave (`k of obj`).
- Comprehensions `[x*2 for x in arr]` e com filtro `when`.
- Parametros default `(x = 10) ->` para funcoes.
- Block strings `"""multi line"""` com dedentacao automatica.
- Heregex `/// regex ///` com comentarios e whitespace ignorado.
- Slice syntax `arr[1..3]`, `arr[..2]`, `arr[3..]` para fatiar arrays/strings.
- REPL interativo com comandos `.exit`, `.help`, `.clear`.
- **NOVO**: Object comprehensions `{k: v for k, v of obj}` e com filtro `when`.
- **NOVO**: Splat em array destructuring `[a, b, rest...] = arr` captura elementos restantes.
- **NOVO**: `@param` shorthand em construtores: `constructor: (@name) ->` auto-atribui `this.name = name`.
- Cobertura de testes ampliada para lexer/parser e runtime (137 testes verdes).

Comando atual de testes:

- `python -m coffeepy.tests` (126 testes verdes)
