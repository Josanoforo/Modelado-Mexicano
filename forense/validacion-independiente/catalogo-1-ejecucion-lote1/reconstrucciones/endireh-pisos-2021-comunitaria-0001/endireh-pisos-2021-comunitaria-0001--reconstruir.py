#!/usr/bin/env python3
"""Reimplementación independiente: exclusivamente entradas locales y NumPy/pandas."""
from pathlib import Path
import csv
import hashlib
import json
import platform
import zipfile
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
SEED = 20260923
B = 200

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def unions(life, recent):
    yl = np.where((life == '1').any(axis=1), 1,
                  np.where((life == '2').all(axis=1), 0, np.nan))
    recent = np.where(life == '2', '4', recent)
    yr = np.where(np.isin(recent, ['1', '2', '3']).any(axis=1), 1,
                  np.where((recent == '4').all(axis=1), 0, np.nan))
    yr[np.isnan(yl)] = np.nan
    return yl, yr

def main():
    out = ROOT / 'salida'
    if out.exists():
        raise SystemExit('La primera ejecución se conserva: salida ya existe.')
    manifest = json.loads((ROOT / 'entrada/manifiesto.json').read_text())
    for name, expected in manifest['archivos'].items():
        assert sha(ROOT / 'entrada' / name) == expected, name
    inputs = json.loads((ROOT / 'entrada/insumos.json').read_text())
    hashes = {}
    for item in inputs:
        matches = list((ROOT / 'raw').glob(item['id'] + '.*'))
        assert len(matches) == 1
        actual = sha(matches[0])
        assert actual == item['sha256'], item['id']
        hashes[str(matches[0].relative_to(ROOT))] = actual
    keys = pd.read_csv(ROOT / 'entrada/estimandos.tsv', sep='\t', dtype=str)
    assert keys.llave.is_unique
    with zipfile.ZipFile(ROOT / 'raw/endireh2021_bd_csv_zip.zip') as z:
        def read(name, columns=None):
            with z.open('bd_endireh_2021_csv/' + name) as f:
                return pd.read_csv(f, dtype=str, keep_default_na=False,
                                   encoding='latin-1', usecols=columns)
        demo = read('TSDem.csv', ['ID_PER', 'EDAD', 'NIV', 'SEXO'])
        cols = ['ID_PER','T_INSTRUM','DOMINIO','CVE_ENT','FAC_MUJ','EST_DIS','UPM_DIS']
        cols += [f'P9_{q}_{i}' for q in (1,3) for i in range(1,17)]
        data = read('TB_SEC_IX.csv', cols)
    assert demo.ID_PER.is_unique and data.ID_PER.is_unique
    original_n = len(data)
    data = data.merge(demo, on='ID_PER', how='left', validate='one_to_one', indicator=True)
    assert (data['_merge'] == 'both').all()
    age = pd.to_numeric(data.EDAD, errors='coerce')
    weight = pd.to_numeric(data.FAC_MUJ, errors='coerce')
    eligible = (data.T_INSTRUM.isin(['A1','A2','B1','B2','C1','C2']) &
                age.between(15,120) & weight.gt(0) & data.SEXO.eq('2'))
    data = data.loc[eligible].reset_index(drop=True)
    age = pd.to_numeric(data.EDAD).to_numpy()
    weight = pd.to_numeric(data.FAC_MUJ).to_numpy(dtype=float)
    assert data.EST_DIS.ne('').all() and data.UPM_DIS.ne('').all()
    life = data[[f'P9_1_{i}' for i in range(1,17)]].to_numpy()
    recent = data[[f'P9_3_{i}' for i in range(1,17)]].to_numpy()
    assert set(np.unique(life)) <= {'', '1', '2'}
    assert set(np.unique(recent)) <= {'','1','2','3','4','9'}
    outcomes = dict(zip(['vida', 'reciente'], unions(life, recent)))
    niv_map = {'00':'ninguno', **{f'{i:02d}':'basica' for i in [1,2,3,5,6]},
               **{f'{i:02d}':'media_superior' for i in [4,7,8]},
               **{f'{i:02d}':'superior' for i in [9,10,11]}}
    segments = {'nacional':np.full(len(data),'MX'),
                'edad':np.select([age < 30, age < 45, age < 60],
                                 ['15-29','30-44','45-59'], default='60+'),
                'escolaridad':data.NIV.map(niv_map).fillna('').to_numpy(),
                'localidad':data.DOMINIO.to_numpy(),
                'pareja':data.T_INSTRUM.to_numpy(),
                'entidad':data.CVE_ENT.to_numpy()}
    # Orden lexicográfico explícito; marco completo antes de definir dominios.
    psus = sorted(set(zip(data.EST_DIS, data.UPM_DIS)))
    index = {p:i for i,p in enumerate(psus)}
    unit = np.array([index[p] for p in zip(data.EST_DIS, data.UPM_DIS)])
    strata = {}
    for i,(s,p) in enumerate(psus):
        strata.setdefault(s, []).append(i)
    rng = np.random.Generator(np.random.PCG64(SEED))
    multiplicity = np.zeros((B,len(psus)), dtype=np.int32)
    for b in range(B):
        for s in sorted(strata):
            ids = np.array(strata[s])
            draw = rng.choice(ids, size=len(ids), replace=True)
            np.add.at(multiplicity[b], draw, 1)
    cells = sorted(set(zip(keys.eje, keys.segmento)))
    estimates, replicates, audit = [], [], []
    for window,y in outcomes.items():
        for axis,segment in cells:
            mask = (segments[axis] == segment) & np.isfinite(y)
            case = mask & (y == 1)
            den = np.bincount(unit[mask], weights=weight[mask], minlength=len(psus))
            num = np.bincount(unit[case], weights=weight[case], minlength=len(psus))
            p = num.sum()/den.sum() if den.sum() else np.nan
            rd = multiplicity @ den
            rn = multiplicity @ num
            rp = np.divide(rn, rd, out=np.full(B,np.nan), where=rd > 0)
            lo,hi = np.quantile(rp,[.025,.975],method='linear')
            cv = np.std(rp,ddof=1)/p if p > 0 else 0.0
            n = int(mask.sum())
            cases_psu = int(np.count_nonzero(num))
            reasons = []
            if n < 100: reasons.append('N_MENOR_100')
            if cases_psu < 5: reasons.append('UPM_CASOS_MENOR_5')
            if not np.isfinite(rp).all(): reasons.append('REPLICA_SIN_DENOMINADOR')
            if not np.isfinite(hi-lo) or hi-lo > .20: reasons.append('ANCHO_IC')
            if p > 0 and (not np.isfinite(cv) or cv > .30): reasons.append('CV')
            state = 'SUPRIMIDA' if reasons else 'PUBLICABLE'
            estimates.append([window,axis,segment, *(['','',''] if reasons else [p,lo,hi]),state])
            audit.append([window,axis,segment,state,';'.join(reasons)])
            if not reasons:
                replicates.extend([window,axis,segment,b+1,float(rp[b])] for b in range(B))
    out.mkdir()
    def write(name, header, rows):
        with (out / name).open('w', newline='') as f:
            w = csv.writer(f,delimiter='\t',lineterminator='\n')
            w.writerow(header); w.writerows(rows)
    write('estimaciones_por_horizonte.tsv', ['horizonte','eje','segmento','punto','ic95_inf','ic95_sup','estado'], estimates)
    write('replicas_publicables.tsv', ['horizonte','eje','segmento','replica','proporcion'], replicates)
    write('supresion.tsv', ['horizonte','eje','segmento','estado','motivos'], audit)
    # Ninguna columna entregada vincula las llaves con el horizonte temporal.
    write('reconstruccion.tsv', ['llave','punto','ic95_inf','ic95_sup','estado'],
          ([k,'','','','FALTANTE_HORIZONTE_EN_LLAVE'] for k in keys.llave))
    metadata = {'sha256_manifiesto_recibido':sha(ROOT/'entrada/manifiesto.json'),
                'manifiesto_recibido':manifest, 'sha256_raw':hashes,
                'semilla':SEED,'replicas':B,'rng':'NumPy Generator PCG64',
                'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,
                'filas_ix':original_n,'mujeres_marco':len(data),'upm':len(psus),
                'estratos':len(strata),'estratos_singleton':sum(len(v)==1 for v in strata.values()),
                'conocidas':{k:int(np.isfinite(v).sum()) for k,v in outcomes.items()},
                'celdas_publicables':sum(r[-1]=='PUBLICABLE' for r in estimates),
                'llaves_sin_horizonte':len(keys)}
    (out/'ejecucion.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in metadata.items() if k not in ['manifiesto_recibido','sha256_raw']},indent=2))

if __name__ == '__main__':
    main()
