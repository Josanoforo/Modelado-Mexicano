"""Verificación independiente del punto y reproducción de salidas."""
import csv
import io
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
with zipfile.ZipFile('/raw/envipe2025_csv/envipe2025_csv.zip') as z:
    def rows(t):
        name = f'{t}_envipe2025/conjunto_de_datos/conjunto_de_datos_{t}_envipe2025.csv'
        return csv.DictReader(io.TextIOWrapper(z.open(name), encoding='utf-8-sig'))
    persons = {}
    crimes = 0
    for r in rows('tmod_vic'):
        if 5 <= int(r['BPCOD']) <= 15 and r['BP1_20'] == '2' and r['BP1_23'] in {'01','02','03','04','05','06','07','08'}:
            crimes += 1
            key = r['ID_PER']
            persons[key] = persons.get(key, False) or r['BP1_23'] in {'01','02','06','08'}
    num = den = matched = 0
    for r in rows('tper_vic2'):
        if r['ID_PER'] in persons:
            matched += 1
            w = int(r['FAC_ELE'])
            den += w
            num += w * persons[r['ID_PER']]
    assert matched == len(persons)
result = next(csv.DictReader((ROOT / 'reconstruccion.tsv').open(), delimiter='\t'))
assert result['estado'] == 'RECONSTRUIDO'
assert int(result['numerador_ponderado']) == num
assert int(result['denominador_ponderado']) == den
assert float(result['estimacion']) == num / den
assert float(result['ic95_inferior']) <= num / den <= float(result['ic95_superior'])
with tempfile.TemporaryDirectory() as dest:
    subprocess.run([sys.executable, str(ROOT / 'reconstruir.py'), '--salida', dest], check=True)
    outputs = ['reconstruccion.tsv', 'recibo.json', 'auditoria.json', 'replicas.tsv', 'entradas_zip.json']
    for name in outputs:
        assert (ROOT / name).read_bytes() == (Path(dest) / name).read_bytes(), name
(ROOT / 'verificacion.json').write_text(json.dumps({
    'punto_independiente_biblioteca_estandar': True,
    'numerador': num, 'denominador': den, 'personas': matched, 'delitos': crimes,
    'reproduccion_byte_a_byte': outputs,
}, indent=2) + '\n')
print('Verificación independiente y reproducción: OK')
