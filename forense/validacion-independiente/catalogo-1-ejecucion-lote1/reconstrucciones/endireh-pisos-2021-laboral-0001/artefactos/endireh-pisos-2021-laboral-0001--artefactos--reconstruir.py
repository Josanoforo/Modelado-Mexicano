#!/usr/bin/env python3
"""Reimplementación desde entradas recibidas, sin resultados de referencia."""
import csv
import hashlib
import io
import json
import platform
from pathlib import Path
import zipfile
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = Path('/raw')
SEED = 20260923
B = 200

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def dump(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def tsv(name, rows, fields):
    with (ROOT / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fields, delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)

def unions(life, recent, eligible_life, eligible_recent):
    v = np.where((life == 1).any(axis=1), 1.,
                 np.where((life == 2).all(axis=1), 0., np.nan))
    v[~eligible_life] = np.nan
    # Las respuestas recientes solo son válidas para actos con respuesta vida sí.
    rec = np.where(life == 2, 4., np.where(life == 1, recent, np.nan))
    r = np.where(np.isin(rec, [1, 2, 3]).any(axis=1), 1.,
                 np.where((rec == 4).all(axis=1), 0., np.nan))
    r[~eligible_recent | np.isnan(v)] = np.nan
    return v, r

def main():
    # Evita sustituir accidentalmente el primer cálculo.
    if (ROOT / 'resultados_semanticos.tsv').exists():
        raise RuntimeError('Ya existe el primer resultado: use una copia limpia para reproducir.')
    manifest = json.loads((ROOT / 'entrada/manifiesto.json').read_text())
    incoming = []
    for p in sorted((ROOT / 'entrada').iterdir()):
        digest = sha(p)
        if p.name in manifest['archivos']:
            assert digest == manifest['archivos'][p.name], p.name
        assert digest == sha(Path('/entrada') / p.name), p.name
        incoming.append({'archivo': '/entrada/' + p.name, 'sha256': digest})
    inputs = json.loads((ROOT / 'entrada/insumos.json').read_text())
    raw_inventory = []
    for spec in inputs:
        ext = '.zip' if spec['id'].endswith('_zip') else '.pdf'
        p = RAW / (spec['id'] + ext)
        digest = sha(p)
        assert digest == spec['sha256'], p
        raw_inventory.append({'ruta_recibida': str(p), 'entrada_original': spec,
                              'sha256_recalculado': digest, 'bytes': p.stat().st_size})
    dump('inventario_raw.json', raw_inventory)
    dump('recibo.json', {
        'rotulo': 'REIMPLEMENTACIÓN-INDEPENDIENTE-NO-CIEGA',
        'alcance_rotulo': 'No se certifica aislamiento del entorno. Solo se leyeron entradas y raw; no se buscaron reservas ni resultados esperados.',
        'sha256_manifiesto_recibido': sha(ROOT / 'entrada/manifiesto.json'),
        'manifiesto_recibido': manifest, 'entradas_recibidas': incoming,
        'revelacion_solicitada': False, 'resultados_esperados_consultados': False,
        'python': platform.python_version(), 'numpy': np.__version__, 'pandas': pd.__version__,
        'rng': 'numpy.random.Generator(PCG64)', 'semilla': SEED, 'replicas': B})
    estimands = list(csv.DictReader((ROOT / 'entrada/estimandos.tsv').open(), delimiter='\t'))
    assert len({r['llave'] for r in estimands}) == len(estimands)
    with zipfile.ZipFile(RAW / 'endireh2021_bd_csv_zip.zip') as z:
        entries = []
        for info in z.infolist():
            h = hashlib.sha256()
            with z.open(info) as f:
                for block in iter(lambda: f.read(1024 * 1024), b''):
                    h.update(block)
            entries.append({'entrada': info.filename, 'bytes': info.file_size,
                            'sha256': h.hexdigest(), 'crc32': f'{info.CRC:08x}'})
        dump('entradas_zip.json', entries)
        prefix = 'bd_endireh_2021_csv/'
        cols = ['ID_PER', 'DOMINIO', 'CVE_ENT', 'T_INSTRUM', 'P8_1', 'P8_4',
                'FAC_MUJ', 'EST_DIS', 'UPM_DIS']
        cols += [f'P8_{q}_{i}' for q in [9, 11] for i in range(1, 20)]
        with z.open(prefix + 'TB_SEC_VIII.csv') as f:
            d = pd.read_csv(f, encoding='latin-1', dtype=str, usecols=cols, keep_default_na=False)
        with z.open(prefix + 'TSDem.csv') as f:
            dem = pd.read_csv(f, encoding='latin-1', dtype=str, usecols=['ID_PER', 'EDAD', 'NIV', 'SEXO'], keep_default_na=False)
    assert not d.ID_PER.duplicated().any()
    assert not dem.ID_PER.duplicated().any()
    d = d.merge(dem, on='ID_PER', how='left', validate='one_to_one', indicator=True)
    assert (d['_merge'] == 'both').all()
    assert (d.SEXO == '2').all()
    # Marco completo del módulo antes de filtrar elegibilidad o dominios.
    assert (d[['EST_DIS', 'UPM_DIS']] != '').all().all()
    psus = sorted(set(zip(d.EST_DIS, d.UPM_DIS)))
    lookup = {p: i for i, p in enumerate(psus)}
    ix = np.array([lookup[p] for p in zip(d.EST_DIS, d.UPM_DIS)])
    strata = {}
    for j, (h, _) in enumerate(psus):
        strata.setdefault(h, []).append(j)
    rng = np.random.Generator(np.random.PCG64(SEED))
    multiplicity = np.zeros((B, len(psus)), dtype=np.float64)
    for ids in strata.values():
        n = len(ids)
        draws = rng.integers(0, n, size=(B, n))
        for b in range(B):
            multiplicity[b, ids] = np.bincount(draws[b], minlength=n)
        assert np.all(multiplicity[:, ids].sum(axis=1) == n)
    age = pd.to_numeric(d.EDAD, errors='coerce').to_numpy()
    weight = pd.to_numeric(d.FAC_MUJ, errors='coerce').to_numpy()
    base = (weight > 0) & np.isfinite(weight) & (age >= 15) & (age <= 120)
    base &= d.T_INSTRUM.isin(['A1','A2','B1','B2','C1','C2']).to_numpy()
    life = d[[f'P8_9_{i}' for i in range(1,20)]].apply(pd.to_numeric, errors='coerce').to_numpy()
    recent = d[[f'P8_11_{i}' for i in range(1,20)]].apply(pd.to_numeric, errors='coerce').to_numpy()
    el = base & (d.P8_1 == '1').to_numpy()
    er = el & (d.P8_4 == '1').to_numpy()
    v, r = unions(life, recent, el, er)
    education = {'00':'ninguno', **{x:'basica' for x in ['01','02','03','05','06']},
                 **{x:'media_superior' for x in ['04','07','08']},
                 **{x:'superior' for x in ['09','10','11']}}
    age_group = np.select([age < 30, age < 45, age < 60, age >= 60],
                          ['15-29','30-44','45-59','60+'], default='')
    axes = {'nacional': np.full(len(d),'MX'), 'edad': age_group,
            'escolaridad': d.NIV.map(education).fillna('').to_numpy(),
            'localidad': d.DOMINIO.to_numpy(), 'pareja': d.T_INSTRUM.to_numpy(),
            'entidad': d.CVE_ENT.to_numpy()}
    domains = sorted({(x['eje'],x['segmento']) for x in estimands})
    output, replicas = [], []
    for window, outcome in [('vida',v), ('reciente',r)]:
        for axis, segment in domains:
            known = base & (axes[axis] == segment) & np.isfinite(outcome)
            n = int(known.sum())
            npsu = int(len(np.unique(ix[known])))
            num = np.bincount(ix[known], weights=weight[known]*outcome[known], minlength=len(psus))
            den = np.bincount(ix[known], weights=weight[known], minlength=len(psus))
            point = num.sum()/den.sum() if den.sum() else np.nan
            rbden = multiplicity @ den
            rbnum = multiplicity @ num
            boot = np.divide(rbnum, rbden, out=np.full(B,np.nan), where=rbden>0)
            lo, hi = np.quantile(boot, [.025,.975], method='linear')
            cv = np.std(boot, ddof=1)/point if point > 0 else 0.
            reasons = []
            if n < 100: reasons.append('n conocido<100')
            if npsu < 5: reasons.append('UPM con casos<5')
            if not np.isfinite(boot).all(): reasons.append('réplica sin denominador')
            if hi-lo > .20: reasons.append('ancho IC>0.20')
            if point > 0 and cv > .30: reasons.append('CV>0.30')
            publish = not reasons
            row = dict(ventana=window,eje=axis,segmento=segment,n_conocido=n,upm_con_casos=npsu,
                       punto=point if publish else '',ic95_inf=lo if publish else '',
                       ic95_sup=hi if publish else '',cv=cv if publish else '',
                       publicable='SI' if publish else 'NO',motivo='; '.join(reasons))
            output.append(row)
            if publish:
                replicas.extend(dict(ventana=window,eje=axis,segmento=segment,replica=b+1,punto=p)
                                for b,p in enumerate(boot))
    tsv('resultados_semanticos.tsv', output, list(output[0]))
    tsv('replicas_agregadas.tsv', replicas, ['ventana','eje','segmento','replica','punto'])
    # Ninguna asociación de ordinales a ventanas se deriva de la documentación.
    reason = ('Identidad incompleta: la llave/celda no indica ventana vida o reciente; '
              'metodo.md no define esa correspondencia. No se infiere por orden ni ordinal.')
    rows = [dict(llave=x['llave'],punto='',ic95_inf='',ic95_sup='',
                 estado='NO-RECALCULABLE-DESDE-SPEC',motivo=reason) for x in estimands]
    tsv('reconstruccion.tsv', rows, ['llave','punto','ic95_inf','ic95_sup','estado','motivo'])
    dump('control.json', {'filas_modulo':len(d), 'filas_base':int(base.sum()),
        'upm_marco':len(psus), 'estratos':len(strata),
        'estratos_singleton':sum(len(x)==1 for x in strata.values()),
        'vida_elegibles':int(el.sum()),'vida_conocidas':int(np.isfinite(v).sum()),
        'reciente_elegibles':int(er.sum()),'reciente_conocidas':int(np.isfinite(r).sum()),
        'llaves_sin_identidad_temporal':len(rows),'calculos_semanticos':len(output),
        'calculos_publicables':sum(x['publicable']=='SI' for x in output)})
    print((ROOT / 'control.json').read_text())

if __name__ == '__main__':
    main()
