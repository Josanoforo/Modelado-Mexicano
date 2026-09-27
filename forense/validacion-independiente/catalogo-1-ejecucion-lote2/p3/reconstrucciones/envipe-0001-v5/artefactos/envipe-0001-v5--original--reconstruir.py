"""Reconstrucción independiente; sólo entradas declaradas y bibliotecas genéricas."""
import argparse
import csv
import hashlib
import json
import platform
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')


def require(df, cols):
    for c in cols:
        if c not in df:
            raise ValueError('NO-ESTIMABLE-COLUMNA-AUSENTE:' + c)
        if df[c].eq('').all():
            raise ValueError('NO-ESTIMABLE-COLUMNA-VACIA:' + c)


def estimate(z, out):
    def read(table):
        name = f'{table}_envipe2025/conjunto_de_datos/conjunto_de_datos_{table}_envipe2025.csv'
        return pd.read_csv(z.open(name), dtype=str, keep_default_na=False).apply(lambda c: c.str.strip())
    m, p = read('tmod_vic'), read('tper_vic2')
    identity = ['UPM', 'VIV_SEL', 'HOGAR', 'R_SEL']
    design = ['EST_DIS', 'UPM_DIS']
    require(m, ['ID_DEL', 'ID_PER', 'BPCOD', 'BP1_20', 'BP1_23'] + identity + design)
    require(p, ['ID_PER', 'FAC_ELE'] + identity + design)
    if m.ID_DEL.eq('').any() or m.ID_DEL.duplicated().any() or p.ID_PER.duplicated().any():
        raise ValueError('IDENTIDAD-NO-UNIVOCA')
    personal = m.BPCOD.isin([f'{i:02d}' for i in range(5, 16)])
    unreported = m.BP1_20.eq('2')
    u = m[personal & unreported & m.BP1_23.isin([f'{i:02d}' for i in range(1, 9)])].copy()
    if u.empty:
        raise ValueError('NO-ESTIMABLE-UNIVERSO-VACIO')
    if u.ID_PER.eq('').any() or not set(u.ID_PER).issubset(set(p.ID_PER)):
        raise ValueError('IDENTIDAD-PERSONAL-AUSENTE-O-SIN-ENLACE')
    link = u.merge(p, on='ID_PER', suffixes=('_m', '_p'), validate='many_to_one')
    for c in identity + design:
        if link[c + '_m'].ne(link[c + '_p']).any():
            raise ValueError('IDENTIDAD-O-DISENO-DISCORDANTE:' + c)
    u['y'] = u.BP1_23.isin(['01', '02', '06', '08']).astype(int)
    y = u.groupby('ID_PER', sort=True).y.max()
    d = p.set_index('ID_PER').loc[y.index].copy()
    d['y'] = y
    if d[design].eq('').any().any():
        raise ValueError('NO-ESTIMABLE-DISENO-INCOMPLETO')
    d['w'] = pd.to_numeric(d.FAC_ELE, errors='raise')
    if not np.isfinite(d.w).all() or (d.w <= 0).any():
        raise ValueError('PONDERADOR-INVALIDO')
    d['wy'] = d.w * d.y
    clusters = d.groupby(design, sort=True)[['wy', 'w']].sum()
    blocks = [g.to_numpy(dtype=np.float64) for _, g in clusters.groupby(level=0, sort=True)]
    singletons = sum(len(g) == 1 for g in blocks)
    rng = np.random.Generator(np.random.PCG64(20260909))
    reps = np.empty(2000)
    # Orden fijo: réplica, estrato y UPM lexicográficos; UPM observadas en U4.
    for b in range(2000):
        total = np.zeros(2)
        for block in blocks:
            n = len(block)
            total += block[rng.integers(0, n, size=n)].sum(axis=0)
        if total[1] <= 0:
            raise ValueError('NO-ESTIMABLE-UNIVERSO-VACIO-EN-REPLICA')
        reps[b] = total[0] / total[1]
    lo, hi = np.percentile(reps, [2.5, 97.5], method='linear')
    result = {
        'estimacion': float(d.wy.sum() / d.w.sum()), 'ic95_inferior': float(lo),
        'ic95_superior': float(hi), 'numerador_ponderado': int(d.wy.sum()),
        'denominador_ponderado': int(d.w.sum()), 'n_personas': len(d),
        'METODO-IC': 'IC-CON-ESTRATOS-DE-UPM-UNICA' if singletons else 'BOOTSTRAP-UPM-ESTRATIFICADO',
    }
    audit = {
        'filas_tmod_vic': len(m), 'filas_tper_vic2': len(p), 'delitos_U1': len(u),
        'personas_U4': len(d), 'personas_C2_positivas': int(d.y.sum()),
        'BP1_23_blanco_no_denunciados_todos': int((unreported & m.BP1_23.eq('')).sum()),
        'BP1_23_blanco_no_denunciados_personales': int((personal & unreported & m.BP1_23.eq('')).sum()),
        'estratos_U4': len(blocks), 'UPM_por_estrato_total_U4': len(clusters),
        'estratos_UPM_unica': singletons, 'enlaces_faltantes': 0,
        'discrepancias_identidad_y_diseno': 0,
        'bootstrap': {'replicas': 2000, 'generador': 'numpy.PCG64', 'semilla': 20260909,
                      'marco': 'UPM observadas en U4, dentro de EST_DIS',
                      'orden': 'replica primero; estrato y UPM lexicograficos',
                      'muestreo': 'n_h extracciones uniformes con reemplazo por estrato',
                      'percentiles': 'numpy.percentile, method=linear'},
    }
    write_json(out / 'auditoria.json', audit)
    np.savetxt(out / 'replicas.tsv', np.column_stack([np.arange(1, 2001), reps]),
               delimiter='\t', header='replica\tproporcion', comments='', fmt=['%d', '%.17g'])
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--entrada', type=Path, default=Path('/entrada'))
    parser.add_argument('--raw', type=Path, default=Path('/raw'))
    parser.add_argument('--salida', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.salida.mkdir(parents=True, exist_ok=True)
    receipt = {'manifiesto_sha256': sha(args.entrada / 'manifiesto.json'),
               'entradas': {}, 'insumos': [], 'resultados_esperados_accedidos': False,
               'revelacion_solicitada': False,
               'versiones': {'python': platform.python_version(), 'numpy': np.__version__, 'pandas': pd.__version__}}
    manifest = json.loads((args.entrada / 'manifiesto.json').read_text())
    for name, expected in manifest['archivos'].items():
        actual = sha(args.entrada / name)
        receipt['entradas'][name] = actual
        if actual != expected:
            raise ValueError('HASH-ENTRADA-NO-COINCIDE:' + name)
    tolerance = json.loads((args.entrada / 'tolerancia.json').read_text())
    assert tolerance['tipo'] == 'flotante' and tolerance['abs'] >= 0
    receipt['tolerancia'] = tolerance
    targets = list(csv.DictReader((args.entrada / 'estimandos.tsv').open(), delimiter='\t'))
    result, status, reason = {}, 'RECONSTRUIDO', ''
    try:
        for item in json.loads((args.entrada / 'insumos.json').read_text()):
            path = args.raw / item['id'] / item['archivo']
            actual = sha(path)
            receipt['insumos'].append({**item, 'ruta': str(path), 'sha256_observado': actual,
                                       'bytes': path.stat().st_size, 'coincide': actual == item['sha256']})
            if actual != item['sha256']:
                raise ValueError('HASH-INSUMO-NO-COINCIDE:' + item['id'])
        with zipfile.ZipFile(args.raw / 'envipe2025_csv' / 'envipe2025_csv.zip') as z:
            entries = []
            for item in z.infolist():
                entries.append({'entrada': item.filename, 'bytes': item.file_size,
                                'sha256': hashlib.sha256(z.read(item)).hexdigest() if not item.is_dir() else None})
            write_json(args.salida / 'entradas_zip.json', entries)
            result = estimate(z, args.salida)
    except (OSError, zipfile.BadZipFile) as exc:
        status, reason = 'BLOQUEADO-POR-ACCESO', str(exc)
    except (ValueError, KeyError) as exc:
        status, reason = 'NO-RECALCULABLE-DESDE-SPEC', str(exc)
    rows = []
    for target in targets:
        if target['llave'] == 'RESULT-ENVIPE-DEN-P-C2-U4':
            rows.append({**target, 'estado': status, 'motivo': reason, **result})
        else:
            rows.append({**target, 'estado': 'NO-RECALCULABLE-DESDE-SPEC',
                         'motivo': 'LLAVE-SIN-IMPLEMENTACION-NI-ASIGNACION-DE-IDENTIDAD'})
    fields = list(targets[0]) + ['estado', 'motivo', 'estimacion', 'ic95_inferior', 'ic95_superior',
              'numerador_ponderado', 'denominador_ponderado', 'n_personas', 'METODO-IC']
    with (args.salida / 'reconstruccion.tsv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    receipt['estado'] = status
    write_json(args.salida / 'recibo.json', receipt)


if __name__ == '__main__':
    main()
