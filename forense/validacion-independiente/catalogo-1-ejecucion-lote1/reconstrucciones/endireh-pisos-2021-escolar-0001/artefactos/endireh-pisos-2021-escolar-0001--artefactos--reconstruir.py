#!/usr/bin/env python3
"""Implementación independiente; no asigna períodos a llaves sin identidad temporal."""
import csv
import hashlib
import json
from pathlib import Path
import platform
import zipfile
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
RAW = Path('/raw')
SEED = 20260923
B = 200

def digest(path):
    with open(path, 'rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def dump(name, obj):
    (BASE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def unions(a, b, life_eligible, recent_eligible):
    life = np.where((a == 1).any(axis=1), 1., np.where((a == 2).all(axis=1), 0., np.nan))
    life[~life_eligible] = np.nan
    adjusted = np.where(a == 2, 4, b)
    recent = np.where(np.isin(adjusted, [1, 2, 3]).any(axis=1), 1.,
                      np.where((adjusted == 4).all(axis=1), 0., np.nan))
    recent[~recent_eligible | np.isnan(life)] = np.nan
    return life, recent

def main():
    # Verificar antes de producir cifras; preservar manifiesto recibido sin modificar.
    manifest = json.loads((BASE / 'entrada/manifiesto.json').read_text())
    for name, expected in manifest['archivos'].items():
        assert digest(BASE / 'entrada' / name) == expected, name
    inputs = json.loads((BASE / 'entrada/insumos.json').read_text())
    observed = []
    for item in inputs:
        suffix = '.zip' if item['id'].endswith('_zip') else '.pdf'
        path = RAW / (item['id'] + suffix)
        actual = digest(path)
        assert actual == item['sha256'], path
        observed.append(dict(entrada=item, ruta_recibida=str(path), sha256_observado=actual,
                             bytes=path.stat().st_size))
    z = zipfile.ZipFile(RAW / 'endireh2021_bd_csv_zip.zip')
    entries = []
    for info in z.infolist():
        with z.open(info) as f:
            h = hashlib.file_digest(f, 'sha256').hexdigest()
        entries.append(dict(entrada=info.filename, bytes=info.file_size, sha256=h))
    dump('recibo.json', dict(sha256_manifiesto_recibido=digest(BASE / 'entrada/manifiesto.json'),
         manifiesto_recibido=manifest, insumos=observed, entradas_zip=entries,
         acceso='Solo /entrada y /raw; no se buscaron ni consultaron reservas o resultados esperados.',
         revelacion_solicitada=False))

    def read(name, cols):
        return pd.read_csv(z.open('bd_endireh_2021_csv/' + name), usecols=cols,
                           dtype=str, keep_default_na=False, encoding='latin1')
    life_cols = [f'P7_6_{j}' for j in range(1, 19)]
    recent_cols = [f'P7_8_{j}' for j in range(1, 19)]
    s = read('TB_SEC_VII.csv', ['ID_PER','FAC_MUJ','EST_DIS','UPM_DIS','P7_1','P7_2',
             'DOMINIO','CVE_ENT','T_INSTRUM'] + life_cols + recent_cols)
    d = read('TSDem.csv', ['ID_PER','EDAD','NIV','SEXO'])
    assert not s.ID_PER.duplicated().any()
    assert not d.ID_PER.duplicated().any()
    s = s.merge(d, on='ID_PER', how='left', validate='one_to_one', indicator=True)
    assert s['_merge'].eq('both').all()
    assert s.SEXO.eq('2').all()
    # Marco de UPM antes de filtrar elegibilidad o dominio: incluye UPM sin casos.
    assert s[['EST_DIS','UPM_DIS']].ne('').all().all()
    frame = s[['EST_DIS','UPM_DIS']].drop_duplicates().sort_values(['EST_DIS','UPM_DIS'])
    pairs = list(frame.itertuples(index=False, name=None))
    index = {p: i for i, p in enumerate(pairs)}
    cluster = np.array([index[p] for p in s[['EST_DIS','UPM_DIS']].itertuples(index=False, name=None)])
    strata = [np.array([index[p] for p in g.itertuples(index=False, name=None)])
              for _, g in frame.groupby('EST_DIS', sort=True)]
    # PCG64 explícito; B sorteos con reemplazo de n_h UPM en cada estrato.
    rng = np.random.Generator(np.random.PCG64(SEED))
    multiplicity = np.zeros((B, len(frame)), dtype=np.int16)
    for r in range(B):
        for ids in strata:
            if len(ids) == 1:
                multiplicity[r, ids[0]] = 1
            else:
                sampled = rng.choice(ids, size=len(ids), replace=True)
                np.add.at(multiplicity[r], sampled, 1)
    w = pd.to_numeric(s.FAC_MUJ, errors='coerce').to_numpy(float)
    age = pd.to_numeric(s.EDAD, errors='coerce').to_numpy(float)
    valid = np.isfinite(w) & (w > 0) & (age >= 15) & (age <= 120)
    valid &= s.T_INSTRUM.isin(['A1','A2','B1','B2','C1','C2']).to_numpy()
    a = s[life_cols].apply(pd.to_numeric, errors='coerce').to_numpy(float)
    b = s[recent_cols].apply(pd.to_numeric, errors='coerce').to_numpy(float)
    eligible = valid & s.P7_1.eq('1').to_numpy()
    life, recent = unions(a, b, eligible, eligible & s.P7_2.eq('1').to_numpy())
    domains = [('nacional','MX', np.ones(len(s), dtype=bool))]
    for label, lo, hi in [('15-29',15,29),('30-44',30,44),('45-59',45,59),('60+',60,120)]:
        domains.append(('edad',label,(age >= lo) & (age <= hi)))
    for label, codes in [('ninguno',['00']),('basica',['01','02','03','05','06']),
                         ('media_superior',['04','07','08']),('superior',['09','10','11'])]:
        domains.append(('escolaridad',label,s.NIV.isin(codes).to_numpy()))
    for axis, col, codes in [('localidad','DOMINIO',['U','C','R']),
                             ('pareja','T_INSTRUM',['A1','A2','B1','B2','C1','C2']),
                             ('entidad','CVE_ENT',[f'{i:02d}' for i in range(1,33)])]:
        for code in codes:
            domains.append((axis,code,s[col].eq(code).to_numpy()))
    rows, reps = [], []
    for period, y in [('vida',life),('reciente',recent)]:
        for axis, segment, mask in domains:
            known = mask & np.isfinite(y)
            n = int(known.sum())
            k = len(np.unique(cluster[known]))
            num = np.bincount(cluster[known], weights=w[known]*y[known], minlength=len(frame))
            den = np.bincount(cluster[known], weights=w[known], minlength=len(frame))
            point = num.sum()/den.sum() if den.sum() else np.nan
            rd = multiplicity @ den
            rn = multiplicity @ num
            estimates = np.divide(rn,rd,out=np.full(B,np.nan),where=rd>0)
            reasons = []
            if n < 100: reasons.append('n conocido < 100')
            if k < 5: reasons.append('UPM con casos < 5')
            if not np.isfinite(estimates).all():
                reasons.append('réplicas sin denominador; spec no define tratamiento')
                low = high = cv = np.nan
            else:
                low, high = np.quantile(estimates,[.025,.975],method='linear')
                cv = np.std(estimates,ddof=1)/point if point > 0 else np.nan
                if high-low > .20: reasons.append('ancho IC > 0.20')
                if point > 0 and cv > .30: reasons.append('CV > 0.30')
            public = not reasons
            rows.append(dict(periodo=period,eje=axis,segmento=segment,
                punto=point if public else '',ic95_inf=low if public else '',ic95_sup=high if public else '',
                n_conocido=n,upm_con_casos=k,publicable=public,motivo='; '.join(reasons)))
            if public:
                for r, val in enumerate(estimates):
                    reps.append(dict(periodo=period,eje=axis,segmento=segment,replica=r+1,punto=val))
    pd.DataFrame(rows).to_csv(BASE/'calculos_sin_asignar.tsv',sep='\t',index=False,float_format='%.17g')
    pd.DataFrame(reps).to_csv(BASE/'replicas_publicables.tsv',sep='\t',index=False,float_format='%.17g')
    requested = pd.read_csv(BASE/'entrada/estimandos.tsv',sep='\t',dtype=str,keep_default_na=False)
    assert not requested.llave.duplicated().any()
    assert 'periodo' not in requested.columns
    reconstruction = requested[['llave']].copy()
    for col in ['punto','ic95_inf','ic95_sup']: reconstruction[col] = ''
    reconstruction['estado'] = 'NO-RECALCULABLE-DESDE-SPEC'
    reconstruction['motivo'] = ('Identidad temporal ausente: metodo.md define vida y reciente, '
        'pero estimandos.tsv no asigna periodo a la llave; celda no tiene regla semantica documentada.')
    reconstruction.to_csv(BASE/'reconstruccion.tsv',sep='\t',index=False)
    dump('ejecucion.json',dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,
        rng='numpy.random.Generator(PCG64)',semilla=SEED,replicas=B,
        orden='replica, estrato lexicografico, UPM lexicografica; singletons sin consumo RNG',
        percentil='numpy.quantile(method=linear)',cv='std(replicas, ddof=1)/p si p>0',
        filas_modulo=len(s),filas_validas=int(valid.sum()),estratos=len(strata),upm=len(frame),
        singleton=sum(len(ids)==1 for ids in strata),conocidos_vida=int(np.isfinite(life).sum()),
        conocidos_reciente=int(np.isfinite(recent).sum()),llaves=len(requested),
        calculos=len(rows),publicables=sum(r['publicable'] for r in rows),
        no_publicables=sum(not r['publicable'] for r in rows)))

if __name__ == '__main__':
    main()
