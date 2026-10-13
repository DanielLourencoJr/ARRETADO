# ARRETADO 2.0 — Projetos 1 e 2

Linguagem esotérica de propósito geral **didático**, inspirada na cultura nordestina. Programas `.arr` são traduzidos para Python 3.10+ pelo `tradutor.py`.

## Instalação

1. Instale Python 3.10+ em https://www.python.org/downloads/ e VS Code em https://code.visualstudio.com/.
2. Extraia o ZIP, abra a pasta `ARRETADO` no VS Code e abra **Terminal > Novo Terminal**.
3. Verifique `python --version` (Windows também pode usar `py --version`).
4. Teste tudo: `python testar_tudo.py`.

## Projeto 1

```
python tradutor.py exemplos/ola_mundo.arr -o gerados/ola_mundo.py
python gerados/ola_mundo.py
python tradutor.py exemplos/99_garrafas.arr -o gerados/99_garrafas.py
python gerados/99_garrafas.py
python tradutor.py exemplos/programa_livre.arr -o gerados/programa_livre.py
python gerados/programa_livre.py
```

## Projeto 2

```
python tradutor.py projeto2/01_fatorial.arr -o gerados/01_fatorial.py
python gerados/01_fatorial.py
python tradutor.py projeto2/02_fibonacci.arr -o gerados/02_fibonacci.py
python gerados/02_fibonacci.py
python tradutor.py projeto2/03_hanoi.arr -o gerados/03_hanoi.py
python gerados/03_hanoi.py
python tradutor.py projeto2/04_ordenacao.arr -o gerados/04_ordenacao.py
python gerados/04_ordenacao.py
python tradutor.py projeto2/05_crud_json.arr -o gerados/05_crud_json.py
python gerados/05_crud_json.py
```

O programa CRUD cria `registros.json` no diretório **atual de execução** e mantém a lista quando aberto novamente. Para apagar os dados de teste, exclua o arquivo `registros.json`.

## Sintaxe resumida

- `OXENTE` e `CABOU`: início/fim obrigatórios, únicos.
- `ARRE_EGUA expr`: imprime expressão.
- `GUARDA nome = expr`: atribui valor.
- `LEIA_NUM nome`, `LEIA_TEXTO nome`: lê número inteiro ou texto.
- `SE_AVEXE cond`, `NUM_DEU`, `FIM_SE`: decisão.
- `ENQUANTO_TIVER cond`, `FIM_ENQUANTO`: repetição.
- `MAIS_UM nome`, `MENOS_UM nome`: incrementa/decrementa.
- `PONHA lista expr`: insere no fim da lista.
- `TROQUE lista indice valor`: substitui item de lista.
- `TIRE lista indice`: remove item por posição.
- `FUNCAO nome(params)`, `FIM_FUNCAO`, `DEVOLVE expr`, `CHAMA nome(args)`: função com recursão.
- `JSON_CARREGA variavel "arquivo.json"`: lê dados ou retorna lista vazia se o arquivo não existir.
- `JSON_SALVA "arquivo.json" variavel`: grava em formato JSON.
- Expressões incluem inteiros, decimais, textos, booleanos, listas, índices, `+ - * / // %`, comparações, `and or not` e funções nativas da ARRETADO `TAMANHO()`, `TEXTO()`, `NUMERO()`.

## Limitações

- Nesta versão, a linguagem é didática e não possui classes, dicionários literais, módulos de terceiros ou tratamento de exceção no código `.arr`.
- `LEIA_NUM` aceita inteiros. Entrada inválida pode ocasionar erro em tempo de execução.
- `JSON_CARREGA` supõe JSON válido quando o arquivo existe.
- O projeto 2 opta por uma lista JSON de **nomes (strings)**, que constitui uma lista de informações para CRUD.
- As funções devem ser declaradas no nível principal antes das chamadas que as utilizam durante a execução.
- A sequência de Fibonacci usa F(1)=0 e F(2)=1; a documentação informa explicitamente essa convenção.

## Entrega

O trabalho original solicita documentação, tradutor, fontes dos programas e instruções. Utilize também o PDF `Manual_Completo_ARRETADO_Projetos_1_e_2.pdf`.

## Execução no Windows (acentos e UTF-8)

O arquivo `testar_tudo.py` força `PYTHONIOENCODING=utf-8` nos programas gerados. Isso evita `UnicodeDecodeError` no Windows com Python 3.14 e páginas de código locais. Rode `py -3 testar_tudo.py` ou `python testar_tudo.py` dentro da pasta ARRETADO.
