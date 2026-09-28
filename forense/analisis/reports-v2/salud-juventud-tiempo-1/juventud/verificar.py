#!/usr/bin/env python3
"""Control dirigido de cobertura y afirmaciones materiales de juventud."""
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
REPORT = ROOT / 'corpus/reports-v2/Psicología_de_la_Juventud_Mexicana_Contemporánea__Gen_Z_y_Millennials_Jóvenes_como_Cohorte_Divergente.md'
MAP = ROOT / 'forense/analisis/dominios/lotes/juventud-filas-v1_0.tsv'

def read(path):
    with path.open(newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))

def main():
    tab = read(HERE / 'tabla.tsv')
    ids = [r['id'] for r in tab]
    originals = [r['id_afirmacion'] for r in read(MAP)]
    assert len(ids) == len(set(ids)), 'identificadores duplicados'
    assert set(originals) <= set(ids), 'falta afirmación del mapa'
    assert len(tab) == 37, 'cobertura esperada: 32 mapa + 5 extra'
    assert all(r['dictamen_v2'] in {'CONFIRMA','MATIZA','ROMPE','SIN-CIFRA'} for r in tab)
    assert all(r['razon_especifica'] and r['falsador_o_siguiente_prueba'] for r in tab)
    report = REPORT.read_text()
    for section in ('Resumen ejecutivo','Marco y mapa','Patrones principales','Causas, estructura','Segmentación explícita','Comparación internacional','Implicaciones y mitos','Síntesis y reglas','Auditoría de rigor extremo'):
        assert section in report, f'falta sección: {section}'
    # Las cantidades de EDER/ENADID que el encargo veta no se filtran al texto.
    for forbidden in ('16.9%', '31.1%', '70.6', '45.2', '2.07', '1.60'):
        assert forbidden not in report, f'cifra reservada en report: {forbidden}'
        assert forbidden not in (HERE / 'tabla.tsv').read_text(), f'cifra reservada en tabla: {forbidden}'
    assert 'edad = periodo' in report and 'no identifica' in report
    assert 'RESULT-ENDUTIH-PISOS-2024-TABLA#46' in report
    result_file = ROOT / 'data/corrida0/CALC-ENDUTIH-PISOS-2024-0001/resultados.json'
    sha = hashlib.sha256(result_file.read_bytes()).hexdigest()
    assert sha == '4c0a3b05b6ecef3e9d7e760163cc6a6691ceaf384fa522e620bbe9b663088c25'
    cells = json.loads(json.loads(result_file.read_text())['resultados']['RESULT-ENDUTIH-PISOS-2024-TABLA'])['celdas']
    for idx, domain, point, n in ((42,'TLOC_1',0.8890201598934077,27695),(45,'TLOC_4',0.699642347777261,12823),(46,'TOTAL',0.8312233799456584,58080)):
        cell = cells[idx]
        assert (cell['medida'],cell['dominio'],cell['n']) == ('internet',domain,n)
        assert abs(cell['punto']-point) < 1e-12
        assert f'RESULT-ENDUTIH-PISOS-2024-TABLA#{idx}' in report
    print(f'OK: {len(originals)} afirmaciones mapa, {len(tab)-len(originals)} adicionales; Bloque B y vetos dirigidos')

if __name__ == '__main__':
    main()
