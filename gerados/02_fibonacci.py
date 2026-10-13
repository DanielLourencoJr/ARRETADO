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
print('Digite N (1 a 10):')
n = int(input())
if n < 1 or n > 10:
    print('N fora do intervalo permitido')
else:
    a = 0
    b = 1
    i = 1
    while i < n:
        proximo = a + b
        a = b
        b = proximo
        i += 1
    print(a)
