#!/usr/bin/env python3
"""Reconstrucción independiente a partir de las entradas congeladas y /raw."""
import argparse
import csv
import hashlib
import json
import platform
import zipfile
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 20260923
REPLICAS = 500
CONDUCTAS = {
    'dinero_libre': ('P4_11', {'1': 1., '2': 0.}),
    'decide_sobre_dinero_ella': ('P15_1AB_3', {'1': 1., '4': 1., '5': 1., '2': 0., '3': 0.}),
    'decide_gasto_ella': ('P15_1AB_7', {'1': 1., '4': 1., '5': 1., '2': 0., '3': 0.}),
}

def sha_stream(stream):
    h = hashlib.sha256()
    for block in iter(lambda: stream.read(1024 * 1024), b''):
        h.update(block)
    return h.hexdigest()

def sha(path):
    with path.open('rb') as f:
        return sha_stream(f)

def save_json(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def domain(d, eje, segmento):
    if eje == 'nacional' and segmento == 'MX':
        return np.ones(len(d), dtype=bool)
    if eje == 'edad':
        bounds = {'15-29': (15,29), '30-44': (30,44), '45-59': (45,59), '60+': (60,120)}
        if segmento in bounds:
            return d.edad.between(*bounds[segmento]).to_numpy()
    if eje == 'escolaridad':
        codes = {'ninguno': ['00'], 'basica': ['01','02','03','05','06'],
                 'media_superior': ['04','07','08'], 'superior': ['09','10','11']}
        if segmento in codes:
            return d.NIV.isin(codes[segmento]).to_numpy()
    for axis, col, values in [('localidad','DOMINIO',['U','C','R']),
                              ('pareja','T_INSTRUM',['A1','A2']),
                              ('entidad','CVE_ENT',[f'{i:02d}' for i in range(1,33)])]:
        if eje == axis and segmento in values:
            return d[col].eq(segmento).to_numpy()
    raise ValueError('Identidad de dominio no documentada')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw', type=Path, default=Path('/raw'))
    parser.add_argument('--salida', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    out = args.salida
    out.mkdir(parents=True, exist_ok=True)
    entrada = base / 'entradas'
    manifiesto = json.loads((entrada/'manifiesto.json').read_text())
    for name, expected in manifiesto['archivos'].items():
        assert sha(entrada/name) == expected, f'Entrada alterada: {name}'
    inventory = []
    for item in json.loads((entrada/'insumos.json').read_text()):
        path = args.raw / (item['id'] + ('.zip' if item['id'].endswith('_zip') else '.pdf'))
        actual = sha(path)
        assert actual == item['sha256'], f'Insumo alterado: {path}'
        inventory.append({'id': item['id'], 'archivo_declarado': item['archivo'],
                          'ruta_recibida': str(path), 'bytes': path.stat().st_size,
                          'sha256': actual, 'url_declarada': item['url']})
    save_json(out/'inventario_raw.json', inventory)
    z = zipfile.ZipFile(args.raw/'endireh2021_bd_csv_zip.zip')
    entries = []
    for info in z.infolist():
        with z.open(info) as f:
            entries.append({'entrada': info.filename, 'bytes': info.file_size,
                            'crc32': f'{info.CRC:08x}', 'sha256': sha_stream(f)})
    save_json(out/'inventario_zip.json', entries)
    def read(name, cols):
        d = pd.read_csv(z.open('bd_endireh_2021_csv/'+name+'.csv'), usecols=cols,
                        dtype=str, encoding='latin1', keep_default_na=False)
        for col in d:
            d[col] = d[col].str.strip()
        assert not d.loc[d.ID_PER.ne(''), 'ID_PER'].duplicated().any(), name
        return d
    xv = read('TB_SEC_XV', ['ID_PER','T_INSTRUM','FAC_MUJ','EST_DIS','UPM_DIS',
                           'DOMINIO','CVE_ENT','P15_1AB_3','P15_1AB_7'])
    iv = read('TB_SEC_IV', ['ID_PER','P4_11'])
    dem = read('TSDem', ['ID_PER','EDAD','NIV','SEXO'])
    a = xv[xv.T_INSTRUM.isin(['A1','A2'])].copy()
    assert a.EST_DIS.ne('').all() and a.UPM_DIS.ne('').all()
    # Marco antes de cualquier exclusión de edad, factor o respuesta.
    psus = a[['EST_DIS','UPM_DIS']].drop_duplicates().sort_values(['EST_DIS','UPM_DIS'])
    psus = psus.reset_index(drop=True)
    psus['psu_idx'] = np.arange(len(psus))
    a = a.merge(psus, on=['EST_DIS','UPM_DIS'], validate='many_to_one')
    d = a[a.ID_PER.ne('')].merge(iv[iv.ID_PER.ne('')], on='ID_PER', how='left',
                                validate='one_to_one', indicator='join_iv')
    d = d.merge(dem[dem.ID_PER.ne('')], on='ID_PER', how='left',
                validate='one_to_one', indicator='join_dem')
    d['edad'] = pd.to_numeric(d.EDAD, errors='coerce')
    d['factor'] = pd.to_numeric(d.FAC_MUJ, errors='coerce')
    eligible = d.edad.between(15,120) & d.factor.gt(0) & np.isfinite(d.factor)
    audit = {'filas_A1_A2': len(a), 'llave_vacia': int(a.ID_PER.eq('').sum()),
             'sin_IV': int(d.join_iv.ne('both').sum()), 'sin_TSDem': int(d.join_dem.ne('both').sum()),
             'excluidas_edad_factor': int((~eligible).sum()),
             'codigos_edad_98_99_incluidos_por_regla_literal': int((eligible & d.EDAD.isin(['98','99'])).sum()),
             'UPM_marco': len(psus), 'estratos': psus.EST_DIS.nunique()}
    d = d[eligible].copy()
    assert d.SEXO.eq('2').all(), 'Identidad de mujer no validada'
    keys = pd.read_csv(entrada/'estimandos.tsv', sep='\t', dtype=str, keep_default_na=False)
    assert keys.llave.is_unique
    numer = np.zeros((len(psus),len(keys)))
    denom = np.zeros_like(numer)
    diagnostics = []
    pending = {}
    for j, row in keys.iterrows():
        try:
            if row.calc != 'CALC-ENDIREH-PISOS-2021-DECISIONES-0001' or row.instrumento != 'ENDIREH' or row.ola != '2021' or row.unidad != 'proporcion' or row.naturaleza_ic != 'IC95-DE-DISENO':
                raise ValueError('Identidad de estimando no documentada')
            if row.conducta not in CONDUCTAS:
                raise ValueError('Identidad de conducta no documentada')
            col, codes = CONDUCTAS[row.conducta]
            y = d[col].map(codes).to_numpy(dtype=float)
            valid = domain(d, row.eje, row.segmento) & np.isfinite(y)
            idx = d.psu_idx.to_numpy()[valid]
            weights = d.factor.to_numpy(dtype=float)[valid]
            numer[:,j] = np.bincount(idx, weights=weights*y[valid], minlength=len(psus))
            denom[:,j] = np.bincount(idx, weights=weights, minlength=len(psus))
            diagnostics.append({'llave': row.llave, 'n_conocido': int(valid.sum()),
                                'upm_con_casos': int(np.count_nonzero(denom[:,j]))})
        except ValueError as e:
            pending[j] = str(e)
            diagnostics.append({'llave': row.llave, 'n_conocido': '', 'upm_con_casos': ''})
    # Un solo flujo PCG64. Estratos/UPM ordenados; matriz con filas de réplica.
    rng = np.random.Generator(np.random.PCG64(SEED))
    multiplicities = np.zeros((REPLICAS,len(psus)))
    singleton = 0
    for _, g in psus.groupby('EST_DIS', sort=True):
        ix = g.index.to_numpy()
        m = len(ix)
        if m == 1:
            multiplicities[:,ix] = 1
            singleton += 1
        else:
            draws = rng.integers(0,m,size=(REPLICAS,m))
            for b in range(REPLICAS):
                multiplicities[b,ix] = np.bincount(draws[b], minlength=m)
        assert np.all(multiplicities[:,ix].sum(axis=1) == m)
    with np.errstate(divide='ignore', invalid='ignore'):
        points = numer.sum(axis=0)/denom.sum(axis=0)
        boot = (multiplicities @ numer)/(multiplicities @ denom)
    rows, published = [], {}
    for j, row in keys.iterrows():
        result = {'llave': row.llave, 'punto': '', 'ic95_inf': '', 'ic95_sup': '',
                  'estado': 'NO-RECALCULABLE-DESDE-SPEC', 'motivo': ''}
        if j in pending:
            result['motivo'] = pending[j]
        else:
            p = points[j]
            b = boot[:,j]
            reasons = []
            if diagnostics[j]['n_conocido'] < 100: reasons.append('n conocido <100')
            if diagnostics[j]['upm_con_casos'] < 5: reasons.append('menos de cinco UPM con casos')
            if not np.isfinite(p) or not np.isfinite(b).all():
                reasons.append('denominador nulo en punto o réplica; spec no define su tratamiento')
            else:
                lo, hi = np.quantile(b, [0.025,0.975], method='linear')
                cv = np.std(b,ddof=1)/p if p > 0 else 0.
                if hi-lo > .20: reasons.append('ancho IC >0.20')
                if p > 0 and cv > .30: reasons.append('CV >0.30')
            if reasons:
                result['motivo'] = 'No publicable según spec: ' + '; '.join(reasons)
            else:
                assert 0 <= lo <= hi <= 1 and 0 <= p <= 1
                result.update(punto=format(p,'.17g'),ic95_inf=format(lo,'.17g'),
                              ic95_sup=format(hi,'.17g'),estado='RECONSTRUIDO')
                published[row.llave] = b
        rows.append(result)
    with (out/'reconstruccion.tsv').open('w') as f:
        w = csv.DictWriter(f,fieldnames=['llave','punto','ic95_inf','ic95_sup','estado','motivo'],delimiter='\t',lineterminator='\n')
        w.writeheader(); w.writerows(rows)
    pd.DataFrame(diagnostics).to_csv(out/'diagnostico_celdas.tsv',sep='\t',index=False)
    pd.DataFrame(published,index=np.arange(1,REPLICAS+1)).rename_axis('replica').to_csv(
        out/'replicas_publicables.tsv',sep='\t',float_format='%.17g')
    audit.update(singletons=singleton,filas_universo=len(d),estados=pd.Series([r['estado'] for r in rows]).value_counts().to_dict(),
                 semilla=SEED,replicas=REPLICAS,rng='numpy.random.PCG64',
                 python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__)
    save_json(out/'auditoria.json',audit)
    print(json.dumps(audit,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
