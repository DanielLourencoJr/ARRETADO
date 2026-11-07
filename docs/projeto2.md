# Projeto 2 — 5 algoritmos em ARRETADO (entrega 02/12/2026)

Regra do professor: qualquer construção fora da linguagem criada gera
demérito (ex.: usar `open` do Python em vez da função de arquivos da
linguagem). Os fontes abaixo usam **só** comandos ARRETADO; arquivos passam
por `JSON_CARREGA`/`JSON_SALVA`.

## Q1. Fatorial de N (0 a 15)

```arr
# Fatorial de N entre 0 e 15
OXENTE
ARRE_EGUA "Digite N (0 a 15):"
LEIA_NUM n
SE_AVEXE n < 0 or n > 15
    ARRE_EGUA "N fora do intervalo permitido"
NUM_DEU
    GUARDA produto = 1
    GUARDA i = 2
    ENQUANTO_TIVER i <= n
        GUARDA produto = produto * i
        MAIS_UM i
    FIM_ENQUANTO
    ARRE_EGUA produto
FIM_SE
CABOU
```

```bash
python tradutor.py projeto2/01_fatorial.arr -o gerados/01_fatorial.py
python gerados/01_fatorial.py
# N=0 -> 1 | N=6 -> 720 | N=15 -> 1307674368000 | N=16 -> "N fora do intervalo permitido"
```

## Q2. Fibonacci, posições 1 a 10 (convenção F(1)=0, F(2)=1)

```arr
# Sequência começa em F(1)=0 e F(2)=1
OXENTE
ARRE_EGUA "Digite N (1 a 10):"
LEIA_NUM n
SE_AVEXE n < 1 or n > 10
    ARRE_EGUA "N fora do intervalo permitido"
NUM_DEU
    GUARDA a = 0
    GUARDA b = 1
    GUARDA i = 1
    ENQUANTO_TIVER i < n
        GUARDA proximo = a + b
        GUARDA a = b
        GUARDA b = proximo
        MAIS_UM i
    FIM_ENQUANTO
    ARRE_EGUA a
FIM_SE
CABOU
```

```bash
python tradutor.py projeto2/02_fibonacci.arr -o gerados/02_fibonacci.py
python gerados/02_fibonacci.py
# N=1 -> 0 | N=4 -> 2 | N=10 -> 34 | N=11 -> "N fora do intervalo permitido"
```

## Q3. Torre de Hanói, 6 discos (63 = 2^6 − 1 movimentos)

```arr
# Estratégia recursiva ótima: 2^6 - 1 = 63 movimentos
OXENTE
FUNCAO mover(n, origem, destino, auxiliar)
    SE_AVEXE n == 1
        ARRE_EGUA "Disco 1: " + origem + " -> " + destino
    NUM_DEU
        CHAMA mover(n - 1, origem, auxiliar, destino)
        ARRE_EGUA "Disco " + TEXTO(n) + ": " + origem + " -> " + destino
        CHAMA mover(n - 1, auxiliar, destino, origem)
    FIM_SE
FIM_FUNCAO
CHAMA mover(6, "A", "C", "B")
CABOU
```

```bash
python tradutor.py projeto2/03_hanoi.arr -o gerados/03_hanoi.py
python gerados/03_hanoi.py   # 63 linhas, de A para C
```

## Q4. Ordenação (bubble sort, N < 100)

```arr
# Bubble sort para N < 100 inteiros
OXENTE
ARRE_EGUA "Digite N (0 a 99):"
LEIA_NUM n
SE_AVEXE n < 0 or n >= 100
    ARRE_EGUA "N fora do intervalo permitido"
NUM_DEU
    GUARDA numeros = []
    GUARDA i = 0
    ENQUANTO_TIVER i < n
        LEIA_NUM valor
        PONHA numeros valor
        MAIS_UM i
    FIM_ENQUANTO
    GUARDA i = 0
    ENQUANTO_TIVER i < n
        GUARDA j = 0
        ENQUANTO_TIVER j < n - 1 - i
            SE_AVEXE numeros[j] > numeros[j + 1]
                GUARDA temp = numeros[j]
                TROQUE numeros j numeros[j + 1]
                TROQUE numeros (j+1) temp
            FIM_SE
            MAIS_UM j
        FIM_ENQUANTO
        MAIS_UM i
    FIM_ENQUANTO
    ARRE_EGUA numeros
FIM_SE
CABOU
```

```bash
python tradutor.py projeto2/04_ordenacao.arr -o gerados/04_ordenacao.py
python gerados/04_ordenacao.py
# N=0 -> [] | 5 valores 7 -5 7 0 3 -> [-5, 0, 3, 7, 7]
```

## Q5. CRUD persistente em JSON (lista de nomes)

```arr
# CRUD de nomes persistente em registros.json; sem Python no código .arr
OXENTE
JSON_CARREGA registros "registros.json"
GUARDA opcao = -1
ENQUANTO_TIVER opcao != 0
    ARRE_EGUA "0=Sair  1=Criar  2=Listar  3=Atualizar  4=Excluir"
    LEIA_NUM opcao
    SE_AVEXE opcao == 1
        ARRE_EGUA "Nome para adicionar:"
        LEIA_TEXTO nome
        PONHA registros nome
        JSON_SALVA "registros.json" registros
        ARRE_EGUA "Adicionado"
    FIM_SE
    SE_AVEXE opcao == 2
        GUARDA i = 0
        ENQUANTO_TIVER i < TAMANHO(registros)
            ARRE_EGUA TEXTO(i) + ": " + registros[i]
            MAIS_UM i
        FIM_ENQUANTO
    FIM_SE
    SE_AVEXE opcao == 3
        ARRE_EGUA "Índice a atualizar:"
        LEIA_NUM indice
        SE_AVEXE indice >= 0 and indice < TAMANHO(registros)
            ARRE_EGUA "Novo nome:"
            LEIA_TEXTO nome
            TROQUE registros indice nome
            JSON_SALVA "registros.json" registros
            ARRE_EGUA "Atualizado"
        NUM_DEU
            ARRE_EGUA "Índice inválido"
        FIM_SE
    FIM_SE
    SE_AVEXE opcao == 4
        ARRE_EGUA "Índice a excluir:"
        LEIA_NUM indice
        SE_AVEXE indice >= 0 and indice < TAMANHO(registros)
            TIRE registros indice
            JSON_SALVA "registros.json" registros
            ARRE_EGUA "Excluído"
        NUM_DEU
            ARRE_EGUA "Índice inválido"
        FIM_SE
    FIM_SE
FIM_ENQUANTO
CABOU
```

```bash
python tradutor.py projeto2/05_crud_json.arr -o gerados/05_crud_json.py
python gerados/05_crud_json.py
```

O `registros.json` é criado no diretório **atual de execução**; índices
fora da lista mostram `Índice inválido`. Para limpar dados de teste, apague
o `registros.json`.

## Verificação

```bash
python testar_tudo.py
# TODOS OS TESTES PASSARAM: 3 programas do Projeto 1 + 5 do Projeto 2, limites e validação.
```
