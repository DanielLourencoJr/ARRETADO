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
print('Hello World!')
