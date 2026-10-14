# ARRETADO 2.0 — Especificação da linguagem

Linguagem esotérica didática de propósito geral, inspirada em expressões
nordestinas. Programas usam a extensão `.arr` e são traduzidos para Python
3.10+ pelo `tradutor.py` (transpilador fonte-para-fonte; o Python é a
linguagem de destino e executa o `.py` gerado).

Fluxo: editar `.arr` → `python tradutor.py fonte.arr -o gerados/fonte.py` →
`python gerados/fonte.py`.

## Instalação

1. Instale Python 3.10+ (https://www.python.org/downloads/). VS Code é
   opcional — basta Python + terminal.
2. Abra um terminal na pasta `ARRETADO`.
3. Verifique com `python --version` (no Windows, `py --version` também vale).
4. Rode `python testar_tudo.py`.

## Estrutura do repositório

```
ARRETADO/
  tradutor.py     # tradutor .arr -> .py
  testar.py       # 3 programas do Projeto 1
  testar_tudo.py  # Projetos 1 + 2, limites e validação
  docs/           # esta documentação (substitui o antigo PDF)
  exemplos/       # Projeto 1 (.arr)
  projeto2/       # Projeto 2 (.arr)
  gerados/        # saída do tradutor (não versionada, vem vazia)
```

## Regras gerais

- Todo programa começa com `OXENTE` e termina com `CABOU`, únicos, nessa ordem.
- Linhas em branco são permitidas; comentários começam com `#`.
- Identificadores: letras ASCII, números e `_`, sem começar por número ou `_`.
- Blocos fecham com `FIM_ENQUANTO`, `FIM_SE` ou `FIM_FUNCAO`. A indentação
  organiza a leitura; os delimitadores definem o bloco.
- Funções vivem no nível principal e podem ser recursivas.
- Expressões: inteiros, decimais, textos entre aspas, booleanos, listas,
  acesso por índice, `+ - * / // %`, comparações `== != < <= > >=` e os
  operadores lógicos `and`, `or`, `not`, além de `TAMANHO()`, `TEXTO()`,
  `NUMERO()`.

## Dicionário de comandos

| Comando | Uso / finalidade |
|---|---|
| `OXENTE` / `CABOU` | Inicia / encerra o fonte `.arr` |
| `ARRE_EGUA expr` | Imprime expressão |
| `GUARDA x = expr` | Cria/atualiza variável |
| `LEIA_NUM x` / `LEIA_TEXTO x` | Lê inteiro / texto do teclado |
| `SE_AVEXE cond` | Início da decisão |
| `NUM_DEU` / `FIM_SE` | Caso contrário / fecha decisão |
| `ENQUANTO_TIVER cond` | Início do laço |
| `FIM_ENQUANTO` | Fecha laço |
| `MAIS_UM x` / `MENOS_UM x` | Soma / subtrai 1 |
| `PONHA lista expr` | Adiciona ao fim da lista |
| `TROQUE lista indice valor` | Substitui elemento |
| `TIRE lista indice` | Remove por posição |
| `FUNCAO nome(params)` / `FIM_FUNCAO` | Declara / encerra função |
| `DEVOLVE expr` / `CHAMA nome(args)` | Retorna valor / chama função |
| `JSON_CARREGA var "arq.json"` | Lê JSON ou lista vazia se ausente |
| `JSON_SALVA "arq.json" var` | Grava em JSON |
| `TAMANHO()` / `TEXTO()` / `NUMERO()` | Tamanho / converte p/ texto / inteiro |

## Identificadores x Python (mangling `arr_`)

Nomes que colidiriam no Python gerado (`class, def, print, len, True, ...`)
**são permitidos** na ARRETADO: o tradutor renomeia no `.py`
(`class` vira `arr_class`), de forma consistente na declaração e em todos
os usos — inclusive dentro de strings? Não: conteúdo de strings nunca é
tocado (`ARRE_EGUA "class"` imprime `class`).

Exceções:

- `and` / `or` / `not` são operadores lógicos da linguagem e não podem ser
  nomes de variáveis/funções.
- O prefixo `arr_` é reservado ao tradutor.

## Arquivos sem `open()`

O fonte `.arr` nunca usa `open()`: persistência é só `JSON_CARREGA` /
`JSON_SALVA`. O runtime injetado pelo tradutor usa `read_text` /
`write_text`, de modo que o código gerado não contém nenhuma chamada a
`open()`.

## Como o tradutor funciona

1. Lê o `.arr` em UTF-8; exige `OXENTE`/`CABOU`.
2. Pré-registra `FUNCAO`s (permite recursão) e coleta identificadores para
   o mangling `arr_`.
3. Valida cada expressão com `ast`: só tipos e operações da linguagem.
4. Emite Python equivalente com pilha de blocos (`if`/`while`/`def`) e
   confere os fechamentos; por fim compila para validar.
5. Grava o `.py` de `-o`.

## Limitações conhecidas

- Sem classes, dicionários literais, imports externos ou `try/except` no `.arr`.
- `LEIA_NUM` aceita inteiros; entrada inválida gera erro em execução.
- `JSON_CARREGA` supõe JSON válido quando o arquivo existe.
- Fibonacci adota F(1)=0 e F(2)=1 (ver `docs/projeto2.md`).
