#!/usr/bin/env python3
"""Catálogo unificado de fuentes, derivado de los 11 inventarios del repo.
Tres formatos coexisten: '## N.'+tabla, '### N.'+tabla, '### N.'+viñetas.
La identidad de cada fuente se resuelve contra data/inventarios/alias-fuentes.yaml
(tabla de alias canónicos); un título que no resuelve va a SIN_RESOLVER en vez de
inventarse una identidad con el fallback de acron().
Toda cifra impresa se deriva aquí."""
import re, glob, os, json, collections, yaml
import os, sys
RAIZ = os.environ.get('MM_RAIZ') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INV  = os.path.join(RAIZ, 'data', 'inventarios')
OUT  = os.path.join(RAIZ, 'data')
ALIAS = os.path.join(INV, 'alias-fuentes.yaml')
if not os.path.isdir(INV):
    sys.exit(f"NO ENCONTRÉ {INV} — este script se corre desde un clon del repo con los "
             f"inventarios en data/inventarios/, o con MM_RAIZ apuntando a la raíz.")
if not os.path.isfile(ALIAS):
    sys.exit(f"NO ENCONTRÉ {ALIAS} — falta la tabla de identidad canónica de fuentes.")


FILES = sorted(glob.glob(os.path.join(INV, 'inventario*mexico.md')))
def dominio(p):
    b = re.sub(r'^inventario[-_]?(fuentes)?[-_]?', '', os.path.basename(p))
    return re.sub(r'[-_]?mexico\.md$', '', b)

def acron(t):
    """Heurística original de identidad. Ya NO se usa como identidad final —
    solo como sugerencia dentro de SIN_RESOLVER y como clave de búsqueda en
    la tabla de alias. Ver forense/notas/2026-08-06-map1-lector.md para el
    porqué (fragmentos truncados a 30 caracteres, colisiones entre fuentes
    distintas, la misma fuente bajo hasta tres identidades)."""
    t = re.sub(r'\*\*.*?\*\*', '', t)
    m = re.findall(r'\(([A-ZÁÉÍÓÚÑ][A-Za-z0-9ÁÉÍÓÚÑáéíóúñ/\-\. ]{1,25})\)', t)
    if m:
        c = m[0].strip().upper().replace('.', '')
        if re.match(r'^[A-Z0-9/\- ]+$', c): return c
    m2 = re.match(r'^([A-ZÁÉÍÓÚÑ]{2,}[A-Za-z0-9]*)', t.strip())
    if m2: return m2.group(1).upper()
    return re.split(r'[—\-–(]', t)[0].strip().upper()[:30]

def normaliza(s):
    """strip() + colapsar espacios internos + mayúsculas. El espacio final
    de un alias nunca debe volver a crear una fuente distinta."""
    return re.sub(r'\s+', ' ', s.strip()).upper()

def carga_tabla_alias():
    entradas = yaml.safe_load(open(ALIAS, encoding='utf-8')) or []
    tabla = {}
    for e in entradas:
        for a in e.get('alias', []):
            tabla[normaliza(a)] = e['canonico']
    return tabla, entradas

TABLA_ALIAS, ALIAS_ENTRADAS = carga_tabla_alias()

def resuelve(titulo):
    """Devuelve (canonico, sugerencia). canonico es None si el título no
    resuelve contra la tabla de alias -- en ese caso NUNCA se usa 'sugerencia'
    como identidad, solo se ofrece como pista dentro de SIN_RESOLVER."""
    sugerencia = acron(titulo)
    return TABLA_ALIAS.get(normaliza(sugerencia)), sugerencia

CAMPOS = {
 'institucion': r'Instituci[óo]n(?: responsable)?',
 'microdatos':  r'Microdatos',
 'acceso':      r'(?:Acceso|Registro para acceder|Registro/solicitud|Registro)',
 'periodo':     r'Periodicidad(?: y ediciones)?',
}
def extrae(bloque, pat):
    m = re.search(r'\|\s*'+pat+r'\s*\|\s*(.+?)\s*\|\s*$', bloque, re.M|re.I)
    if m: return m.group(1).strip()
    m = re.search(r'^[-*]\s*\*\*'+pat+r':?\*\*:?\s*(.+?)$', bloque, re.M|re.I)
    return m.group(1).strip() if m else ''

