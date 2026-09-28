#!/usr/bin/env python3
"""Contrato único de salida v3 y conversión conservadora de documentos v2.

No lee referencias ni compara cifras. El adaptador v2 permanece inalterado.
"""

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
V2_PATH = ROOT / 'tools/validacion/astra6_aislamiento_v2/adaptador.py'
_spec = importlib.util.spec_from_file_location('astra6_adaptador_v2', V2_PATH)
_v2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_v2)

STATES = frozenset({
    'RECONSTRUIDO', 'NO-EVALUADO', 'NO-RECALCULABLE-DESDE-SPEC',
    'BLOQUEADO-POR-ACCESO', 'DENOMINADOR-CERO', 'NO-ESTIMABLE',
})
IC_STATES = frozenset({'SIN-IC', 'CALCULADO', 'NO-IDENTIFICADA'})
NUMERIC = ('punto', 'ic95_inf', 'ic95_sup')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def validate(document):
    """Valida y normaliza solo alias; preserva lexemas y ausencia/null/número."""
    require(type(document) is dict and set(document) == {'version', 'identidad', 'filas'},
            'Documento v3: campos faltantes/extra')
    require(type(document['version']) is int and document['version'] == 3,
            'Version v3 invalida')
    identity = document['identidad']
    require(type(identity) is dict and set(identity) == {'paquete', 'version_entrada', 'sha256_entrada'},
            'Identidad v3 invalida')
    require(all(type(v) is str and v for v in identity.values()), 'Identidad vacia/invalida')
    import re
    require(bool(re.fullmatch('[0-9a-f]{64}', identity['sha256_entrada'])), 'SHA de entrada invalido')
    rows = document['filas']
    require(type(rows) is list and rows, 'Filas v3 invalidas')
    aliases = _v2.read_json(_v2.CONTRACT)['alias']
    allowed = {'llave', 'unidad', 'estado', 'estado_ic', 'motivo', 'motivo_ic'} | {
        alias for names in aliases.values() for alias in names
    }
    normalized, mappings, seen = [], [], set()
    for row in rows:
        require(type(row) is dict and {'llave', 'unidad', 'estado'} <= set(row) <= allowed,
                'Fila v3: campos faltantes/extra')
        require(all(type(row[k]) is str and row[k] for k in ('llave', 'unidad', 'estado')),
                'Llave/unidad/estado invalidos')
        require(row['llave'] not in seen, 'Llave repetida')
        seen.add(row['llave'])
        require(row['estado'] in STATES, 'Estado v3 invalido')
        for key in ('estado_ic', 'motivo', 'motivo_ic'):
            if key in row:
                require(type(row[key]) is str and bool(row[key]), key + ' invalido')
        if 'estado_ic' in row:
            require(row['estado_ic'] in IC_STATES, 'Estado IC v3 invalido')
        out = {k: v for k, v in row.items() if k in {
            'llave', 'unidad', 'estado', 'estado_ic', 'motivo', 'motivo_ic'
        }}
        mapping = {}
        for target, names in aliases.items():
            found = [name for name in names if name in row]
            require(len(found) <= 1, 'Colision ambigua: ' + target)
            source = found[0] if found else None
            mapping[target] = source
            if source:
                value = row[source]
                if value is not None:
                    _v2.number(value)
                out[target] = value
        point = out.get('punto')
        ic = out.get('estado_ic')
        inf, sup = out.get('ic95_inf'), out.get('ic95_sup')
        if row['estado'] == 'RECONSTRUIDO':
            require('punto' in out and point is not None, 'RECONSTRUIDO exige punto numerico')
            require(ic in IC_STATES, 'RECONSTRUIDO exige estado_ic explicito')
            if ic == 'CALCULADO':
                require(inf is not None and sup is not None and
                        'ic95_inf' in out and 'ic95_sup' in out, 'IC calculado incompleto')
                require(_v2.number(inf) <= _v2.number(sup), 'IC invertido')
            else:
                require('ic95_inf' not in out and 'ic95_sup' not in out,
                        'IC no calculado exige extremos ausentes')
                if ic == 'NO-IDENTIFICADA':
                    require('motivo_ic' in out, 'Incertidumbre no identificada exige motivo_ic')
        else:
            require(not any(field in out for field in NUMERIC),
                    'Estado sin estimacion exige numeros ausentes, no null')
            require(ic in (None, 'SIN-IC'), 'Estado sin estimacion no admite IC')
            if row['estado'] in {'NO-RECALCULABLE-DESDE-SPEC', 'BLOQUEADO-POR-ACCESO',
                                 'DENOMINADOR-CERO', 'NO-ESTIMABLE'}:
                require('motivo' in out, 'Estado sin estimacion exige motivo')
        normalized.append(out)
        mappings.append({'llave': row['llave'], 'campos': mapping})
    return {'version': 3, 'identidad': identity.copy(), 'filas': normalized,
            'mapa_campos': mappings}


def from_v2(document):
    """Convierte solo estados cuya semántica v2 está declarada sin ambigüedad."""
    old = _v2.normalize(document)
    rows = []
    for row in old['filas']:
        state = row['estado']
        if state == 'RECONSTRUIDO':
            require(row.get('estado_ic') in {'SIN-IC', 'CALCULADO'},
                    'v2 reconstruido sin estado_ic explicito: ambigüedad')
            if row['estado_ic'] == 'SIN-IC':
                require('ic95_inf' not in row and 'ic95_sup' not in row,
                        'v2 SIN-IC ambiguo')
            else:
                require(row.get('ic95_inf') is not None and row.get('ic95_sup') is not None,
                        'v2 IC calculado ambiguo')
        else:
            require(not any(field in row for field in NUMERIC),
                    'v2 estado sin estimacion con campo numerico ambiguo')
            require(row.get('estado_ic') in (None, 'SIN-IC'), 'v2 estado IC ambiguo')
            if state in {'NO-RECALCULABLE-DESDE-SPEC', 'BLOQUEADO-POR-ACCESO'}:
                require('motivo' in row, 'v2 estado sin motivo ambiguo')
        rows.append(row)
    converted = {'version': 3, 'identidad': old['identidad'], 'filas': rows}
    result = validate(converted)
    result['mapa_campos'] = old['mapa_campos']
    return result
