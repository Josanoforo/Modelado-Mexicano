#!/usr/bin/env python3
"""Reconstrucción independiente; sólo biblioteca estándar y NumPy."""
import csv
import hashlib
import io
import json
import platform
import struct
import zipfile
from collections import Counter
from decimal import Decimal
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
ENTRADA = Path('/entrada')
RAW = Path('/raw')
SEED, B = 20260909, 2000


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save_json(name, obj):
    (ROOT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2,
                                     allow_nan=False) + '\n')


def dbf(data, selected):
    n, h, width = struct.unpack_from('<IHH', data, 4)
    fields, offset = [], 1
    for pos in range(32, h, 32):
        if data[pos] == 13:
            break
        d = data[pos:pos + 32]
        name = d[:11].split(b'\0')[0].decode('ascii')
        fields.append(dict(nombre=name, tipo=chr(d[11]), ancho=d[16],
                           decimales=d[17], offset=offset))
        offset += d[16]
    assert offset == width and len(data) >= h + n * width
    assert selected <= {f['nombre'] for f in fields}
    wanted = [f for f in fields if f['nombre'] in selected]
    rows, deleted = [], 0
    for i in range(n):
        rec = data[h + i * width:h + (i + 1) * width]
        if rec[0:1] == b'*':
            deleted += 1
            continue
        assert rec[0:1] == b' '
        rows.append({f['nombre']: rec[f['offset']:f['offset'] + f['ancho']]
                     .decode('ascii').strip() for f in wanted})
    return rows, dict(registros_header=n, eliminados=deleted, campos=fields)


def integer(s):
    if not s:
        return -1
    value = Decimal(s)
    assert value.is_finite() and value == value.to_integral_value()
    return int(value)


