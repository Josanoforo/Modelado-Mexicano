#!/usr/bin/env python3
"""Reconstrucción independiente; entradas locales, sin resultados de referencia."""
import csv
import hashlib
import json
from pathlib import Path
import platform
import zipfile

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
ENT = ROOT / 'entrada'
RAW = Path('/raw')
SEED = 20260923
B = 200


def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def write_json(name, obj):
    (ROOT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def union(values):
    positive = np.isin(values, ['1', '2', '3']).any(axis=1)
    known = positive | (values == '4').all(axis=1)
    return positive, known


def main():
    # No sobrescribir el primer resultado.
    if (ROOT / 'reconstruccion.tsv').exists():
        raise SystemExit('Ya existe el primer resultado; no se sobrescribe.')
    manifest = json.loads((ENT / 'manifiesto.json').read_text())
    for name, digest in manifest['archivos'].items():
        assert sha(ENT / name) == digest, name
    raw_receipt = []
    for entry in json.loads((ENT / 'insumos.json').read_text()):
        suffix = '.zip' if entry['id'].endswith('_zip') else '.pdf'
        path = RAW / (entry['id'] + suffix)
        digest = sha(path)
        assert digest == entry['sha256'], path
        raw_receipt.append({**entry, 'ruta_recibida': str(path),
                            'sha256_recalculado': digest, 'bytes': path.stat().st_size})
    z = zipfile.ZipFile(RAW / 'endireh2021_bd_csv_zip.zip')
    members = []
    for info in z.infolist():
        members.append({'nombre': info.filename, 'bytes': info.file_size, 'crc32': f'{info.CRC:08x}'})
    def read(name, cols):
        member = 'bd_endireh_2021_csv/' + name
        with z.open(member) as f:
            digest = hashlib.file_digest(f, 'sha256').hexdigest()
        for item in members:
            if item['nombre'] == member:
                item['sha256'] = digest
        return pd.read_csv(z.open(member), encoding='latin1', dtype=str,
                           keep_default_na=False, usecols=cols)
    items = [f'P11_1_{i}' for i in range(1, 21)]
    xi = read('TB_SEC_XI.csv', ['ID_PER', 'T_INSTRUM', 'DOMINIO', 'CVE_ENT',
                              'FAC_MUJ', 'EST_DIS', 'UPM_DIS'] + items)
    dem = read('TSDem.csv', ['ID_PER', 'EDAD', 'NIV', 'SEXO'])
    assert xi.ID_PER.is_unique and dem.ID_PER.is_unique
    d = xi.merge(dem, on='ID_PER', how='left', validate='one_to_one', indicator=True)
    assert d['_merge'].eq('both').all()
    age = pd.to_numeric(d.EDAD, errors='coerce')
    weight = pd.to_numeric(d.FAC_MUJ, errors='coerce').to_numpy()
    eligible = (age.between(15, 120) & d.T_INSTRUM.isin(['A1', 'A2', 'B1', 'B2', 'C1', 'C2']) & (weight > 0)).to_numpy()
    assert d.loc[eligible, 'SEXO'].eq('2').all()
    positive, known = union(d[items].to_numpy())
    include = eligible & known
    # Marco completo de UPM del módulo XI, antes de seleccionar dominios.
    assert d.EST_DIS.ne('').all() and d.UPM_DIS.ne('').all()
    psu = d[['EST_DIS', 'UPM_DIS']].drop_duplicates().sort_values(['EST_DIS', 'UPM_DIS']).reset_index(drop=True)
    psu['idx'] = np.arange(len(psu))
    row_idx = d[['EST_DIS', 'UPM_DIS']].merge(psu, how='left', sort=False, validate='many_to_one')['idx'].to_numpy()
    strata = [g.idx.to_numpy() for _, g in psu.groupby('EST_DIS', sort=True)]
    keys = pd.read_csv(ENT / 'estimandos.tsv', sep='\t', dtype=str, keep_default_na=False)
    assert keys.llave.is_unique
    schooling = d.NIV.map({'00': 'ninguno', **{x: 'basica' for x in ['01','02','03','05','06']},
                           **{x: 'media_superior' for x in ['04','07','08']},
                           **{x: 'superior' for x in ['09','10','11']}})
    age_group = pd.cut(age, bins=[14,29,44,59,120], labels=['15-29','30-44','45-59','60+'])
    axes = {'nacional': pd.Series('MX', index=d.index), 'edad': age_group,
            'escolaridad': schooling, 'localidad': d.DOMINIO,
            'pareja': d.T_INSTRUM, 'entidad': d.CVE_ENT}
    numerator = np.zeros((len(psu), len(keys)))
    denominator = np.zeros_like(numerator)
    counts, clusters, reasons = [], [], []
    for j, row in keys.iterrows():
        if row.eje not in axes or row.segmento not in set(axes[row.eje].dropna()):
            reasons.append('Identidad del segmento no determinada por la especificación y los campos documentados.')
            counts.append(0); clusters.append(0)
            continue
        reasons.append('')
        mask = include & axes[row.eje].eq(row.segmento).to_numpy()
        counts.append(int(mask.sum()))
        clusters.append(int(np.unique(row_idx[mask]).size))
        denominator[:, j] = np.bincount(row_idx[mask], weights=weight[mask], minlength=len(psu))
        numerator[:, j] = np.bincount(row_idx[mask], weights=weight[mask]*positive[mask], minlength=len(psu))
    rng = np.random.Generator(np.random.PCG64(SEED))
    reps = np.full((B, len(keys)), np.nan)
    for b in range(B):
        draws = np.concatenate([rng.choice(s, size=len(s), replace=True) for s in strata])
        den = denominator[draws].sum(axis=0)
        np.divide(numerator[draws].sum(axis=0), den, out=reps[b], where=den > 0)
    den = denominator.sum(axis=0)
    point = np.divide(numerator.sum(axis=0), den, out=np.full(len(keys), np.nan), where=den > 0)
    intervals = np.quantile(reps, [.025, .975], axis=0, method='linear')
    se = np.std(reps, axis=0, ddof=1)
    output, diagnostics = [], []
    for j, row in keys.iterrows():
        p, lo, hi = point[j], intervals[0,j], intervals[1,j]
        cv = se[j]/p if p > 0 else 0.0
        failure = []
        if counts[j] < 100: failure.append('n conocido<100')
        if clusters[j] < 5: failure.append('UPM con respuesta conocida<5')
        if not np.isfinite([p,lo,hi]).all(): failure.append('estimación o réplicas indefinidas')
        if hi-lo > .20: failure.append('ancho IC>0.20')
        if p > 0 and cv > .30: failure.append('CV>0.30')
        reason = reasons[j] or ('Supresión requerida por spec: ' + '; '.join(failure) if failure else '')
        output.append({'llave': row.llave, 'punto': '' if reason else p,
                       'ic95_inf': '' if reason else lo, 'ic95_sup': '' if reason else hi,
                       'estado': 'NO-RECALCULABLE-DESDE-SPEC' if reason else 'RECONSTRUIDO', 'motivo': reason})
        diagnostics.append({'llave': row.llave, 'n_conocido': counts[j], 'upm_con_casos': clusters[j],
                            'ancho_ic': None if reason else hi-lo, 'cv': None if reason else cv})
    pd.DataFrame(output).to_csv(ROOT / 'reconstruccion.tsv', sep='\t', index=False, float_format='%.17g')
    pd.DataFrame(diagnostics).to_csv(ROOT / 'diagnosticos.tsv', sep='\t', index=False, float_format='%.17g')
    # Las réplicas publicadas contienen únicamente agregados de celdas no suprimidas.
    published = [j for j, out in enumerate(output) if out['estado'] == 'RECONSTRUIDO']
    rep_table = pd.DataFrame(reps[:, published], columns=keys.iloc[published].llave)
    rep_table.index = np.arange(1,B+1)
    rep_table.to_csv(ROOT / 'replicas.tsv', sep='\t', index_label='replica', float_format='%.17g')
    write_json('recibo.json', {'manifiesto_sha256_recibido': sha(ENT / 'manifiesto.json'),
        'manifiesto_recibido': manifest, 'entradas': {p.name: sha(p) for p in sorted(ENT.iterdir())},
        'insumos': raw_receipt, 'entradas_zip': members,
        'alcance': 'Solo /entrada y /raw; sin consulta de resultados esperados ni contacto con preparador.',
        'semilla': SEED, 'replicas': B, 'rng': 'numpy.random.Generator(PCG64)',
        'versiones': {'python': platform.python_version(), 'numpy': np.__version__, 'pandas': pd.__version__},
        'auditoria': {'filas_xi': len(xi), 'filas_dem': len(dem), 'elegibles': int(eligible.sum()),
                     'conocidas_elegibles': int(include.sum()), 'desconocidas_elegibles': int((eligible & ~known).sum()),
                     'upm_marco': len(psu), 'estratos': len(strata), 'singleton': sum(len(s)==1 for s in strata)},
        'estados': pd.Series([o['estado'] for o in output]).value_counts().to_dict()})
    print(json.dumps({'estados': pd.Series([o['estado'] for o in output]).value_counts().to_dict(), 'nacional': output[0]}, ensure_ascii=False))


if __name__ == '__main__':
    main()
