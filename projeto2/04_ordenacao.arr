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
