"""ARRETADO 2.0: tradutor de .arr para Python. Nenhum Python embutido no fonte .arr."""
import argparse
import ast
import io
import keyword
import re
import tokenize
from pathlib import Path

IDENT = r'[A-Za-z_][A-Za-z0-9_]*'
RESERVADOS = {'OXENTE','CABOU','ARRE_EGUA','GUARDA','ENQUANTO_TIVER','FIM_ENQUANTO','SE_AVEXE','NUM_DEU','FIM_SE','MAIS_UM','MENOS_UM','LEIA_NUM','LEIA_TEXTO','PONHA','TROQUE','TIRE','FUNCAO','FIM_FUNCAO','DEVOLVE','CHAMA','JSON_CARREGA','JSON_SALVA'}
FUNCOES = {'TAMANHO':'len', 'TEXTO':'str', 'NUMERO':'int'}
# Nomes do Python que colidiriam no código gerado (keywords + builtins do runtime).
# Em vez de proibir, o tradutor renomeia: `class` vira `arr_class` no .py gerado.
# `and`/`or`/`not` são exceção: são operadores lógicos da própria ARRETADO.
COLIDE_PY = set(keyword.kwlist) | {'print', 'len', 'str', 'int', 'list', 'dict', 'input', 'open', 'json', 'Path'}
OPERADORES = {'and', 'or', 'not'}
NOS = (ast.Expression, ast.Load, ast.Constant, ast.Name, ast.List, ast.Subscript, ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare, ast.Call, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.FloorDiv, ast.UAdd, ast.USub, ast.Not, ast.And, ast.Or, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE)

def py_nome(nome):
    """Nome seguro no Python gerado para um identificador ARRETADO."""
    return 'arr_' + nome if nome in COLIDE_PY else nome

def mangle_tokens(texto, linha, mangling):
    """Troca NAMEs declarados que colidem com o Python antes do parse.

    Usa tokens (não regex) para não tocar no conteúdo de strings:
    `ARRE_EGUA "class"` continua imprimindo `class`.
    """
    if not mangling:
        return texto
    try:
        toks = tokenize.generate_tokens(io.StringIO(texto.strip()).readline)
        saida = []
        for tk in toks:
            if tk.type == tokenize.NAME and tk.string in mangling:
                saida.append(tk._replace(string=py_nome(tk.string)))
            else:
                saida.append(tk)
        return tokenize.untokenize(saida)
    except (tokenize.TokenError, IndentationError) as e:
        raise ValueError(f'Linha {linha}: expressão inválida: {texto}') from e

def expr(texto, linha, permitir_funcoes=(), mangling=frozenset()):
    try:
        arvore = ast.parse(mangle_tokens(texto, linha, mangling), mode='eval')
    except SyntaxError as e:
        raise ValueError(f'Linha {linha}: expressão inválida: {texto}') from e
    permitidas = set(FUNCOES) | {py_nome(f) for f in permitir_funcoes}
    for no in ast.walk(arvore):
        if not isinstance(no, NOS):
            raise ValueError(f'Linha {linha}: construção proibida: {type(no).__name__}')
        if isinstance(no, ast.Constant) and type(no.value) not in (int, float, str, bool):
            raise ValueError(f'Linha {linha}: literal não suportado')
        if isinstance(no, ast.Name) and (no.id.startswith('_') or no.id in RESERVADOS):
            raise ValueError(f'Linha {linha}: identificador reservado: {no.id}')
        if isinstance(no, ast.Call):
            if not isinstance(no.func, ast.Name) or no.func.id not in permitidas or no.keywords:
                raise ValueError(f'Linha {linha}: chamada não declarada na ARRETADO')
    class Troca(ast.NodeTransformer):
        def visit_Call(self, no):
            self.generic_visit(no)
            if isinstance(no.func, ast.Name) and no.func.id in FUNCOES:
                no.func.id = FUNCOES[no.func.id]
            return no
    return ast.unparse(Troca().visit(arvore))

def nome_ok(nome, linha):
    if nome in OPERADORES:
        raise ValueError(f'Linha {linha}: `{nome}` é operador lógico, escolha outro nome')
    if not re.fullmatch(IDENT, nome) or nome.startswith('_') or nome.startswith('arr_') or nome in RESERVADOS or nome in FUNCOES:
        raise ValueError(f'Linha {linha}: identificador inválido: {nome}')

