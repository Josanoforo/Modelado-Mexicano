"""P4 de GEN2-REGLAS-Y-RESULT-1: ensambla por-dominio/*.tsv con el universo P1 en
canon/reglas-contrastadas-v1_0.tsv y verifica los criterios de «hecho»:
ids sin fila 0 · dictamen vacío 0 · CONFIRMA/ROMPE con resultado_id en
data/corrida0/<calc>/resultados.json y sello.json (0 ausentes)."""
import csv, glob, os, sys, collections
B = 'forense/analisis/reglas-y-result-1/'
U = {r['regla_id']: r for r in csv.DictReader(open(B + 'universo-reglas-v1_0.tsv'), delimiter='\t')}
D = {}
for f in sorted(glob.glob(B + 'por-dominio/*.tsv')):
    for r in csv.DictReader(open(f), delimiter='\t'):
        D[r['regla_id']] = r
faltan = [k for k in U if k not in D]; extra = [k for k in D if k not in U]
vacios = [k for k, r in D.items() if not r['dictamen'].strip()]
aus = []
for k, r in D.items():
    if r['dictamen'] in ('CONFIRMA', 'ROMPE'):
        c, rid = r['calc'], r['resultado_id']
        p = f'data/corrida0/{c}/resultados.json'
        if not (rid and os.path.exists(p) and rid in open(p).read()
                and os.path.exists(f'data/corrida0/{c}/sello.json')):
            aus.append(k)
cols = list(U[next(iter(U))]) + [c for c in next(iter(D.values())) if c != 'regla_id'] + ['temporalidad']
with open('canon/reglas-contrastadas-v1_0.tsv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=cols, delimiter='\t', extrasaction='ignore')
    w.writeheader()
    for k in U:
        w.writerow({**U[k], **D.get(k, {}), 'temporalidad': 'RETROSPECTIVA'})
print('universo', len(U), 'ids_sin_fila', len(faltan), 'filas_extra', len(extra),
      'dictamen_vacio', len(vacios), 'confirma_rompe_sin_result', len(aus))
print('por_dictamen', dict(collections.Counter(r['dictamen'] for r in D.values())))
sys.exit(1 if faltan or vacios or aus else 0)
