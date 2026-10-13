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
