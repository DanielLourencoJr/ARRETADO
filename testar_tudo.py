"""Testes integrados dos projetos 1 e 2."""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from tradutor import traduzir

BASE = Path(__file__).resolve().parent

def executar(nome, entrada='', pasta=None):
    origem = BASE / ('projeto2' if nome.startswith(('01_', '02_', '03_', '04_', '05_')) else 'exemplos') / f'{nome}.arr'
    compilado = BASE / 'gerados' / f'{nome}.py'
    compilado.parent.mkdir(exist_ok=True)
    compilado.write_text(traduzir(origem.read_text(encoding='utf-8')), encoding='utf-8')
    ambiente = os.environ.copy()
    # Força UTF-8 na saída do Python filho, inclusive no Windows (cp1252/cp850).
    ambiente['PYTHONIOENCODING'] = 'utf-8'
    resultado = subprocess.run([sys.executable, str(compilado)], input=entrada,
                               text=True, capture_output=True, cwd=pasta or BASE,
                               encoding='utf-8', errors='strict', env=ambiente, timeout=15)
    assert resultado.returncode == 0, resultado.stderr
    return resultado.stdout

assert executar('ola_mundo').strip() == 'Hello World!'
assert executar('99_garrafas').count('Tire uma, passe adiante!') == 99
assert executar('programa_livre').strip().endswith('30')
assert executar('01_fatorial','0\n').strip().endswith('1')
assert executar('01_fatorial','15\n').strip().endswith('1307674368000')
assert executar('01_fatorial','16\n').strip().endswith('N fora do intervalo permitido')
assert executar('02_fibonacci','1\n').strip().endswith('0')
assert executar('02_fibonacci','10\n').strip().endswith('34')
assert executar('02_fibonacci','11\n').strip().endswith('N fora do intervalo permitido')
assert len(executar('03_hanoi').splitlines()) == 63
assert executar('04_ordenacao','5\n7\n-5\n7\n0\n3\n').strip().endswith('[-5, 0, 3, 7, 7]')
assert executar('04_ordenacao','0\n').strip().endswith('[]')
with tempfile.TemporaryDirectory() as d:
    saida = executar('05_crud_json','1\nMaria\n1\nJoao\n3\n1\nJose\n4\n0\n2\n0\n',d)
    assert json.loads((Path(d)/'registros.json').read_text(encoding='utf-8'))==['Jose']
    assert '0: Jose' in saida
try:
    traduzir('OXENTE\nARRE_EGUA __import__("os")\nCABOU')
except ValueError:
    pass
else:
    raise AssertionError('A linguagem aceitou execução arbitrária')
print('TODOS OS TESTES PASSARAM: 3 programas do Projeto 1 + 5 do Projeto 2, limites e validação.')
