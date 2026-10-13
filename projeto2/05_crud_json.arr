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