def coletar_nomes(linhas):
    """Pré-pass: todos os identificadores declarados (vars, funções, params).

    Permite renomear de forma consistente mesmo com uso antes da declaração,
    e renomear só o que foi declarado (literais True/False e operadores
    and/or/not continuam com o sentido da expressão).
    """
    nomes = set()
    for raw in linhas:
        s = raw.strip()
        if not s or s.startswith('#'):
            continue
        m = re.fullmatch(r'GUARDA\s+(' + IDENT + r')\s*=\s*(.+)', s)
        if m:
            nomes.add(m.group(1)); continue
        m = re.fullmatch(r'(MAIS_UM|MENOS_UM)\s+(' + IDENT + r')', s)
        if m:
            nomes.add(m.group(2)); continue
        m = re.fullmatch(r'LEIA_(?:NUM|TEXTO)\s+(' + IDENT + r')', s)
        if m:
            nomes.add(m.group(1)); continue
        m = re.fullmatch(r'PONHA\s+(' + IDENT + r')\s+(.+)', s)
        if m:
            nomes.add(m.group(1)); continue
        m = re.fullmatch(r'TROQUE\s+(' + IDENT + r')\s+([^ ]+)\s+(.+)', s)
        if m:
            nomes.add(m.group(1)); continue
        m = re.fullmatch(r'TIRE\s+(' + IDENT + r')\s+(.+)', s)
        if m:
            nomes.add(m.group(1)); continue
        m = re.fullmatch(r'JSON_CARREGA\s+(' + IDENT + r')\s+(.+)', s)
        if m:
            nomes.add(m.group(1)); continue
        m = re.fullmatch(r'JSON_SALVA\s+(.+?)\s+(' + IDENT + r')', s)
        if m:
            nomes.add(m.group(2)); continue
        m = re.fullmatch(r'FUNCAO\s+(' + IDENT + r')\(([^()]*)\)', s)
        if m:
            nomes.add(m.group(1))
            for x in m.group(2).split(','):
                x = x.strip()
                if x:
                    nomes.add(x)
    return nomes

