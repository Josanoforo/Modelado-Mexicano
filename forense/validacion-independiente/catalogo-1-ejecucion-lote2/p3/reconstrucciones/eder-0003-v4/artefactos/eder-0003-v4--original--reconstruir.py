#!/usr/bin/env python3
"""Reconstrucción ciega, exclusivamente con /entrada y /raw."""
import csv
import hashlib
import json
import platform
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
ENTRADA = Path('/entrada')
RAW = Path('/raw')
KEY = ['folioviv', 'foliohog', 'id_pobla']
LIBRE = {'1', '12', '13', '14', '17', '18', '126'}
DIRECTO = {'2', '3', '4', '26', '27', '28', '46', '47', '48'}


def digest(stream):
    h = hashlib.sha256()
    for block in iter(lambda: stream.read(1024 * 1024), b''):
        h.update(block)
    return h.hexdigest()


def sha(path):
    with path.open('rb') as stream:
        return digest(stream)


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    inventory = []
    manifest = json.loads((ENTRADA / 'manifiesto.json').read_text())
    for path in sorted(ENTRADA.iterdir()):
        observed = sha(path)
        expected = manifest['archivos'].get(path.name)
        if expected:
            assert expected == observed, f'Hash diferente: {path}'
        inventory.append(dict(ruta=str(path), bytes=path.stat().st_size,
                              sha256=observed, sha256_declarado=expected))
    inputs = json.loads((ENTRADA / 'insumos.json').read_text())
    paths = {}
    for item in inputs:
        path = RAW / item['id'] / Path(item['archivo']).name
        observed = sha(path)
        assert observed == item['sha256'], f'Hash diferente: {path}'
        paths[item['id']] = path
        inventory.append(dict(ruta=str(path), bytes=path.stat().st_size,
                              sha256=observed, entrada=item))
    archive = paths['eder_2017_eder2017_bases_csv']
    with zipfile.ZipFile(archive) as z:
        for member in z.infolist():
            with z.open(member) as f:
                inventory.append(dict(archivo=str(archive), miembro=member.filename,
                                      bytes=member.file_size, sha256=digest(f)))
        def read(name, cols):
            with z.open(name) as f:
                return pd.read_csv(f, usecols=cols, dtype=str, keep_default_na=False)
        ant = read('antecedentes.csv', KEY + ['factor_per'])
        viv = read('vivienda.csv', ['folioviv', 'est_dis', 'upm'])
        assert not ant.duplicated(KEY).any(), 'Identidad duplicada en antecedentes'
        assert not viv.duplicated(['folioviv']).any(), 'Identidad duplicada en vivienda'
        candidates, seen, people = [], set(), set()
        total_rows = 0
        with z.open('historiavida.csv') as f:
            for chunk in pd.read_csv(f, usecols=KEY + ['anio_retro', 'edo_civil1'],
                                     dtype=str, keep_default_na=False, chunksize=100000):
                total_rows += len(chunk)
                for row in chunk[KEY + ['anio_retro']].itertuples(index=False, name=None):
                    assert row not in seen, 'Persona-año duplicada: método no resuelve empate'
                    seen.add(row)
                    people.add(row[:3])
                assert chunk['edo_civil1'].str.fullmatch(r'[0-9]+').all(), 'Código vacío/ambiguo'
                nonzero = chunk.loc[chunk['edo_civil1'].ne('0')].copy()
                nonzero['anio_retro'] = pd.to_numeric(nonzero['anio_retro'], errors='raise')
                candidates.append(nonzero.sort_values('anio_retro').drop_duplicates(KEY))
        first = (pd.concat(candidates).sort_values('anio_retro')
                 .drop_duplicates(KEY).sort_values(KEY))
    merged = first.merge(ant, on=KEY, how='left', validate='one_to_one', indicator=True)
    assert merged['_merge'].eq('both').all(), 'Falta enlace de identidad en antecedentes'
    merged['w'] = pd.to_numeric(merged['factor_per'], errors='coerce')
    valid = np.isfinite(merged['w']) & merged['w'].gt(0)
    universe = merged.loc[valid].drop(columns='_merge').merge(
        viv, on='folioviv', how='left', validate='many_to_one', indicator=True)
    assert universe['_merge'].eq('both').all(), 'Falta enlace de identidad en vivienda'
    assert universe[['est_dis', 'upm']].map(lambda s: bool(s.strip())).all().all()
    universe['libre_w'] = universe.w * universe.edo_civil1.isin(LIBRE)
    universe['directo_w'] = universe.w * universe.edo_civil1.isin(DIRECTO)
    sums = universe[['w', 'libre_w', 'directo_w']].sum().to_numpy(dtype=float)
    p = sums[1:] / sums[0]
    # Marco de remuestreo: UPM presentes en el universo analítico.
    # Orden lexicográfico de las cadenas crudas; una secuencia PCG64 compartida.
    clusters = universe.groupby(['est_dis', 'upm'], sort=True)[['w', 'libre_w', 'directo_w']].sum()
    rng = np.random.Generator(np.random.PCG64(20260915))
    rep = np.zeros((2000, 3))
    singleton = 0
    for _, frame in clusters.groupby(level=0, sort=True):
        values = frame.to_numpy(dtype=float)
        n = len(values)
        singleton += int(n == 1)
        draw = rng.integers(0, n, size=(2000, n))
        rep += values[draw].sum(axis=1)
    assert (rep[:, 0] > 0).all()
    intervals = np.percentile(rep[:, 1:] / rep[:, :1], [2.5, 97.5], axis=0, method='linear')
    method_ic = 'IC-CON-ESTRATOS-DE-UPM-UNICA' if singleton else 'BOOTSTRAP-UPM-ESTRATIFICADO'
    mapping = {'RESULT-EDER-UNION-A-P-LIBRE': 0, 'RESULT-EDER-UNION-A-P-DIRECTO': 1}
    with (ENTRADA / 'estimandos.tsv').open(newline='') as f:
        reader = csv.DictReader(f, delimiter='\t')
        fields = reader.fieldnames + ['estado', 'valor', 'ic_025', 'ic_975', 'metodo_ic', 'motivo']
        rows = list(reader)
    for row in rows:
        index = mapping.get(row['llave'])
        if index is None:
            row.update(estado='NO-RECALCULABLE-DESDE-SPEC', motivo='Llave sin correspondencia explícita en el método.')
        else:
            row.update(estado='RECONSTRUIDO', valor=format(p[index], '.17g'),
                       ic_025=format(intervals[0, index], '.17g'),
                       ic_975=format(intervals[1, index], '.17g'), metodo_ic=method_ic, motivo='')
    with (ROOT / 'reconstruccion.tsv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)
    unclassified = ~universe.edo_civil1.isin(LIBRE | DIRECTO)
    partition = float((sums[1] + sums[2] + universe.loc[unclassified, 'w'].sum()) / sums[0])
    assert abs(partition - 1) < 1e-12
    save('diagnostico.json', dict(
        filas_historia=total_rows, personas_historia=len(people), personas_con_codigo_no_cero=len(first),
        personas_excluidas_por_peso=int((~valid).sum()), personas_universo=len(universe),
        suma_pesos=float(sums[0]), numerador_libre=float(sums[1]), numerador_directo=float(sums[2]),
        personas_sin_clasificar=int(unclassified.sum()),
        peso_sin_clasificar=float(universe.loc[unclassified, 'w'].sum()),
        codigos_primer_no_cero=universe.edo_civil1.value_counts().sort_index().to_dict(),
        estratos=int(clusters.index.get_level_values(0).nunique()), upm_por_estrato_total=len(clusters),
        estratos_upm_unica=singleton,
        **{'G-VEREDICTO-TIPO-CODIGO': 'CADENA-CRUDA; dtype=str; sin normalización numérica',
           'A-SUMA-LIBRE-DIRECTO-MAS-SIN-CLASIFICAR': partition,
           'A-METODO-IC': method_ic}))
    save('inventario.json', inventory)
    save('recibo.json', dict(
        paquete=manifest['paquete'], version_entrada=manifest['version_entrada'],
        manifiesto_ruta='/entrada/manifiesto.json', manifiesto_sha256=sha(ENTRADA / 'manifiesto.json'),
        entradas_permitidas=['/entrada', '/raw'], resultados_esperados_consultados=False,
        revelacion_solicitada=False, tolerancia=json.loads((ENTRADA / 'tolerancia.json').read_text()),
        entorno=dict(python=platform.python_version(), numpy=np.__version__, pandas=pd.__version__),
        artefactos_sha256={name: sha(ROOT / name) for name in
                          ['reconstruir.py', 'reconstruccion.tsv', 'diagnostico.json', 'inventario.json']}))


if __name__ == '__main__':
    main()
