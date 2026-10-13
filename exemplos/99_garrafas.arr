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
