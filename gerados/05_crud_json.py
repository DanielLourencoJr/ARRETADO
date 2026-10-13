# Gerado automaticamente a partir de um programa ARRETADO (.arr)
import json as _ar_json
from pathlib import Path as _ar_Path
def _ar_carrega(caminho):
    p = _ar_Path(caminho)
    if not p.exists(): return []
    with p.open("r", encoding="utf-8") as f: return _ar_json.load(f)
def _ar_salva(caminho, dados):
    p = _ar_Path(caminho)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f: _ar_json.dump(dados, f, indent=2, ensure_ascii=False)
registros = _ar_carrega('registros.json')
opcao = -1
while opcao != 0:
    print('0=Sair  1=Criar  2=Listar  3=Atualizar  4=Excluir')
    opcao = int(input())
    if opcao == 1:
        print('Nome para adicionar:')
        nome = input()
        registros.append(nome)
        _ar_salva('registros.json', registros)
        print('Adicionado')
    if opcao == 2:
        i = 0
        while i < len(registros):
            print(str(i) + ': ' + registros[i])
            i += 1
    if opcao == 3:
        print('Índice a atualizar:')
        indice = int(input())
        if indice >= 0 and indice < len(registros):
            print('Novo nome:')
            nome = input()
            registros[indice] = nome
            _ar_salva('registros.json', registros)
            print('Atualizado')
        else:
            print('Índice inválido')
    if opcao == 4:
        print('Índice a excluir:')
        indice = int(input())
        if indice >= 0 and indice < len(registros):
            registros.pop(indice)
            _ar_salva('registros.json', registros)
            print('Excluído')
        else:
            print('Índice inválido')
