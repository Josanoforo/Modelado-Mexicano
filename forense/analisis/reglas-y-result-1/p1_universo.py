"""P1 de GEN2-REGLAS-Y-RESULT-1: universo de reglas SI-ENTONCES por objeto.
Patrón declarado: línea con r'\bSI\b.{0,300}ENTONCES' (misma línea física).
Fuentes: reglas-propuestas-v1_0.tsv (todas sus filas), corpus/reports (v1),
corpus/reports-v2 (líneas no ya citadas por la tabla), integrador.
Llave: sha1 del texto normalizado (minúsculas, sin markdown ni citas [..])."""
import csv, glob, hashlib, re, sys, unicodedata
PAT = re.compile(r'\bSI\b.{0,300}ENTONCES')
def norm(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
    t = re.sub(r'\[[^\]]*\]|[`*_>]|regla:|^[-\d. ]+', ' ', t)
    return re.sub(r'[^a-z0-9]+', ' ', t).strip()
def llave(t): return 'RG-' + hashlib.sha1(norm(t).encode()).hexdigest()[:10]
tier_re = re.compile(r'\[(FUERTE|MEDIA|MEDIO|HIP[A-ZÓ ]*|NARRATIVA[A-Z ]*|D[ÉE]BIL)[^\]]*\]', re.I)
filas, vistas = {}, set()
def add(texto, fuente, origen, tier='', seg='', drv='', rp=''):
    k = llave(texto)
    if k in filas:
        filas[k]['fuentes'] += ' | ' + fuente; return
    filas[k] = dict(regla_id=k, rp_id=rp, origen=origen, fuentes=fuente,
                    texto=re.sub(r'\s+', ' ', texto).strip()[:900],
                    tier_declarado=tier, segmento=seg, driver=drv)
for r in csv.DictReader(open('forense/analisis/reports-v2/reglas-propuestas-v1_0.tsv'), delimiter='\t'):
    add(r['regla'], r['fuente'], 'TABLA-C3-1', r['tier_declarado'], r['segmento'], r['driver'], r['id'])
    vistas.add(r['fuente'])
conteo = {}
for d, org in (('corpus/reports', 'REPORT-V1'), ('corpus/reports-v2', 'REPORT-V2'),
               ('canon', 'INTEGRADOR')):
    pat = 'canon/integrador-psicologia-mexicano.md' if d == 'canon' else d + '/*.md'
    n = 0
    for f in sorted(glob.glob(pat)):
        for i, l in enumerate(open(f, encoding='utf-8'), 1):
            if not PAT.search(l): continue
            n += 1
            if f'{f}:{i}' in vistas: continue
            if org == 'INTEGRADOR' and 'SI-ENTONCES' in l and not re.search(r'\bSI\b [a-z]', l): continue
            m = tier_re.search(l)
            add(l, f'{f}:{i}', org, m.group(1).upper() if m else '')
    conteo[org] = n
w = csv.DictWriter(open(sys.argv[1], 'w', newline=''), fieldnames=list(next(iter(filas.values()))), delimiter='\t')
w.writeheader(); w.writerows(filas.values())
print('lineas_patron', conteo, 'filas_universo', len(filas))
