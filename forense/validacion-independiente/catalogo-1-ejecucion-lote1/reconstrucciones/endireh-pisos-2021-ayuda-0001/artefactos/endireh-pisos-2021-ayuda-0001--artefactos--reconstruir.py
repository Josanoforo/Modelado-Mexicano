#!/usr/bin/env python3
"""Reimplementación independiente. Solo lee entrada y raw; no resultados externos."""
import csv
import hashlib
import json
import os
from pathlib import Path
import platform
import zipfile

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = Path(os.environ.get('ENDIREH_RAW', '/raw'))
SEED, B = 20260923, 500


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def dump(name, obj):
    (ROOT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def write_tsv(name, rows, columns):
    with open(ROOT / name, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=columns, delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def main():
    # Validación íntegra del paquete antes del primer cálculo.
    manifest = json.loads((ROOT / 'entrada/manifiesto.json').read_text())
    for name, expected in manifest['archivos'].items():
        assert sha(ROOT / 'entrada' / name) == expected, name
    inputs = json.loads((ROOT / 'entrada/insumos.json').read_text())
    inventory = []
    for item in inputs:
        extension = '.zip' if item['id'].endswith('_zip') else '.pdf'
        path = RAW / (item['id'] + extension)
        actual = sha(path)
        assert actual == item['sha256'], path
        inventory.append({**item, 'ruta_recibida': str(path),
                          'sha256_observado': actual, 'verificacion': 'VERIFICADO'})
    dump('inventario_insumos.json', inventory)
    z = zipfile.ZipFile(RAW / 'endireh2021_bd_csv_zip.zip')
    entries = []
    for info in z.infolist():
        h = hashlib.sha256()
        with z.open(info) as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b''):
                h.update(chunk)
        entries.append({'entrada': info.filename, 'bytes': info.file_size,
                        'sha256_descomprimido': h.hexdigest()})
    dump('entradas_zip.json', entries)

    def read(name, columns):
        return pd.read_csv(z.open('bd_endireh_2021_csv/' + name + '.csv'),
                           usecols=columns, dtype=str, encoding='latin1',
                           keep_default_na=False).apply(lambda c: c.str.strip())

    acts = ['P14_1_' + str(i) + ('AB' if i in [23, 24, 35, 36, 37, 38] else '')
            for i in range(1, 39)]
    institutions = ['P14_8_' + str(i) for i in range(1, 11)]
    reasons = ['P14_22_' + str(i) for i in range(1, 16)]
    design = ['ID_PER', 'T_INSTRUM', 'DOMINIO', 'CVE_ENT',
              'FAC_MUJ', 'EST_DIS', 'UPM_DIS']
    d = read('TB_SEC_XIV', design + acts + ['P14_7_1', 'P14_7_2'] + institutions)
    d = d[d.T_INSTRUM.isin(['A1', 'A2'])].copy()
    assert d.ID_PER.is_unique
    # El marco de UPM se fija ANTES de excluir edad, actos o respuestas desconocidas.
    assert d[['EST_DIS', 'UPM_DIS']].ne('').all().all()
    psus = d[['EST_DIS', 'UPM_DIS']].drop_duplicates().sort_values(
        ['EST_DIS', 'UPM_DIS']).reset_index(drop=True)
    psus['psu_index'] = np.arange(len(psus))
    d = d.merge(psus, on=['EST_DIS', 'UPM_DIS'], validate='many_to_one')
    for name, columns in [('TB_SEC_XIV_2', reasons), ('TSDem', ['EDAD', 'NIV', 'SEXO'])]:
        right = read(name, ['ID_PER'] + columns)
        assert right.ID_PER.is_unique, name
        d = d.merge(right, on='ID_PER', how='left', validate='one_to_one', indicator=True)
        assert d['_merge'].eq('both').all(), name
        d = d.drop(columns='_merge')
    assert d.SEXO.eq('2').all()
    age = pd.to_numeric(d.EDAD, errors='coerce')
    valid_age = age.between(15, 120)
    w = pd.to_numeric(d.FAC_MUJ, errors='raise').to_numpy(float)
    assert np.isfinite(w).all() and (w > 0).all()
    positive = d[acts].isin(['1', '2', '3']).any(axis=1)
    negative = d[acts].eq('4').all(axis=1)
    eligible = valid_age & positive
    index = d.psu_index.to_numpy()
    requests = list(csv.DictReader(open(ROOT / 'entrada/estimandos.tsv'), delimiter='\t'))
    assert len({r['llave'] for r in requests}) == len(requests)
    numerators, denominators, metadata = [], [], []
    mappings = []
    for r in requests:
        c, axis, segment = r['conducta'], r['eje'], r['segmento']
        issue = ''
        if c == 'ayuda':
            variable, universe, known_codes = 'P14_7_1', eligible, ['1', '2']
        elif c == 'denuncia':
            variable, universe, known_codes = 'P14_7_2', eligible, ['1', '2']
        elif c.startswith('institucion_'):
            variable = 'P14_8_' + str(int(c.split('_')[1]))
            universe, known_codes = eligible & d.P14_7_1.eq('1'), ['1', '2']
        elif c.startswith('razon_'):
            variable = 'P14_22_' + str(int(c.split('_')[1]))
            universe = eligible & d.P14_7_1.eq('2') & d.P14_7_2.eq('2')
            known_codes = ['0', '1']
            if c == 'razon_14':
                issue = ('Identidad contradictoria: metodo.md dice desconocía servicios; '
                         'P14_22_14 en FD p. 632 y cuestionario A 14.22 dice '
                         'no sabía que existían leyes para sancionar la violencia. '
                         'No se asigna equivalencia semántica.')
        else:
            raise ValueError(c)
        if axis == 'nacional':
            assert segment == 'MX'
            domain = np.ones(len(d), dtype=bool)
        elif axis == 'edad':
            lo, hi = {'15-29': (15, 29), '30-44': (30, 44),
                      '45-59': (45, 59), '60+': (60, 120)}[segment]
            domain = age.between(lo, hi)
        elif axis == 'escolaridad':
            levels = {'ninguno': ['00'], 'basica': ['01', '02', '03', '05', '06'],
                      'media_superior': ['04', '07', '08'], 'superior': ['09', '10', '11']}
            domain = d.NIV.isin(levels[segment])
        elif axis in ['localidad', 'pareja', 'entidad']:
            column = {'localidad': 'DOMINIO', 'pareja': 'T_INSTRUM', 'entidad': 'CVE_ENT'}[axis]
            domain = d[column].eq(segment)
        else:
            raise ValueError(axis)
        assert c in ['ayuda', 'denuncia'] or axis == 'nacional'
        mappings.append({'llave': r['llave'], 'variable': variable, 'eje': axis,
                         'segmento': segment, 'observacion': issue})
        if issue:
            metadata.append((r, issue, None, None))
            continue
        known = np.asarray(universe & domain & d[variable].isin(known_codes))
        yes = known & d[variable].eq('1').to_numpy()
        den = np.bincount(index, weights=w * known, minlength=len(psus))
        num = np.bincount(index, weights=w * yes, minlength=len(psus))
        metadata.append((r, '', int(known.sum()), int(np.count_nonzero(den))))
        denominators.append(den)
        numerators.append(num)
    den = np.column_stack(denominators)
    num = np.column_stack(numerators)
    rng = np.random.Generator(np.random.PCG64(SEED))
    boot_den = np.zeros((B, den.shape[1]))
    boot_num = np.zeros_like(boot_den)
    singleton = 0
    for _, group in psus.groupby('EST_DIS', sort=True):
        indices = group.psu_index.to_numpy()
        size = len(indices)
        if size == 1:
            counts = np.ones((B, 1), dtype=np.int64)
            singleton += 1
        else:
            draws = rng.integers(0, size, size=(B, size))
            counts = np.zeros((B, size), dtype=np.int64)
            np.add.at(counts, (np.arange(B)[:, None], draws), 1)
        assert (counts.sum(axis=1) == size).all()
        boot_den += counts @ den[indices]
        boot_num += counts @ num[indices]
    with np.errstate(invalid='ignore', divide='ignore'):
        point = num.sum(axis=0) / den.sum(axis=0)
        boot = boot_num / boot_den
    results, quality, replicas = [], [], []
    j = 0
    for r, issue, n, npsu in metadata:
        out = dict(llave=r['llave'], punto='', ic95_inf='', ic95_sup='',
                   estado='NO-RECALCULABLE-DESDE-SPEC', motivo=issue)
        if not issue:
            values = boot[:, j]
            failures = []
            if n < 100:
                failures.append('menos de 100 respuestas conocidas')
            if npsu < 5:
                failures.append('menos de 5 UPM con respuestas conocidas')
            if not np.isfinite(values).all() or not np.isfinite(point[j]):
                failures.append('denominador cero en estimación o réplica; spec no define tratamiento')
            else:
                lower, upper = np.quantile(values, [.025, .975], method='linear')
                cv = np.std(values, ddof=1) / point[j] if point[j] > 0 else 0.0
                if upper - lower > .20:
                    failures.append('ancho IC95 mayor que 0.20')
                if point[j] > 0 and cv > .30:
                    failures.append('CV mayor que 0.30')
            if failures:
                out['motivo'] = 'Supresión exigida por spec: ' + '; '.join(failures)
            else:
                out.update(punto=format(point[j], '.17g'), ic95_inf=format(lower, '.17g'),
                           ic95_sup=format(upper, '.17g'), estado='RECONSTRUIDO', motivo='')
                assert 0 <= lower <= upper <= 1 and 0 <= point[j] <= 1
                replicas.extend({'llave': r['llave'], 'replica': b + 1,
                                 'proporcion': format(v, '.17g')} for b, v in enumerate(values))
            quality.append({'llave': r['llave'], 'n_conocidas': n, 'upm_con_casos': npsu,
                            'publicable': not failures, 'motivo': out['motivo']})
            j += 1
        results.append(out)
    write_tsv('reconstruccion.tsv', results,
              ['llave', 'punto', 'ic95_inf', 'ic95_sup', 'estado', 'motivo'])
    write_tsv('replicas.tsv', replicas, ['llave', 'replica', 'proporcion'])
    write_tsv('identidades.tsv', mappings, ['llave', 'variable', 'eje', 'segmento', 'observacion'])
    dump('control_calidad.json', quality)
    dump('ejecucion.json', {
        'python': platform.python_version(), 'numpy': np.__version__, 'pandas': pd.__version__,
        'semilla': SEED, 'replicas': B, 'rng': 'numpy.random.Generator(PCG64)',
        'orden': 'estratos y UPM ordenados lexicográficamente; sort=True; matriz B por n_h',
        'percentiles': 'numpy.quantile method=linear', 'cv': 'sd de réplicas ddof=1 / punto',
        'filas_A1_A2': len(d), 'edad_invalida': int((~valid_age).sum()),
        'union_positiva': int(positive.sum()), 'union_negativa': int(negative.sum()),
        'union_desconocida': int((~positive & ~negative).sum()),
        'upm': len(psus), 'estratos': psus.EST_DIS.nunique(), 'singleton': singleton,
        'llaves': len(results), 'estados': pd.Series([r['estado'] for r in results]).value_counts().to_dict(),
        'primera_ejecucion_numerica': True,
        'sin_resultados_esperados': True,
    })
    print((ROOT / 'ejecucion.json').read_text())


if __name__ == '__main__':
    main()
