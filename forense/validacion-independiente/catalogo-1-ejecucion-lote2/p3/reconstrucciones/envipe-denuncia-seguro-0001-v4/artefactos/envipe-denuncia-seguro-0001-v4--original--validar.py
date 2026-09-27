#!/usr/bin/env python3
"""Verifica conteos por una ruta independiente y repetibilidad de artefactos."""
import csv
from decimal import Decimal
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import zipfile

base = Path(__file__).resolve().parent
raw = Path(sys.argv[1]) if len(sys.argv)>1 else Path('/raw')
with zipfile.ZipFile(raw/'envipe2025_csv/envipe2025_csv.zip') as z:
    with z.open('tmod_vic_envipe2025/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2025.csv') as f:
        datos = list(csv.DictReader(io.TextIOWrapper(f, encoding='utf-8-sig', newline='')))
with (base/'reconstruccion.tsv').open() as f:
    salida = list(csv.DictReader(f,delimiter='\t'))
verificados=[]
for resultado, cobertura, desenlace in zip(salida, ['1','1','2','2'], ['1','2','1','2'], strict=True):
    seleccion = [r for r in datos if r['BPCOD']=='01' and r['BP2_1']==cobertura]
    den = sum(Decimal(r['FAC_DEL']) for r in seleccion)
    num = sum(Decimal(r['FAC_DEL']) for r in seleccion if r['BP1_20']==desenlace)
    assert resultado['estado']=='RECONSTRUIDO'
    assert Decimal(resultado['numerador'])==num
    assert Decimal(resultado['denominador'])==den
    assert int(resultado['n'])==len(seleccion)
    assert abs(Decimal(resultado['estimacion'])-num/den)<Decimal('1e-10')
    verificados.append(resultado['llave'])
archivos=['reconstruccion.tsv','replicas.tsv','diagnostico.json','recibo.json',
          'inventario_insumos.json','inventario_zip.json']
antes={n:hashlib.sha256((base/n).read_bytes()).hexdigest() for n in archivos}
subprocess.run([sys.executable,str(base/'reconstruir.py'),str(raw)],check=True)
despues={n:hashlib.sha256((base/n).read_bytes()).hexdigest() for n in archivos}
assert antes==despues
with (base/'replicas.tsv').open() as f:
    replicas=list(csv.DictReader(f,delimiter='\t'))
assert len(replicas)==2000
for r in replicas:
    for llave in verificados:
        assert 0<=float(r[llave])<=1
(base/'validacion.json').write_text(json.dumps(dict(
    conteos_decimal_verificados=verificados, repeticion_identica=True,
    hashes_salidas=antes, replicas_en_rango=2000,
    comparacion_con_resultados_esperados=False),ensure_ascii=False,indent=2)+'\n')
print('Conteos independientes, límites y repetibilidad: OK')
