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
pontos = 0
rodada = 1
while rodada <= 5:
    print('Rodada:')
    print(rodada)
    pontos = pontos + rodada * 2
    rodada += 1
if pontos >= 20:
    print('Arretado! Meta alcançada.')
else:
    print('Bora tentar de novo!')
print('Pontuação final:')
print(pontos)
