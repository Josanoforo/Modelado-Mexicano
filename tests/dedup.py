import json, re, unicodedata, collections
import os, sys
RAIZ = os.environ.get('MM_RAIZ') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INV  = os.path.join(RAIZ, 'data', 'inventarios')
OUT  = os.path.join(RAIZ, 'data')
if not os.path.isdir(INV):
    sys.exit(f"NO ENCONTRÉ {INV} — este script se corre desde un clon del repo con los "
             f"inventarios en data/inventarios/, o con MM_RAIZ apuntando a la raíz.")

d = json.load(open(os.path.join(OUT,'catalogo_derivado.json')))
F = d['fuentes']
def norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode()
    s = re.sub(r'\*\*.*?\*\*','',s)
    s = re.sub(r'\(.*?\)','',s)
    s = re.split(r'[—–]|\s-\s', s)[0]
    s = re.sub(r'[^a-z0-9 ]',' ', s.lower())
    s = re.sub(r'\b(encuesta|nacional|de|del|la|el|los|las|y|en|sobre|para|mexico|censo)\b',' ',s)
    return re.sub(r'\s+',' ',s).strip()
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
MAN = os.path.join(OUT, 'manifiesto.yaml')
en_disco = set()
if os.path.exists(MAN):
    ids = re.findall(r'^- id: ([a-z0-9_]+)', open(MAN, encoding='utf-8').read(), re.M)
    pref = {m.group(0).upper() for i in ids if (m := re.match(r'^[a-z]+', i))}
    for r in rows:
        a = r['acronimo'].upper()
        if a in pref or any(p in a for p in pref if len(p) > 3):
            en_disco.add(r['acronimo'])
    r_disco = f"{len(en_disco)} ({', '.join(sorted(en_disco))})"
else:
    r_disco = "manifiesto.yaml ausente — cruce NO derivado"
op_disco = [r for r in op if r['acronimo'] in en_disco]
print(f"\nCRUCE CONTRA data/manifiesto.yaml")
print(f"  fuentes del catálogo ya registradas: {r_disco}")
print(f"  OPERABLES ya en disco:      {len(op_disco)}")
print(f"  OPERABLES sin bajar:        {len(op) - len(op_disco)}")
for r in rows:
    r['en_disco'] = r['acronimo'] in en_disco

json.dump(rows, open(os.path.join(OUT,'catalogo_unico.json'),'w'), ensure_ascii=False, indent=1)
