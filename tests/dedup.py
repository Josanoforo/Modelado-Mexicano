import json, re, unicodedata, collections, yaml
import os, sys
RAIZ = os.environ.get('MM_RAIZ') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INV  = os.path.join(RAIZ, 'data', 'inventarios')
OUT  = os.path.join(RAIZ, 'data')
ALIAS = os.path.join(INV, 'alias-fuentes.yaml')
if not os.path.isdir(INV):
    sys.exit(f"NO ENCONTRÉ {INV} — este script se corre desde un clon del repo con los "
             f"inventarios en data/inventarios/, o con MM_RAIZ apuntando a la raíz.")

d = json.load(open(os.path.join(OUT,'catalogo_derivado.json')))
F_TODAS = d['fuentes']
# tests/catalogo.py ya no inventa identidad para un título que no resuelve
# contra la tabla de alias (acronimo=None) -- este script hereda esa señal:
# se excluyen del dedup (akey()/unicodedata no operan sobre None) y se
# imprime el conteo antes que cualquier otra cifra, mismo criterio que
# tests/catalogo.py.
F = [r for r in F_TODAS if r['acronimo'] is not None]
SIN_RESOLVER_HEREDADO = len(F_TODAS) - len(F)
print(f"SIN_RESOLVER (heredado de catalogo.py, excluidas del dedup): {SIN_RESOLVER_HEREDADO}")

def norm(s):
    s = re.sub(r'\*\*.*?\*\*','',s)
    s = re.sub(r'\(.*?\)','',s)
    s = re.split(r'[—–]|\s-\s', s)[0]
    s = unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode()
    s = re.sub(r'[^a-z0-9 ]',' ', s.lower())
    s = re.sub(r'\b(encuesta|nacional|de|del|la|el|los|las|y|en|sobre|para|mexico|censo)\b',' ',s)
    return re.sub(r'\s+',' ',s).strip()

# [ENCARGO REPAIR-1, 2026-08-06, Tarea 4] caso de prueba: PR #147 declaró
# que encode('ascii','ignore') corría antes del split en em-dash y lo
# borraba, dejando ese corte muerto -- nunca disparaba. Dos títulos reales
# de data/catalogo_derivado.json (WVS) que solo difieren tras un em-dash
# deben normalizar igual una vez que el corte esté vivo.
_prueba_norm_emdash_a = norm('World Values Survey (WVS) — muestra de México')
_prueba_norm_emdash_b = norm('World Values Survey (WVS) — olas de México')
assert _prueba_norm_emdash_a == _prueba_norm_emdash_b, (
    f"corte en em-dash sigue muerto: {_prueba_norm_emdash_a!r} != {_prueba_norm_emdash_b!r}")
def akey(a):
    a = unicodedata.normalize('NFKD', a).encode('ascii','ignore').decode()
    return re.split(r'\s*/\s*', a.strip())[0].strip()

parent={}
def find(x):
    parent.setdefault(x,x)
    while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
    return x
def union(a,b):
    ra,rb=find(a),find(b)
    if ra!=rb: parent[rb]=ra

for i,r in enumerate(F):
    k='I%d'%i; find(k)
    union('A:'+akey(r['acronimo']), k)
    n=norm(r['titulo'])
    if len(n)>3: union('A:'+akey(r['acronimo']), 'N:'+n)

groups=collections.defaultdict(list)
for i,r in enumerate(F): groups[find('I%d'%i)].append(r)

print(f"ENTRADAS: {len(F)}    FUENTES ÚNICAS tras dedup por acrónimo+nombre: {len(groups)}")
rows=[]
for g in groups.values():
    ac = sorted({x['acronimo'] for x in g}, key=len)[0]
    tit = max((x['titulo'] for x in g), key=len)
    doms = sorted({x['dominio'] for x in g})
    micro = 'sí' if any(re.match(r'\s*\**s[ií]', x['microdatos'] or '', re.I) for x in g) else \
            ('no' if any(re.match(r'\s*\**no', x['microdatos'] or '', re.I) for x in g) else '?')
    libre = 'sí' if any(re.search(r'directa|sin registro|abierto|^\s*\**no\b|p[uú]blic', x['acceso'] or '', re.I) for x in g) else '?'
    inst = next((x['institucion'] for x in g if x['institucion']), '')
    rows.append(dict(acronimo=ac, titulo=tit, n_dom=len(doms), dominios=doms, micro=micro, libre=libre, inst=inst))
