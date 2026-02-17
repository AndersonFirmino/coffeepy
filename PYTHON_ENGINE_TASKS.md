# CoffeePy - Plano de Reconstrucao (Zero)

Objetivo do produto:

- Aceitar arquivos `.coffee` com sintaxe CoffeeScript.
- Interpretar diretamente em Python (runtime nativo).
- Dar acesso ao ecossistema Python (imports, bibliotecas, objetos, excecoes).
- Nao transpilar para JavaScript.
- Nao depender de Node para execucao.

## Status geral

- Progresso atual: **54%**
- Restante: **46%**
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

1. Implementar loops (`while`/`until`) com blocos por indentacao.
2. Adicionar `return` com expressao multiline e regras de parse mais robustas.
3. Expandir interop Python para colecoes mais ricas (tupla/set e chamadas com kwargs em mais formas).
4. Consolidar suite negativa de parser/runtime para erros de chamada e atribuicao invalida.

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
- Cobertura de testes ampliada para lexer/parser e runtime (44 testes verdes).

Comando atual de testes:

- `python -m coffeepy.tests`
