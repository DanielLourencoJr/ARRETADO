# Projeto 1 — Linguagem + tradutor + 3 programas (entrega 18/11/2026)

Entregáveis do professor: documentação da linguagem (`docs/linguagem.md`),
tradutor (`tradutor.py`), três programas `.arr` e o passo a passo de
tradução/execução.

## 1. `ola_mundo.arr` — Hello World

```arr
# Primeiro programa ARRETADO
OXENTE
ARRE_EGUA "Hello World!"
CABOU
```

```bash
python tradutor.py exemplos/ola_mundo.arr -o gerados/ola_mundo.py
python gerados/ola_mundo.py
# Hello World!
```

## 2. `99_garrafas.arr` — 99 garrafas de cerveja

```arr
# A canção das 99 garrafas - versão simplificada
OXENTE
GUARDA garrafas = 99
ENQUANTO_TIVER garrafas > 0
    ARRE_EGUA garrafas
    SE_AVEXE garrafas == 1
        ARRE_EGUA "garrafa de cerveja na parede."
    NUM_DEU
        ARRE_EGUA "garrafas de cerveja na parede."
    FIM_SE
    ARRE_EGUA "Tire uma, passe adiante!"
    MENOS_UM garrafas
FIM_ENQUANTO
ARRE_EGUA "Nenhuma garrafa de cerveja na parede!"
CABOU
```

```bash
python tradutor.py exemplos/99_garrafas.arr -o gerados/99_garrafas.py
python gerados/99_garrafas.py
# 99 ... "Tire uma, passe adiante!" (x99) ... "Nenhuma garrafa de cerveja na parede!"
```

## 3. `programa_livre.arr` — placar nordestino

Soma 2× cada rodada, de 1 a 5. Pontuação final: 30.

```arr
# Mini-tabuleiro de pontuação nordestina
OXENTE
GUARDA pontos = 0
GUARDA rodada = 1
ENQUANTO_TIVER rodada <= 5
    ARRE_EGUA "Rodada:"
    ARRE_EGUA rodada
    GUARDA pontos = pontos + rodada * 2
    MAIS_UM rodada
FIM_ENQUANTO
SE_AVEXE pontos >= 20
    ARRE_EGUA "Arretado! Meta alcançada."
NUM_DEU
    ARRE_EGUA "Bora tentar de novo!"
FIM_SE
ARRE_EGUA "Pontuação final:"
ARRE_EGUA pontos
CABOU
```

```bash
python tradutor.py exemplos/programa_livre.arr -o gerados/programa_livre.py
python gerados/programa_livre.py
# ... "Arretado! Meta alcançada." ... "Pontuação final:" ... 30
```

## Verificação

```bash
python testar.py
# [OK] ola_mundo
# [OK] 99_garrafas
# [OK] programa_livre
```
