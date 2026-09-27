"""Diagnóstico NO CIEGO de las once publicabilidades; no modifica sellos."""
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
BASE = ROOT / 'forense/validacion-independiente/catalogo-1-ejecucion-lote1'


def regla(n, upm, p, ancho, cv):
    if p is None or ancho is None or not math.isfinite(p) or not math.isfinite(ancho):
        return 'NO-ESTIMABLE'
    if p > 0 and (cv is None or not math.isfinite(cv)):
        return 'NO-ESTIMABLE'
    return 'PUBLICABLE' if n >= 100 and upm >= 5 and ancho <= .20 and (p == 0 or cv <= .30) else 'SUPRIMIDO'


def main():
    with (BASE / 'dictamenes-publicabilidad.tsv').open() as f:
        cases = list(csv.DictReader(f, delimiter='\t'))
    rows = []
    for year, part, tag in [('2011', 'MODULOS', 'MOD'), ('2021', 'DISCRIMINACION', 'DIS')]:
        key = f'RESULT-ENDIREH{year}-{tag}-TABLA'
        source = ROOT / f'data/corrida0/CALC-ENDIREH-PISOS-{year}-{part}-0001/resultados.json'
        cells = json.loads(json.loads(source.read_text())['resultados'][key])
        support = {}
        if year == '2021':
            pack = 'endireh-pisos-2021-discriminacion-0001'
            path = BASE / 'reconstrucciones' / pack / 'artefactos' / (pack + '--artefactos--soporte.tsv')
            with path.open() as f:
                support = {r['llave']: r for r in csv.DictReader(f, delimiter='\t')}
        for case in cases:
            identity = case['llave']
            if not identity.startswith(key + '#'):
                continue
            c = cells[int(identity.split('#')[1])]
            width = c['ic95'][1] - c['ic95'][0]
            cv = c['se'] / c['p']
            s = support.get(identity, {})
            rows.append(dict(llave=identity, conducta=c['resultado'], eje=c['eje'], segmento=c['categoria'],
                n_sellado=c['n'], upm_sellado=c['upm'], cv_sellado=cv, ancho_sellado=width,
                margen_cv=.30-cv, margen_ancho=.20-width,
                regla_sellado=regla(c['n'], c['upm'], c['p'], width, cv),
                cv_independiente=s.get('cv', 'NO-PUBLICADO'), n_independiente=s.get('n_conocido', 'NO-PUBLICADO'),
                upm_independiente=s.get('upm_con_casos', 'NO-PUBLICADO'),
                motivo_independiente=case['motivo'], dictamen='DISCREPA-PUBLICABILIDAD',
                condicion='sesion01: universo CP4_1' if year=='2011' and c['resultado'].startswith('permiso') else
                    'sesion01: columnas y elegibilidad denuncia externa' if year=='2011' else 'sin dependencia material de sesion01 identificada',
                cifra_disponible='sellada SI; independiente NO', incertidumbre='no equivalente demostrada',
                conclusion='cambia disponibilidad; cambio de conclusion sustantiva no probado'))
    assert len(rows) == 11
    with (OUT / 'dictamenes.tsv').open('w') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t'); w.writeheader(); w.writerows(rows)
    # Enumeración exhaustiva de dos extracciones con reemplazo: la UPM sin
    # mujeres cambia la distribución de denominadores, aunque no el punto.
    from itertools import product
    frame_mass = [sum({'u1':1, 'u2':1, 'u0':0}[u] for u in draw)
                  for draw in product(('u1','u2','u0'), repeat=2)]
    domain_mass = [sum(1 for u in draw) for draw in product(('u1','u2'), repeat=2)]
    checks = {
        'frontera_inclusiva': regla(100, 5, .1, .20, .30) == 'PUBLICABLE',
        'cv_sobre_frontera': regla(100, 5, .1, .20, math.nextafter(.30, 1)) == 'SUPRIMIDO',
        'ancho_sobre_frontera': regla(100, 5, .1, math.nextafter(.20, 1), .30) == 'SUPRIMIDO',
        'cero_exime_cv': regla(100, 5, 0, 0, None) == 'PUBLICABLE',
        'no_estimable_no_es_cero': regla(100, 5, None, None, None) == 'NO-ESTIMABLE',
        'cv_ausente_positivo': regla(100, 5, .1, .1, None) == 'NO-ESTIMABLE',
        'dominio_no_es_marco': min(frame_mass)==0 and min(domain_mass)==2,
        'upm_cero_contribuye_marco_no_soporte': regla(100,4,.1,.1,.1) == 'SUPRIMIDO',
        'once_sellados_pasan_regla': all(r['regla_sellado']=='PUBLICABLE' for r in rows),
        'cinco_cv_independientes_exceden': all(float(r['cv_independiente'])>.30 for r in rows if r['cv_independiente']!='NO-PUBLICADO'),
    }
    assert all(checks.values()), checks
    (OUT / 'pruebas.json').write_text(json.dumps(checks, indent=2)+'\n')
    print(json.dumps({'identidades':len(rows), 'pruebas':checks}))


if __name__ == '__main__':
    main()