def traduzir(texto):
    linhas = texto.splitlines()
    # Nomes declarados que colidem com o Python: renomear em todos os usos.
    mangling = frozenset(n for n in coletar_nomes(linhas) if n in COLIDE_PY - OPERADORES)
    # O runtime é implementado pelo tradutor; a interface pública da linguagem são os comandos JSON_*.
    # O fonte .arr nunca usa open(): só JSON_CARREGA/JSON_SALVA. O runtime usa
    # read_text/write_text para não expor open() no código gerado.
    out = [
        '# Gerado automaticamente a partir de um programa ARRETADO (.arr)',
        'import json as _ar_json',
        'from pathlib import Path as _ar_Path',
        'def _ar_carrega(caminho):',
        '    p = _ar_Path(caminho)',
        '    if not p.exists(): return []',
        '    return _ar_json.loads(p.read_text(encoding="utf-8"))',
        'def _ar_salva(caminho, dados):',
        '    p = _ar_Path(caminho)',
        '    p.parent.mkdir(parents=True, exist_ok=True)',
        '    p.write_text(_ar_json.dumps(dados, indent=2, ensure_ascii=False), encoding="utf-8")',
    ]
    pilha=[]; nivel=0; inicio=False; fim=False; funcoes=set()
    # Pré-cadastrar funções para chamadas recursivas.
    for i, raw in enumerate(linhas, 1):
        m=re.fullmatch(r'FUNCAO\s+('+IDENT+r')\(([^()]*)\)', raw.strip())
        if m:
            nome_ok(m.group(1),i)
            if m.group(1) in funcoes: raise ValueError(f'Linha {i}: função duplicada')
            funcoes.add(m.group(1))
    for i, raw in enumerate(linhas, 1):
        s=raw.strip()
        if not s or s.startswith('#'): continue
        if fim: raise ValueError(f'Linha {i}: conteúdo depois de CABOU')
        if s=='OXENTE':
            if inicio: raise ValueError(f'Linha {i}: OXENTE repetido')
            inicio=True; continue
        if not inicio: raise ValueError(f'Linha {i}: esperado OXENTE')
        if s=='CABOU':
            if pilha: raise ValueError(f'Linha {i}: bloco pendente {pilha[-1][0]}')
            fim=True; continue
        def em(c): out.append('    '*nivel+c)
        def e(t): return expr(t,i,funcoes,mangling)
        if s.startswith('ARRE_EGUA '): em('print('+e(s[9:].strip())+')')
        elif m:=re.fullmatch(r'GUARDA\s+('+IDENT+r')\s*=\s*(.+)', s):
            nome_ok(m[1],i); em(py_nome(m[1])+' = '+e(m[2]))
        elif m:=re.fullmatch(r'(MAIS_UM|MENOS_UM)\s+('+IDENT+r')',s):
            nome_ok(m[2],i); em(py_nome(m[2])+' '+('+' if m[1]=='MAIS_UM' else '-')+'= 1')
        elif m:=re.fullmatch(r'LEIA_(NUM|TEXTO)\s+('+IDENT+r')',s):
            nome_ok(m[2],i); em(py_nome(m[2])+' = '+('int(input())' if m[1]=='NUM' else 'input()'))
        elif m:=re.fullmatch(r'PONHA\s+('+IDENT+r')\s+(.+)',s):
            nome_ok(m[1],i); em(py_nome(m[1])+'.append('+e(m[2])+')')
        elif m:=re.fullmatch(r'TROQUE\s+('+IDENT+r')\s+([^ ]+)\s+(.+)',s):
            nome_ok(m[1],i); em(py_nome(m[1])+'['+e(m[2])+'] = '+e(m[3]))
        elif m:=re.fullmatch(r'TIRE\s+('+IDENT+r')\s+(.+)',s):
            nome_ok(m[1],i); em(py_nome(m[1])+'.pop('+e(m[2])+')')
        elif m:=re.fullmatch(r'JSON_CARREGA\s+('+IDENT+r')\s+(.+)',s):
            nome_ok(m[1],i); em(py_nome(m[1])+' = _ar_carrega('+e(m[2])+')')
        elif m:=re.fullmatch(r'JSON_SALVA\s+(.+?)\s+('+IDENT+r')',s):
            nome_ok(m[2],i); em('_ar_salva('+e(m[1])+', '+py_nome(m[2])+')')
        elif s.startswith('ENQUANTO_TIVER '):
            em('while '+e(s[len('ENQUANTO_TIVER '):])+':'); pilha.append(('while',i,False)); nivel+=1
        elif s=='FIM_ENQUANTO':
            if not pilha or pilha[-1][0]!='while': raise ValueError(f'Linha {i}: FIM_ENQUANTO sem ENQUANTO_TIVER')
            pilha.pop(); nivel-=1
        elif s.startswith('SE_AVEXE '):
            em('if '+e(s[len('SE_AVEXE '):])+':'); pilha.append(('if',i,False)); nivel+=1
        elif s=='NUM_DEU':
            if not pilha or pilha[-1][0]!='if' or pilha[-1][2]: raise ValueError(f'Linha {i}: NUM_DEU inválido')
            nivel-=1; em('else:'); nivel+=1; pilha[-1]=('if',pilha[-1][1],True)
        elif s=='FIM_SE':
            if not pilha or pilha[-1][0]!='if': raise ValueError(f'Linha {i}: FIM_SE inválido')
            pilha.pop(); nivel-=1
        elif m:=re.fullmatch(r'FUNCAO\s+('+IDENT+r')\(([^()]*)\)',s):
            if pilha or nivel: raise ValueError(f'Linha {i}: função deve ser de nível superior')
            params=[x.strip() for x in m[2].split(',') if x.strip()]
            if len(set(params))!=len(params): raise ValueError(f'Linha {i}: parâmetro repetido')
            for x in params: nome_ok(x,i)
            em('def '+py_nome(m[1])+'('+', '.join(py_nome(x) for x in params)+'):'); pilha.append(('func',i,False)); nivel+=1
        elif s=='FIM_FUNCAO':
            if not pilha or pilha[-1][0]!='func': raise ValueError(f'Linha {i}: FIM_FUNCAO inválido')
            pilha.pop(); nivel-=1
        elif s.startswith('DEVOLVE '):
            if not any(b[0]=='func' for b in pilha): raise ValueError(f'Linha {i}: DEVOLVE fora de função')
            em('return '+e(s[8:]))
        elif s.startswith('CHAMA '):
            chamada=s[6:]; arv=ast.parse(e(chamada),mode='eval').body
            if not isinstance(arv,ast.Call) or not isinstance(arv.func,ast.Name) or arv.func.id not in {py_nome(f) for f in funcoes}:
                raise ValueError(f'Linha {i}: CHAMA exige função ARRETADO declarada')
            em(e(chamada))
        else: raise ValueError(f'Linha {i}: comando desconhecido: {s}')
    if not inicio or not fim: raise ValueError('Programa precisa de OXENTE e CABOU')
    codigo='\n'.join(out)+'\n'
    try: compile(codigo,'<ARRETADO>','exec')
    except SyntaxError as ex: raise ValueError('Bloco vazio ou construção incompleta') from ex
    return codigo

def main():
    p=argparse.ArgumentParser(description='Tradutor ARRETADO (.arr → .py)')
    p.add_argument('arquivo',type=Path); p.add_argument('-o','--saida',type=Path)
    args=p.parse_args()
    if args.arquivo.suffix.lower()!='.arr': p.error('Somente arquivos .arr')
    try:
        destino=args.saida or args.arquivo.with_suffix('.py')
        codigo=traduzir(args.arquivo.read_text(encoding='utf-8'))
        destino.parent.mkdir(parents=True,exist_ok=True)
        destino.write_text(codigo,encoding='utf-8')
    except (ValueError,OSError,UnicodeError) as ex: p.exit(1,f'Erro: {ex}\n')
    print('Tradução concluída:', destino)
if __name__=='__main__': main()