fuentes, sosp, sin_resolver = [], {}, []
for f in FILES:
    txt = open(f, encoding='utf-8').read(); dom = dominio(f); base = os.path.basename(f)
    part = re.split(r'^#{1,2} (?=Fuentes que se sospecha|Fuentes sospechadas)', txt, flags=re.M)
    conf = part[0]; sosp[dom] = len(re.findall(r'^#{2,4} ', part[1], re.M)) if len(part) > 1 else 0
    heads = list(re.finditer(r'^#{2,3} (\d+)\.\s*(.+)$', conf, flags=re.M))
    for i, m in enumerate(heads):
        fin = heads[i+1].start() if i+1 < len(heads) else len(conf)
        b = conf[m.end():fin]
        titulo = m.group(2).strip()
        linea = txt.count('\n', 0, m.start()) + 1
        canon, sugerencia = resuelve(titulo)
        fuentes.append({'dominio': dom, 'n': int(m.group(1)), 'titulo': titulo,
                        'acronimo': canon,
                        **{k: extrae(b, v) for k, v in CAMPOS.items()}})
        if canon is None:
            sin_resolver.append({'dominio': dom, 'archivo': base, 'linea': linea,
                                  'titulo': titulo, 'sugerencia': sugerencia})

# --- SIN_RESOLVER se imprime antes que cualquier otra cifra: un lector que
# adivina en silencio es como se llegó a las identidades falsas de antes;
# uno que se queja a gritos es el arreglo. ---
print(f"SIN_RESOLVER: {len(sin_resolver)}")
for s in sin_resolver:
    print(f"  {s['archivo']}:{s['linea']}  sugerencia(no-usada-como-identidad)={s['sugerencia']!r}  titulo={s['titulo']!r}")
print()

# --- VERIFICACIÓN DE LA RECETA contra casos de respuesta conocida ---
print("VERIFICACIÓN DE RECETA (parser vs. conteo crudo de encabezados numerados)")
ok = True
for f in FILES:
    d = dominio(f); txt = open(f, encoding='utf-8').read()
    crudo = len(re.findall(r'^#{2,3} \d+\.', txt.split('# Fuentes que se sospecha')[0], re.M))
    got = sum(1 for x in fuentes if x['dominio'] == d)
    flag = 'ok' if crudo == got else 'DESCUADRE'
    if crudo != got: ok = False
    print(f"  {flag:9s} {d:32s} crudo={crudo:3d}  parseado={got:3d}")
print("RECETA:", "consistente" if ok else "INCONSISTENTE — no usar las cifras de abajo")

print(f"\nARCHIVOS: {len(FILES)}   ENTRADAS (con repetición): {len(fuentes)}"
      f"   RESUELTAS: {len(fuentes)-len(sin_resolver)}   SIN_RESOLVER: {len(sin_resolver)}")
uni = collections.defaultdict(list)
for r in fuentes:
    if r['acronimo'] is not None:
        uni[r['acronimo']].append(r)
print(f"FUENTES ÚNICAS (dedup por identidad canónica, tabla de alias): {len(uni)}")
print(f"SOSPECHADAS NO CONFIRMADAS: {sum(sosp.values())}  {dict((k,v) for k,v in sosp.items() if v)}")

print("\nPOR DOMINIO:")
for d, n in sorted(collections.Counter(x['dominio'] for x in fuentes).items(), key=lambda x:-x[1]):
    print(f"  {n:3d}  {d}")

comp = sorted(((len(set(x['dominio'] for x in v)), k) for k, v in uni.items()), reverse=True)
print("\nTRANSVERSALES (en 3+ dominios) — candidatas a espina dorsal:")
for n, k in comp:
    if n >= 3: print(f"  {n} dominios · {k}")
print(f"MONO-DOMINIO: {sum(1 for n,_ in comp if n==1)}")

def has(v, pat): return bool(re.search(pat, v or '', re.I))
micro = {k for k,v in uni.items() if any(has(x['microdatos'], r'^\s*\**s[íi]') for x in v)}
nomicro = {k for k,v in uni.items() if all(has(x['microdatos'], r'^\s*\**no') for x in v) and any(x['microdatos'] for x in v)}
libre = {k for k,v in uni.items() if any(has(x['acceso'], r'directa|sin registro|abierto|no\b|p[úu]blic') for x in v)}
print(f"\nMICRODATOS: sí={len(micro)}  no={len(nomicro)}  indeterminado={len(uni)-len(micro)-len(nomicro)}")
print(f"ACCESO LIBRE / SIN REGISTRO: {len(libre)}")
print(f"MICRODATOS **Y** ACCESO LIBRE (el conjunto operable): {len(micro & libre)}")
print("  " + ', '.join(sorted(micro & libre)))
json.dump({'fuentes':fuentes,'sospechadas':sosp,'sin_resolver':sin_resolver},
          open(os.path.join(OUT,'catalogo_derivado.json'),'w'), ensure_ascii=False, indent=1)
