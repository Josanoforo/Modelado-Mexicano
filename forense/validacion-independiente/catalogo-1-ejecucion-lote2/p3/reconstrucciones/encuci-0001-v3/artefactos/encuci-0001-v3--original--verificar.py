#!/usr/bin/env python3
"""Comprobaciones internas, sin valores de referencia ni resultados esperados."""
import csv
import json
import os
import subprocess
import sys
import zipfile
from decimal import Decimal

from reconstruir import ROOT, RAW, dbf, sha


def main():
    outputs = ['reconstruccion.tsv', 'celdas_metodo.tsv', 'auditoria.json',
               'inventario.json', 'recibo.json']
    before = {f: sha((ROOT / f).read_bytes()) for f in outputs}
    subprocess.run([sys.executable, str(ROOT / 'reconstruir.py')], check=True,
                   env=dict(os.environ, OPENBLAS_NUM_THREADS='1'))
    after = {f: sha((ROOT / f).read_bytes()) for f in outputs}
    assert before == after, 'La repetición debe ser idéntica byte a byte'
    names = [f'AP5_16_{i}' for i in range(1, 11)]
    with zipfile.ZipFile(RAW / 'encuci2020_bd_dbf/BD_ENCUCI2020_dbf.zip') as z:
        a, _ = dbf(z.read('ENCUCI_2020_SEC_4_5.dbf'),
                   set(names) | {'ID_PER', 'FAC_SEL', 'AP5_17', 'AP5_18', 'AP4_3_2', 'DOMINIO'})
        b, _ = dbf(z.read('ENCUCI_2020_SEC_6_7_8.dbf'), {'ID_PER', 'AP7_3_5'})
    protest = {r['ID_PER']: r['AP7_3_5'] for r in b}
    # Suma directa con Decimal, independiente de matrices, NumPy y agrupación por UPM.
    totals = {k: [Decimal(0), Decimal(0), 0] for k in ['A-P-CUALQUIERA', 'B-P-URB-AGR']}
    for r in a:
        contact = any(r[k] and Decimal(r[k]) == 1 for k in names)
        if contact and r['AP5_17'] in ('1', '2') and r['AP5_18'] in ('1', '2'):
            t = totals['A-P-CUALQUIERA']
            t[1] += Decimal(r['FAC_SEL'])
            t[0] += Decimal(r['FAC_SEL']) * (r['AP5_17'] == '1' or r['AP5_18'] == '1')
            t[2] += 1
        d = protest[r['ID_PER']]
        if r['AP4_3_2'] and Decimal(r['AP4_3_2']) == 1 and r['DOMINIO'] in ('U', 'C') and d in ('1', '2'):
            t = totals['B-P-URB-AGR']
            t[1] += Decimal(r['FAC_SEL'])
            t[0] += Decimal(r['FAC_SEL']) * (d == '1')
            t[2] += 1
    with (ROOT / 'reconstruccion.tsv').open() as f:
        results = list(csv.DictReader(f, delimiter='\t'))
    checks = {}
    for r in results:
        if r['estado'] == 'RECONSTRUIDO':
            num, den, n = totals[r['celda_reconstruida']]
            error = abs(Decimal(r['estimacion']) - num / den)
            assert error <= Decimal('1e-10')
            assert Decimal(r['numerador_ponderado']) == num
            assert Decimal(r['denominador_ponderado']) == den
            assert int(r['n']) == n
            checks[r['llave']] = str(error)
        else:
            assert r['motivo'] and all(not r[k] for k in
                ['estimacion', 'ic95_inf', 'ic95_sup', 'n', 'numerador_ponderado', 'denominador_ponderado'])
    report = dict(resultado='PASS', repeticion_byte_a_byte=True,
                  sumas_directas_decimal=True, errores_absolutos=checks,
                  sin_cifras_para_identidad_ambigua=True, hashes_salidas=after,
                  comparacion_con_resultados_esperados=False)
    (ROOT / 'validacion.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print('PASS: repetibilidad, suma directa Decimal, estados sin cifras.')


if __name__ == '__main__':
    main()
