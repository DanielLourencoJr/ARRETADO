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
