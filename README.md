# CoffeePy

Reinicio oficial do projeto.

Este repositorio foi resetado para comecar do zero com um objetivo unico:

- Escrever codigo em sintaxe CoffeeScript (`.coffee`)
- Executar em runtime Python nativo
- Usar ecossistema Python (stdlib + libs externas)
- Sem transpilar para JavaScript
- Sem dependencia de Node para executar programas

## Estado atual

Projeto em fase **bootstrap**.

- Arquitetura anterior foi descartada
- Replanejamento feito para Python-first
- Base de codigo reiniciada
- Referencia oficial de sintaxe/tests restaurada em `references/coffeescript/` (uso de referencia, nao de runtime)
- Primeira execucao funcional bootstrap implementada (lexer/parser/interpreter/CLI iniciais)

## Proximo passo

Consulte `PYTHON_ENGINE_TASKS.md` para o plano oficial de reconstrucao.

## Bootstrap atual (ja funcional)

- `import` e `from ... import ...` basicos
- atribuicoes em identificador, atributo e indice (`x = ...`, `obj.a = ...`, `arr[0] = ...`)
- atribuicoes compostas e update (`+=`, `-=`, `++`, `--`)
- aritmetica basica (`+`, `-`, `*`, `/`, `%`, `**`)
- comparacoes (`<`, `<=`, `>`, `>=`, `==`, `!=`) e logica (`and`, `or`, `not`)
- acesso por atributo (`obj.prop`)
- acesso por indice (`arr[0]`) e literais `[]`/`{}`
- chamadas explicitas (`fn(...)`) e implicitas simples (`fn x`)
- kwargs em chamada explicita (`fn(a=1, b=2)`)
- condicionais em expressao (`if ... then ... else ...`, postfix `if/unless`)
- loops basicos (`while` e `until`) com bloco por indentacao e forma `then`
- funcoes literais (`x -> expr`, `(x, y) -> expr`, `-> expr`)
- `return` em corpo de funcao
- blocos multiline por indentacao para `if` e corpo de funcao

Exemplo rapido:

```coffee
from math import sqrt
x = sqrt 81
print x
```

Exemplo multiline:

```coffee
double_then_add = (x, y) ->
  z = x * 2
  z + y

if true
  print double_then_add 5, 3
else
  print 0
```

Rodar:

```bash
python -m coffeepy --eval "from math import sqrt; print sqrt 81"
python -m coffeepy caminho/do/arquivo.coffee
```

Testes:

```bash
python -m coffeepy.tests
```

Status atual da suite bootstrap: 50 testes passando.

## Referencia de linguagem

- O codigo oficial do CoffeeScript fica em `references/coffeescript/` para consulta de sintaxe, parser e testes.
- Essa pasta e usada como **fonte de referencia tecnica**, nao como dependencia de execucao do CoffeePy.
- Contrato atual da linguagem (Python-first) em `docs/COFFEEPY_LANGUAGE_CONTRACT_V0.md`.
