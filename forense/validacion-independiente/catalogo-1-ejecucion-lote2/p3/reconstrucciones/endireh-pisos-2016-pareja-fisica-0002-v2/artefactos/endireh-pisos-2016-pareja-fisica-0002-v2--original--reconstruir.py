#!/usr/bin/env python3
"""Reconstrucción independiente; no asigna ventanas a llaves opacas."""
import csv
import hashlib
import json
import platform
import shutil
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
ENTRADA = Path('/entrada')
RAW = Path('/raw')
SEED, B = 20260923, 500


def sha_file(path):
    with open(path, 'rb') as f:
        return sha_stream(f)


def sha_stream(f):
    h = hashlib.sha256()
    for block in iter(lambda: f.read(1024 * 1024), b''):
        h.update(block)
    return h.hexdigest()


def write_json(name, value):
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def union(x):
    return np.where(np.isin(x, [1, 2, 3]).any(axis=1), 1.,
                    np.where((x == 4).all(axis=1), 0., np.nan))


def responses(life, recent):
    a = union(life)
    corrected = np.where(life == 4, 4, recent)
    b = union(corrected)
    b[np.isnan(a)] = np.nan
    return a, b


def main():
    manifest_hash = sha_file(ENTRADA / 'manifiesto.json')
    manifest = json.loads((ENTRADA / 'manifiesto.json').read_text())
    inventory = []
    (BASE / 'entrada').mkdir(exist_ok=True)
    for name in ['manifiesto.json', *manifest['archivos']]:
        p = ENTRADA / name
        digest = sha_file(p)
        if name in manifest['archivos']:
            assert digest == manifest['archivos'][name], f'Hash incorrecto: {name}'
        inventory.append(dict(tipo='entrada', ruta=str(p), sha256=digest, bytes=p.stat().st_size))
        shutil.copyfile(p, BASE / 'entrada' / name)
    sources = json.loads((ENTRADA / 'insumos.json').read_text())
    zip_path = None
    for source in sources:
        p = RAW / source['id'] / Path(source['archivo']).name
        digest = sha_file(p)
        assert digest == source['sha256'], f'Hash incorrecto: {p}'
        inventory.append(dict(tipo='insumo', ruta=str(p), sha256=digest,
                              bytes=p.stat().st_size, entrada=source))
        if p.suffix == '.zip':
            zip_path = p
    assert zip_path is not None
    with zipfile.ZipFile(zip_path) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            with z.open(info) as f:
                digest = sha_stream(f)
            inventory.append(dict(tipo='miembro_zip', archivo=str(zip_path),
                                  entrada=info.filename, bytes=info.file_size, sha256=digest))
            if info.filename.endswith('/fd_endireh2016_dbf.pdf'):
                assert digest == 'd6b1805e4e0eae0d12df5acd834e4913e59e56dcc101d80d1036535e8c3f1cba'
        prefix = 'bd_mujeres_endireh2016_sitioinegi_csv/'
        a_cols = [f'P13_1_{i}' for i in range(1, 10)]
        b_cols = [f'P13_3_{i}' for i in range(1, 10)]
        cols = ['ID_MUJ', 'T_INSTRUM', 'FAC_MUJ', 'EST_DIS', 'UPM_DIS', 'DOMINIO', 'CVE_ENT'] + a_cols + b_cols
        with z.open(prefix + 'TB_SEC_XIII.csv') as f:
            module = pd.read_csv(f, usecols=cols, dtype=str, encoding='latin1')
        with z.open(prefix + 'TSDem.csv') as f:
            dem = pd.read_csv(f, usecols=['ID_MUJ', 'EDAD', 'NIV'], dtype=str, encoding='latin1')
    write_json('inventario.json', inventory)
    assert not module.ID_MUJ.duplicated().any()
    assert not dem.ID_MUJ.duplicated().any()
    sample = module.loc[module.T_INSTRUM.isin(['A1', 'A2'])].copy()
    assert sample[['EST_DIS', 'UPM_DIS']].notna().all().all()
    # Marco completo A1/A2 anterior a filtros de elegibilidad y respuesta.
    frame = sample[['EST_DIS', 'UPM_DIS']].drop_duplicates().sort_values(['EST_DIS', 'UPM_DIS']).reset_index(drop=True)
    frame['cluster_index'] = np.arange(len(frame))
    data = sample.merge(dem, on='ID_MUJ', how='left', validate='one_to_one', indicator=True)
    assert (data['_merge'] == 'both').all(), 'Falta correspondencia demográfica'
    for col in ['FAC_MUJ', 'EDAD', 'NIV'] + a_cols + b_cols:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    eligible = (data.FAC_MUJ > 0) & data.EDAD.between(15, 120)
    excluded = int((~eligible).sum())
    data = data.loc[eligible].merge(frame, on=['EST_DIS', 'UPM_DIS'], validate='many_to_one')
    life, recent = responses(data[a_cols].to_numpy(), data[b_cols].to_numpy())
    domains = [('nacional', 'MX', np.ones(len(data), dtype=bool))]
    for label, low, high in [('15-29',15,29),('30-44',30,44),('45-59',45,59),('60+',60,120)]:
        domains.append(('edad', label, data.EDAD.between(low, high).to_numpy()))
    for label, codes in [('ninguno',[0]),('basica',[1,2,3,5,6]),('media_superior',[4,7,8]),('superior',[9,10,11])]:
        domains.append(('escolaridad', label, data.NIV.isin(codes).to_numpy()))
    for axis, col, labels in [('localidad','DOMINIO',['U','C','R']), ('pareja','T_INSTRUM',['A1','A2']), ('entidad','CVE_ENT',[f'{i:02d}' for i in range(1,33)])]:
        for label in labels:
            domains.append((axis, label, (data[col] == label).to_numpy()))
    rng = np.random.Generator(np.random.PCG64(SEED))
    multiplicities = np.zeros((B, len(frame)), dtype=np.int32)
    singleton = 0
    for _, block in frame.groupby('EST_DIS', sort=True):
        ix = block.cluster_index.to_numpy()
        n = len(ix)
        singleton += n == 1
        multiplicities[:, ix] = rng.multinomial(n, np.full(n, 1. / n), size=B)
        assert (multiplicities[:, ix].sum(axis=1) == n).all()
    weights = data.FAC_MUJ.to_numpy(dtype=float)
    clusters = data.cluster_index.to_numpy()
    results, replicas = [], []
    for window, outcome in [('desde_inicio_relacion_P13_1', life), ('octubre_2015_a_entrevista_P13_3', recent)]:
        for axis, label, mask in domains:
            known = mask & np.isfinite(outcome)
            positive = known & (outcome == 1)
            den = np.bincount(clusters[known], weights=weights[known], minlength=len(frame))
            num = np.bincount(clusters[positive], weights=weights[positive], minlength=len(frame))
            p = num.sum() / den.sum() if den.sum() else np.nan
            rep_den = multiplicities @ den
            rep_num = multiplicities @ num
            rep = np.divide(rep_num, rep_den, out=np.full(B, np.nan), where=rep_den > 0)
            all_valid = np.isfinite(rep).all()
            lo, hi = np.quantile(rep, [.025, .975], method='linear') if all_valid else [np.nan, np.nan]
            se = np.std(rep, ddof=1) if all_valid else np.nan
            cv = se / p if p > 0 else np.nan
            # 'UPM con casos' = UPM con respuesta conocida que aporta al denominador.
            upm = int((den > 0).sum())
            reasons = []
            if known.sum() < 100: reasons.append('n_conocida<100')
            if upm < 5: reasons.append('upm_con_respuesta<5')
            if not all_valid: reasons.append('replica_sin_denominador')
            if np.isfinite(hi) and hi - lo > .20: reasons.append('ancho_ic>0.20')
            if p > 0 and cv > .30: reasons.append('cv>0.30')
            publish = not reasons
            results.append(dict(ventana=window, eje=axis, segmento=label,
                                n_conocida=int(known.sum()), n_desconocida=int((mask & ~np.isfinite(outcome)).sum()),
                                upm_con_respuesta=upm, publicable=publish, motivo=';'.join(reasons),
                                proporcion=p if publish else None, ic95_inf=lo if publish else None,
                                ic95_sup=hi if publish else None, error_estandar=se if publish else None,
                                cv=cv if publish else None))
            for i in range(B):
                replicas.append(dict(ventana=window, eje=axis, segmento=label, replica=i+1,
                                     numerador=rep_num[i], denominador=rep_den[i], proporcion=rep[i]))
    pd.DataFrame(results).to_csv(BASE/'calculos_por_ventana.tsv', sep='\t', index=False, float_format='%.17g')
    pd.DataFrame(replicas).to_csv(BASE/'replicas_agregadas.tsv', sep='\t', index=False, float_format='%.17g')
    requested = pd.read_csv(ENTRADA/'estimandos.tsv', sep='\t', dtype=str)
    assert not requested.llave.duplicated().any()
    assert set(zip(requested.eje, requested.segmento)) == {(a,b) for a,b,_ in domains}
    requested['estado'] = 'NO-RECALCULABLE-DESDE-SPEC'
    requested['motivo'] = ('Falta asignación explícita llave→ventana: el método define P13_1 y P13_3, '
                           'pero estimandos.tsv no identifica la ventana; no se infiere del índice celda ni del orden.')
    for col in ['proporcion', 'ic95_inf', 'ic95_sup']:
        requested[col] = ''
    requested.to_csv(BASE/'reconstruccion.tsv', sep='\t', index=False)
    audit = dict(filas_modulo=len(module), filas_tsdem=len(dem), filas_A1_A2=len(sample),
                 excluidas_factor_edad=excluded, elegibles=len(data), upm_marco=len(frame),
                 estratos=int(frame.EST_DIS.nunique()), estratos_singleton=int(singleton),
                 conocidas_P13_1=int(np.isfinite(life).sum()), conocidas_P13_3=int(np.isfinite(recent).sum()),
                 celdas_calculadas=len(results), celdas_publicables=sum(r['publicable'] for r in results),
                 replicas_agregadas=len(replicas), llaves=len(requested),
                 estados=requested.estado.value_counts().to_dict())
    write_json('auditoria.json', audit)
    outputs = ['reconstruir.py','reconstruccion.tsv','calculos_por_ventana.tsv','replicas_agregadas.tsv','inventario.json','auditoria.json']
    write_json('recibo.json', dict(manifiesto_sha256=manifest_hash, paquete=manifest['paquete'],
               entradas='/entrada', insumos='/raw', resultados_esperados_accedidos=False,
               revelacion_solicitada=False, asignacion_de_identidad_inferida=False,
               fase='congelación anterior a revelación',
               entorno=dict(python=platform.python_version(), numpy=np.__version__, pandas=pd.__version__),
               bootstrap=dict(replicas=B, semilla=SEED, generador='PCG64',
                              orden='EST_DIS, UPM_DIS lexicográfico; por estrato, 500 multinomiales',
                              percentil='lineal', desviacion_estandar_ddof=1),
               salidas_sha256={name:sha_file(BASE/name) for name in outputs}, resumen=audit))
    print(json.dumps(audit, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
