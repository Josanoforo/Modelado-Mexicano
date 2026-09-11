#!/usr/bin/env python3
"""Sondas de revisión sobre el repo indicado. Sólo escribe fixtures temporales.
Uso: python3 PRUEBAS-CANDADOS-GEN2.py /ruta/al/repo
Salida JSON descriptiva; no afirma que un comportamiento observado sea correcto.
No ejecuta modelos, red ni microdatos. No modifica el repositorio.
"""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(sys.argv[1]).resolve()


def carga(rel, nombre):
    s = importlib.util.spec_from_file_location(nombre, ROOT / rel)
    m = importlib.util.module_from_spec(s)
    sys.modules[nombre] = m
    s.loader.exec_module(m)
    return m


T = carga('tests/test_corrida0.py', 'sonda_fixture_c0')
C = T.C
out = {'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()}

# Control y variantes de una misma ruta; sólo ejercita la clasificación.
out['rutas'] = {}
for ruta in ['milpa/tramite.yaml', './milpa/tramite.yaml', 'milpa/../milpa/tramite.yaml',
             'forense/prereg-duelo-v2/snapshot-M-triada-v1_0.json',
             'forense/prereg-duelo-v2/corridas-R/correr-R.py']:
    spec = {'etiquetas': {'generacion': 'GEN2', 'cuenta_gen2': 'SI'},
            'inputs': [{'id': 'X', 'origen': 'repo', 'ruta': ruta}]}
    out['rutas'][ruta] = C._cuenta_gen2_resuelto('CALC-SONDA', spec, {})

# Cadena cuyo padre se declara LEGACY, pero no cae en el detector por ruta.
of = [{'calc_id': 'CALC-PADRE', 'envuelto_legacy': 'NO', 'generacion': 'LEGACY-GEN1',
       'spec': {'etiquetas': {'generacion': 'LEGACY-GEN1'}, 'inputs': []}},
      {'calc_id': 'CALC-HIJO', 'envuelto_legacy': 'NO', 'generacion': 'GEN2',
       'spec': {'inputs': [{'ruta': 'data/corrida0/CALC-PADRE/resultados.json'}]}}]
C._propaga_envuelto(of)
out['herencia_padre_declarado_legacy'] = of[1]['envuelto_legacy']

# Fixture con sello real y salida legacy envuelta etiquetada GEN2/cuenta=NO.
# Esta sonda prueba registro y T35, no un preflight/medición científica real.
rid = 'RESULT-SONDA-WRAPPER'
calcs = [{'calc_id': 'CALC-SONDA-WRAPPER', 'valores': {rid: .5},
          'etiquetas': {'generacion': 'GEN2', 'cuenta_gen2': 'NO'}}]
tramite = {'reglas': [{'id': 'r.sonda', 'entonces': [{'conducta': 'c1', 'p': .5,
              'corrida0_generacion': 'GEN2', 'corrida0_resultado_id': rid}]}]}
with T._arbol_registro(calcs=calcs, tramite=tramite) as tmp:
    d = tmp / 'CALC-SONDA-WRAPPER'
    spec = yaml.safe_load((d / 'spec.yaml').read_text())
    spec['inputs'] = [{'id': 'IN-LEGACY', 'origen': 'repo', 'ruta': 'milpa/tramite.yaml',
                       'sha256': C._sha256_archivo(ROOT / 'milpa/tramite.yaml')}]
    (d / 'spec.yaml').write_text(yaml.safe_dump(spec))
    ej = json.loads((d / 'ejecucion.json').read_text())
    ej['spec_yaml_sha256'] = C._sha256_archivo(d / 'spec.yaml')
    ej['input_ids'] = ['IN-LEGACY']
    ej['input_sha256'] = {'IN-LEGACY': spec['inputs'][0]['sha256']}
    C._escribe_json(d / 'ejecucion.json', ej)
    C._escribe_json(d / 'sello.json', C._construye_sello(d, spec))
    subprocess.run([sys.executable, str(C.SELLA_PY), str(d / 'sello.json')], check=True, capture_output=True)
    consumidor = f'{C._rel(C.TRAMITE)}:r.sonda:c1'
    C._escribe(C.DEMANDA_RESULTADOS, C.COLS_RESULTADOS,
              [T._fila_demanda('RES-SONDA', consumidor, 'CORR-SONDA')])
    C._escribe(C.DEMANDA_CORRIDAS, C.COLS_CORRIDAS,
              [T._fila_corrida('CORR-SONDA', ['RES-SONDA'])])
    chk = T._carga_check()
    chk.FAILS.clear(); chk.WARNS.clear(); chk.SENAL.clear()
    chk.t35_repro(modulo=C)
    vista = C._filas_registro(False)
    fila = next(x for x in vista['corridas'] if x['spec_id'] == 'CALC-SONDA-WRAPPER')
    out['adopcion_wrapper'] = {'envuelto_legacy': fila['envuelto_legacy'],
                              'generacion': fila['generacion'], 'cuenta_gen2': fila['cuenta_gen2'],
                              't35_fallos': chk.FAILS}

F = carga('tools/calcula_f5_completa.py', 'sonda_calcula_f5')
base, _ = F.calcular()
snap = json.loads(F.SNAPSHOT_M.read_text())
with tempfile.TemporaryDirectory(prefix='candados-f5-') as tmp:
    ruta = Path(tmp) / 'snapshot.json'
    for campo, valor in [('estado_firewall', 'CONTAMINADO-POR-OBJETIVO'),
                         ('identidad_confirmada', False)]:
        alterado = copy.deepcopy(snap)
        celda = next(x for x in alterado['celdas'] if x['id_celda'] == 'CIV-M-01')
        celda[campo] = valor
        ruta.write_text(json.dumps(alterado))
        F.SNAPSHOT_M = ruta
        r, _ = F.calcular()
        out['f5_' + campo] = {'celda_sigue_en_u3': 'CIV-M-01' in r['u3_ids'],
                              'u3_n': r['u3_n'], 'mae_igual': r['mae_pp'] == base['mae_pp'],
                              'veredicto': r['veredicto_global']}

# Medidor vigente: comprueba qué lecturas hace pese a recibir cero inputs.
abiertas = set()
activo = False
def auditor(event, args):
    if activo and event == 'open' and args and isinstance(args[0], (str, bytes)):
        try:
            p = Path(args[0]).resolve()
            abiertas.add(str(p.relative_to(ROOT)))
        except (ValueError, TypeError):
            pass
sys.addaudithook(auditor)
M = carga('data/corrida0/CALC-TRIADA-0002/medidor.py', 'sonda_medidor_f5')
spec = yaml.safe_load((ROOT / 'data/corrida0/CALC-TRIADA-0002/spec.yaml').read_text())
activo = True
vals = M.medir({}, C.contrato_ejecutable(spec))
activo = False
declarados = {x.get('ruta') for x in spec['inputs']}
extra_json = sorted(p for p in abiertas if p.endswith('.json') and p not in declarados)
out['f5_inputs'] = {'inputs_entregados': 0, 'resultados_emitidos': len(vals),
                   'json_extra_no_declarados': len(extra_json),
                   'capturas_extra': sum('/corridas-L-completa-v1_0/' in p for p in extra_json),
                   'r_extra': sum('/CALC-R-' in p and p.endswith('/resultados.json') for p in extra_json),
                   'muestra': extra_json[:4]}

vista = C._filas_registro(False)
out['usos_actuales'] = dict(Counter(u['generacion_leida'] for u in vista['usos'] if u['activo'] == 'SI'))
out['tríadas_actuales'] = [{k: r[k] for k in ['spec_id', 'generacion', 'cuenta_gen2', 'envuelto_legacy']}
                         for r in vista['corridas'] if r['spec_id'] in ['CALC-TRIADA-0001','CALC-TRIADA-0002']]
out['arbitros_clasificados_por_ruta_codigo'] = [r['spec_id'] for r in vista['corridas']
    if r.get('envuelto_legacy') == 'SI' and r['spec_id'].startswith('CALC-R-')
    and 'IN-CODIGO-CORRER-R=' in r.get('motivo_cuenta_gen2','')]
print(json.dumps(out, indent=2, ensure_ascii=False))
