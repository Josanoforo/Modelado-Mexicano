#!/usr/bin/env python3
"""Deriva hallazgos por identidad tras congelación y comparación."""
from collections import Counter
import csv
import io
import json
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'forense/validacion-independiente/catalogo-1-ejecucion-lote1'
CAT = ROOT / 'forense/validacion-independiente/catalogo-1'


def efectos():
    with (BASE / 'tabla-estimadores.tsv').open() as stream:
        final = {row['llave']: row for row in csv.DictReader(stream, delimiter='\t')}
    identities = {}
    lots = {row['paquete']: row for row in json.loads((CAT / 'lotes.json').read_text())}
    effects, gaps = [], []
    for entry in json.loads((BASE / 'entregas.json').read_text()):
        package = entry['paquete']
        with tarfile.open(CAT / 'paquetes' / package / lots[package]['archivo'], 'r:gz') as tar:
            identities.update({row['llave']: row for row in csv.DictReader(io.StringIO(tar.extractfile('estimandos.tsv').read().decode()), delimiter='\t')})
        for row in json.loads((BASE / entry['comparacion']).read_text())['resultados']:
            key = row['llave']
            state = final[key]['estado']
            if state == 'NO-RECALCULABLE-DESDE-SPEC':
                gaps.append({'llave': key, 'paquete': package, 'estado': state, 'motivo': final[key]['motivo'],
                             'accion_propuesta': 'Spec sucesora explícita por identidad; nuevo intento, sin alterar el primer resultado'})
            if state != 'DISCREPA':
                continue
            identity = identities[key]
            fields = row.get('campos', {})
            component = 'publicabilidad' if not fields else 'punto' if not fields['punto']['dentro'] else 'IC'
            cause = 'Umbrales de publicación aplicados; reconstrucción ejecutada, no D-15' if component == 'publicabilidad' else 'Realización aleatoria y/o marco UPM: no se acreditó equivalencia inferencial'
            if component == 'punto' and '2011' in package:
                behavior = identity['conducta']
                if identity['eje'] == 'edad' and identity['segmento'] == '60+':
                    cause = 'edad_60+: filtros de edad distintos; adjudicar código con FD de esta ola'
                elif behavior == 'externo_denuncia_ultima_visita':
                    cause = 'denuncia_externa: columnas 1/5 vs 1–4 y elegibilidad distintas'
                elif behavior.startswith('externo_'):
                    cause = 'ambitos_externos: desconocidos vs negativos y denominador conocido'
                elif behavior.startswith('pareja_institucion_'):
                    cause = 'instituciones: solicitantes vs afectadas, cambia estimando'
                elif behavior.startswith('permiso_'):
                    cause = 'permisos: filtro CP4_1 distinto'
                elif behavior.startswith('pareja_') and behavior.endswith('desde_octubre_2010'):
                    cause = 'pareja_reciente: condicionamiento por vida conocida distinto'
                else:
                    raise ValueError('Discrepancia de punto 2011 sin investigación: ' + key)
            elif component == 'punto':
                assert 'nofisica-bc' in package
                cause = 'edad_60+: inclusión de EDAD 98/99 no especificada en productor; FD 2021'
            effects.append({'llave': key, 'paquete': package, 'conducta': identity['conducta'],
                            'eje': identity['eje'], 'segmento': identity['segmento'], 'componente': component,
                            'delta_punto': fields.get('punto', {}).get('delta', ''),
                            'delta_ic95_inf': fields.get('ic95_inf', {}).get('delta', ''),
                            'delta_ic95_sup': fields.get('ic95_sup', {}).get('delta', ''),
                            'causa_o_hipotesis': cause, 'conclusion': 'Efecto sobre cifra/incertidumbre/alcance; cambio de conclusión o regla no probado'})
    for filename, rows in [('efectos-discrepancias.tsv', effects), ('hallazgos-spec.tsv', gaps)]:
        with (BASE / filename).open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter='\t')
            writer.writeheader()
            writer.writerows(rows)
    groups = Counter(row['causa_o_hipotesis'] for row in effects if row['componente'] == 'punto')
    report = {'efectos': len(effects), 'hallazgos_spec': len(gaps), 'puntos_por_causa': dict(groups),
              'max_delta_absoluta_punto': max(abs(row['delta_punto']) for row in effects if row['componente'] == 'punto')}
    (BASE / 'resumen-efectos.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    efectos()
