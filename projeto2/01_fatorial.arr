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