rows.sort(key=lambda r:(-r['n_dom'], r['acronimo']))
print(f"MICRODATOS sí={sum(1 for r in rows if r['micro']=='sí')} no={sum(1 for r in rows if r['micro']=='no')} ?={sum(1 for r in rows if r['micro']=='?')}")
op=[r for r in rows if r['micro']=='sí' and r['libre']=='sí']
print(f"OPERABLES (microdatos + acceso libre): {len(op)}")
print(f"TRANSVERSALES (3+ dominios): {sum(1 for r in rows if r['n_dom']>=3)}   mono-dominio: {sum(1 for r in rows if r['n_dom']==1)}")
print("\n== ESPINA DORSAL: 3+ dominios ==")
for r in rows:
    if r['n_dom']>=3: print(f"  {r['n_dom']}d  micro={r['micro']:2s} libre={r['libre']:2s}  {r['acronimo']:16s} {r['titulo'][:60]}")

# --- cruce contra el manifiesto: qué del catálogo ya está en disco ---
# ENCARGO MAP-1: el emparejamiento pasa ahora por la tabla de alias
# (data/inventarios/alias-fuentes.yaml) en vez del heurístico de prefijos
# de acrónimo sueltos que se comparaba contra el acronimo (ya) fragmentado
# de catalogo.py. Sigue siendo aproximado -- la versión exacta, mantenida a
# mano, vive en tests/cruce_operables.py (fuera del perímetro de este acto).
# Un id de manifiesto que no empareja con ninguna fuente canónica va a su
# propia lista (MANIFEST_SIN_MATCH) y se cuenta, no se descarta en silencio.
def ascii_up(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().upper()

def prefijos_id(mid):
    """Mismo criterio que la versión anterior: si el id empieza con letra,
    su corrida de letras iniciales; si empieza con dígito (ordinal de
    documento multi-parte, p.ej. `1_vfinal_..._ensanut_2024_...`), todas las
    palabras del id -- la significativa no está al inicio."""
    m = re.match(r'^[a-z]+', mid)
    if m: return {m.group(0).upper()}
    return {tok.upper() for tok in re.findall(r'[a-z]+', mid)}

ALIAS_ENTRADAS = yaml.safe_load(open(ALIAS, encoding='utf-8')) or [] if os.path.isfile(ALIAS) else []
tokens_por_canon = {}
for e in ALIAS_ENTRADAS:
    toks = {ascii_up(e['canonico'].split('/')[0].strip())}
    for al in e.get('alias', []):
        al_n = al.strip()
        # solo siglas cortas como blanco de emparejamiento contra ids -- un
        # truncamiento largo de rama-fallback nunca aparece tal cual en un id
        if al_n and len(al_n) <= 12 and '/' not in al_n:
            toks.add(ascii_up(al_n))
    tokens_por_canon[e['canonico']] = {t for t in toks if len(t) >= 2}

MAN = os.path.join(OUT, 'manifiesto.yaml')
en_disco = set()
id_a_canon = {}
manifest_sin_match = []
if os.path.exists(MAN):
    ids = re.findall(r'^- id: ([a-z0-9_]+)', open(MAN, encoding='utf-8').read(), re.M)
    for mid in ids:
        pfs = prefijos_id(mid)
        hallado = None
        for canon, toks in tokens_por_canon.items():
            if pfs & toks:
                hallado = canon; break
        if hallado is None:
            for canon, toks in tokens_por_canon.items():
                if any(len(pf) > 3 and any(pf in t or t in pf for t in toks) for pf in pfs):
                    hallado = canon; break
        if hallado:
            id_a_canon[mid] = hallado
            en_disco.add(hallado)
        else:
            manifest_sin_match.append(mid)
    r_disco = f"{len(en_disco)} ({', '.join(sorted(en_disco))})"
else:
    ids = []
    r_disco = "manifiesto.yaml ausente — cruce NO derivado"
op_disco = [r for r in op if r['acronimo'] in en_disco]
print(f"\nCRUCE CONTRA data/manifiesto.yaml (vía tabla de alias)")
print(f"  entradas de manifiesto: {len(ids)}")
print(f"  ids emparejados a alguna fuente canónica: {len(id_a_canon)}")
print(f"  MANIFEST_SIN_MATCH (id sin fuente canónica que lo explique): {len(manifest_sin_match)}")
print(f"  fuentes del catálogo ya registradas: {r_disco}")
print(f"  OPERABLES ya en disco:      {len(op_disco)}")
print(f"  OPERABLES sin bajar:        {len(op) - len(op_disco)}")
for r in rows:
    r['en_disco'] = r['acronimo'] in en_disco

print(f"  MANIFEST_SIN_MATCH, primeros 20 de {len(manifest_sin_match)}: {manifest_sin_match[:20]}")

# catalogo_unico.json se mantiene como LISTA (no dict): tests/cruce_operables.py
# (fuera del perímetro de este acto) hace `for r in json.load(open(UNICO))`
# esperando ese formato exacto -- cambiarlo rompería ese script.
json.dump(rows, open(os.path.join(OUT,'catalogo_unico.json'),'w'), ensure_ascii=False, indent=1)