def write_tsv(name, rows, columns):
    with (ROOT / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=columns, delimiter='\t',
                           lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def main():
    manifest_data = (ENTRADA / 'manifiesto.json').read_bytes()
    manifest = json.loads(manifest_data)
    inventory = []
    for p in sorted(ENTRADA.iterdir()):
        if p.is_file():
            digest = sha(p.read_bytes())
            expected = manifest['archivos'].get(p.name)
            assert expected is None or digest == expected, p
            inventory.append(dict(ruta=str(p), bytes=p.stat().st_size,
                                  sha256=digest, esperado=expected))
    inputs = json.loads((ENTRADA / 'insumos.json').read_text())
    for item in inputs:
        p = RAW / item['id'] / item['archivo']
        digest = sha(p.read_bytes())
        assert digest == item['sha256'], p
        inventory.append(dict(ruta=str(p), bytes=p.stat().st_size,
                              sha256=digest, esperado=item['sha256']))
    tolerance = json.loads((ENTRADA / 'tolerancia.json').read_text())
    assert tolerance == {'tipo': 'flotante', 'abs': 1e-10}
    keys = list(csv.DictReader(io.StringIO((ENTRADA / 'estimandos.tsv').read_text()),
                              delimiter='\t'))
    design = {'ID_PER', 'FAC_SEL', 'DOMINIO', 'EST_DIS', 'UPM_DIS'}
    contact_names = [f'AP5_16_{k}' for k in range(1, 11)]
    with zipfile.ZipFile(RAW / 'encuci2020_bd_dbf/BD_ENCUCI2020_dbf.zip') as z:
        members = [dict(entrada=i.filename, bytes=i.file_size,
                        sha256=sha(z.read(i))) for i in z.infolist()]
        a, ah = dbf(z.read('ENCUCI_2020_SEC_4_5.dbf'), design |
                    set(contact_names) | {'AP4_3_2', 'AP5_17', 'AP5_18'})
        b, bh = dbf(z.read('ENCUCI_2020_SEC_6_7_8.dbf'), design | {'AP7_3_5'})
    index = {r['ID_PER']: r for r in b}
    assert len(index) == len(b) and len({r['ID_PER'] for r in a}) == len(a)
    assert set(index) == {r['ID_PER'] for r in a}
    assert all(r['ID_PER'] for r in a)
    b = [index[r['ID_PER']] for r in a]
    assert all(x[k] == y[k] for x, y in zip(a, b) for k in design)
    w = np.array([float(r['FAC_SEL']) for r in a])
    assert np.all(np.isfinite(w) & (w > 0)), 'FAC_SEL inválido'
    assert all(r['EST_DIS'] and r['UPM_DIS'] for r in a)
    contact = np.array([any(integer(r[k]) == 1 for k in contact_names) for r in a])
    solic = np.array([integer(r['AP5_17']) for r in a])
    entrega = np.array([integer(r['AP5_18']) for r in a])
    agr = np.array([integer(r['AP4_3_2']) for r in a])
    protest = np.array([integer(r['AP7_3_5']) for r in b])
    dom = np.array([r['DOMINIO'] for r in a])
    ua = contact & np.isin(solic, [1, 2]) & np.isin(entrega, [1, 2])
    ub = np.isin(agr, [1, 2]) & np.isin(protest, [1, 2]) & np.isin(dom, ['U', 'C', 'R'])
    # Marco completo de personas, antes de excluir respuestas o formar dominios.
    pairs = sorted({(r['EST_DIS'], r['UPM_DIS']) for r in a})
    pair_index = {p: i for i, p in enumerate(pairs)}
    ix = np.array([pair_index[(r['EST_DIS'], r['UPM_DIS'])] for r in a])
    strata = sorted({p[0] for p in pairs})
    rng = np.random.Generator(np.random.PCG64(SEED))
    multiplicity = np.zeros((B, len(pairs)), dtype=np.int32)
    singletons = []
    for s in strata:
        cols = np.array([i for i, p in enumerate(pairs) if p[0] == s])
        m = len(cols)
        if m == 1:
            singletons.append(s)
        draws = rng.integers(0, m, size=(B, m))
        counts = np.bincount((draws + np.arange(B)[:, None] * m).ravel(),
                             minlength=B * m).reshape(B, m)
        multiplicity[:, cols] = counts
        assert np.all(counts.sum(axis=1) == m)
    ic_method = ('IC-CON-ESTRATOS-DE-UPM-UNICA' if singletons
                 else 'BOOTSTRAP-UPM-DENTRO-ESTRATO')

    def estimate(cell, mask, outcome, role):
        numerator = np.bincount(ix, weights=w * mask * outcome, minlength=len(pairs))
        denominator = np.bincount(ix, weights=w * mask, minlength=len(pairs))
        den_reps = multiplicity @ denominator
        assert np.all(den_reps > 0)
        reps = (multiplicity @ numerator) / den_reps
        lo, hi = np.percentile(reps, [2.5, 97.5], method='linear')
        p = numerator.sum() / denominator.sum()
        assert 0 <= lo <= hi <= 1 and 0 <= p <= 1
        return dict(celda=cell, papel=role, estimacion=float(p), ic95_inf=float(lo),
                    ic95_sup=float(hi), n=int(mask.sum()),
                    numerador_ponderado=float(numerator.sum()),
                    denominador_ponderado=float(denominator.sum()),
                    metodo_ic=ic_method)

    cells = []
    for name, outcome in [('CUALQUIERA', (solic == 1) | (entrega == 1)),
                          ('SOLICITUD', solic == 1), ('ENTREGA', entrega == 1),
                          ('AMBAS', (solic == 1) & (entrega == 1))]:
        cells.append(estimate('A-P-' + name, ua, outcome, 'METODO'))
    # Celdas del método: no constituyen una asignación a identidades contradictorias.
    for alternative in [False, True]:
        for env, codes in [('URB', ['U'] if alternative else ['U', 'C']),
                           ('RUR', ['R', 'C'] if alternative else ['R'])]:
            for label, value in [('AGR', 1), ('SIN-AGR', 2)]:
                name = ('SENS-' if alternative else '') + f'B-P-{env}-{label}'
                cells.append(estimate(name, ub & np.isin(dom, codes) & (agr == value),
                                      protest == 1,
                                      'SENSIBILIDAD-NO-ADOPTABLE' if alternative else 'METODO'))
    write_tsv('celdas_metodo.tsv', cells, list(cells[0]))
    by_cell = {r['celda']: r for r in cells}
    results = []
    for key in keys:
        row = dict(key)
        row.update(estado='', motivo='', celda_reconstruida='', estimacion='',
                   ic95_inf='', ic95_sup='', n='', numerador_ponderado='',
                   denominador_ponderado='', metodo_ic='')
        identity = key['result_id']
        if identity == 'RESULT-ENCUCI-B-P-RUR-AGR':
            row.update(estado='NO-RECALCULABLE-DESDE-SPEC', motivo=
                       'Identidad contradictoria: llave/result_id y conducta indican rural; '
                       'segmento indica agravio_urbano; celda vacía y sin regla de precedencia. '
                       'No se asigna ninguna celda a esta identidad.')
        elif identity in {'RESULT-ENCUCI-A-P-CUALQUIERA', 'RESULT-ENCUCI-B-P-URB-AGR'}:
            cell = identity.removeprefix('RESULT-ENCUCI-')
            value = by_cell[cell]
            row.update(estado='RECONSTRUIDO', celda_reconstruida=cell)
            for field in ['estimacion', 'ic95_inf', 'ic95_sup', 'n',
                          'numerador_ponderado', 'denominador_ponderado', 'metodo_ic']:
                row[field] = value[field]
        else:
            row.update(estado='NO-RECALCULABLE-DESDE-SPEC', motivo='Identidad sin correspondencia implementada.')
        results.append(row)
    write_tsv('reconstruccion.tsv', results, list(results[0]))
    counts = lambda rows, field: dict(sorted(Counter(r[field] or '<BLANCO>' for r in rows).items()))
    save_json('auditoria.json', dict(
        filas_a=len(a), filas_b=len(b), union='ID_PER uno a uno; conjuntos y diseño idénticos',
        cabeceras={'SEC_4_5': ah, 'SEC_6_7_8': bh},
        G_3=dict(contacto_literal_1=sum(any(r[k] == '1' for k in contact_names) for r in a),
                 contacto_normalizado_1=int(contact.sum()),
                 agravio_literal_1=sum(r['AP4_3_2'] == '1' for r in a),
                 agravio_normalizado_1=int((agr == 1).sum())),
        codigos={f: counts(a, f) for f in contact_names + ['AP5_17', 'AP5_18', 'AP4_3_2']} |
                {'AP7_3_5': counts(b, 'AP7_3_5')},
        exclusiones=dict(A_sin_contacto_declarado=int((~contact).sum()),
                         A_contacto_respuestas_invalidas=int((contact & ~ua).sum()),
                         A_total=int((~ua).sum()), B_total=int((~ub).sum())),
        diseno=dict(estratos=len(strata), upm_estrato=len(pairs),
                    estratos_upm_unica=singletons, METODO_IC=ic_method),
        replicas=B, semilla=SEED, generador='numpy.PCG64',
        orden='EST_DIS y UPM_DIS lexicográfico; por estrato matriz (2000, n_UPM), rng.integers',
        percentiles='numpy.percentile method=linear; 2.5 y 97.5',
        marco='Todas las personas SEC_4_5; dominios fuera de celda aportan cero; mismos sorteos para todas las celdas',
        entorno=dict(python=platform.python_version(), numpy=np.__version__), tolerancia=tolerance))
    save_json('inventario.json', dict(archivos=inventory, entradas_zip=members))
    save_json('recibo.json', dict(paquete=manifest['paquete'], version_entrada=manifest['version_entrada'],
        manifiesto_sha256=sha(manifest_data), fuentes=['/entrada', '/raw'],
        resultados_esperados_consultados=False, revelacion_solicitada=False,
        estados=dict(Counter(r['estado'] for r in results)),
        congelacion='Código y números incluidos en el commit local; identificar con git rev-parse HEAD.'))


if __name__ == '__main__':
    main()
