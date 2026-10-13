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
