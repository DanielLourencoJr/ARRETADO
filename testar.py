from pathlib import Path
import subprocess
import sys
import os
from tradutor import traduzir

base = Path(__file__).resolve().parent
for nome in ('ola_mundo','99_garrafas','programa_livre'):
    fonte = base / 'exemplos' / f'{nome}.arr'
    destino = base / 'gerados' / f'{nome}.py'
    destino.parent.mkdir(exist_ok=True)
    destino.write_text(traduzir(fonte.read_text(encoding='utf-8')), encoding='utf-8')
    ambiente = os.environ.copy()
    ambiente['PYTHONIOENCODING'] = 'utf-8'
    execucao = subprocess.run(
        [sys.executable, str(destino)],
        capture_output=True, text=True, check=True, encoding='utf-8',
        errors='strict', env=ambiente, timeout=15
    )
    if nome == 'ola_mundo':
        assert execucao.stdout.strip() == 'Hello World!'
    elif nome == '99_garrafas':
        assert execucao.stdout.count('Tire uma, passe adiante!') == 99
        assert 'Nenhuma garrafa' in execucao.stdout
    else:
        assert 'Meta alcançada' in execucao.stdout and execucao.stdout.strip().endswith('30')
    print(f'[OK] {nome}')
print('Todos os três testes passaram.')
