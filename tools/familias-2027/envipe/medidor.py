"""Dos estimandos fijos; lector de columnas blancas, réplica común de diseño.

No importa productores históricos. No permite abrir olas futuras en este acto.
El agrupador único es el conglomerado de diseño (EST_DIS, UPM_DIS).
"""
import csv
import hashlib
import io
import zipfile
from pathlib import Path

import numpy as np

COLUMNAS = {
    'modulo': ('ID_PER', 'ID_DEL', 'BPCOD', 'BP1_20', 'BP1_23',
               'FAC_DEL', 'EST_DIS', 'UPM_DIS'),
    'persona': ('ID_PER', 'FAC_ELE', 'EST_DIS', 'UPM_DIS'),
}
FAMILIAS = ('DENUNCIA_U4', 'EVASION_NORMA')


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def codigo(value):
    try:
        return int(value.strip())
    except (ValueError, AttributeError):
        return None


def peso(value):
    try:
        x = float(value)
        return x if np.isfinite(x) and x > 0 else None
    except (ValueError, TypeError):
        return None


def dictamen(lo, hi, comparable=True, estimable=True):
    if not comparable:
        return 'NO-COMPARABLE'
    if not estimable or not np.isfinite([lo, hi]).all() or lo > hi:
        return 'NO-ESTIMABLE'
    if -.02 <= lo and hi <= .02:
        return 'COMPATIBLE-CON-TOLERANCIA'
    if hi < -.02 or lo > .02:
        return 'DESVÍO-MATERIAL'
    return 'INDETERMINADO'


def leer(path, contrato, modo='historico'):
    if modo not in ('historico', 'sintetico'):
        raise ValueError('RESERVADA: apertura requiere acto COMMIT-3 autorizado')
    if contrato['agrupacion'] != ['EST_DIS', 'UPM_DIS']:
        raise ValueError('una sola agrupacion de diseño autorizada')
    if contrato['columnas'] != {k: list(v) for k, v in COLUMNAS.items()}:
        raise ValueError('lista blanca de columnas alterada')
    if modo == 'historico' and sha(path) != contrato['insumo']['sha256']:
        raise ValueError('identidad de ola histórica incorrecta')
    tablas = {}
    with zipfile.ZipFile(path) as z:
        for tabla, cols in COLUMNAS.items():
            member = contrato['tablas'][tabla]
            # Abre exclusivamente el miembro congelado, no extrae el ZIP.
            with z.open(member) as raw:
                reader = csv.reader(io.TextIOWrapper(raw, encoding='utf-8-sig', newline=''))
                header = [c.strip().upper() for c in next(reader)]
                if len(set(header)) != len(header) or not set(cols) <= set(header):
                    raise ValueError('esquema ausente o ambiguo: ' + tabla)
                indices = [header.index(c) for c in cols]
                rows = []
                for row in reader:
                    if len(row) != len(header):
                        raise ValueError('fila de ancho incorrecto')
                    rows.append(dict(zip(cols, (row[i].strip() for i in indices))))
                tablas[tabla] = rows
    return tablas


def construir(tablas):
    personas = {}
    marco = set()
    for p in tablas['persona']:
        pid = p['ID_PER']
        if not pid or pid in personas:
            raise ValueError('llave persona ausente/duplicada')
        if not p['EST_DIS'] or not p['UPM_DIS'] or peso(p['FAC_ELE']) is None:
            raise ValueError('diseño o FAC_ELE inválido')
        personas[pid] = p
        marco.add((p['EST_DIS'], p['UPM_DIS']))
    delitos, u1, c2, potencial, excluidas = [], [], {}, set(), []
    ids = set()
    for f in tablas['modulo']:
        if not f['ID_DEL'] or f['ID_DEL'] in ids:
            raise ValueError('llave delito ausente/duplicada')
        ids.add(f['ID_DEL'])
        pid = f['ID_PER']
        if pid not in personas:
            raise ValueError('delito sin persona: unión inválida')
        p = personas[pid]
        if (f['EST_DIS'], f['UPM_DIS']) != (p['EST_DIS'], p['UPM_DIS']):
            raise ValueError('diseño persona-delito no coincide')
        w = peso(f['FAC_DEL'])
        if w is None:
            raise ValueError('FAC_DEL inválido; no se imputa')
        bp, motivo, tipo = codigo(f['BP1_20']), codigo(f['BP1_23']), codigo(f['BPCOD'])
        e, u = f['EST_DIS'], f['UPM_DIS']
        if bp in (1, 2):
            delitos.append((e, u, w, int(bp == 2 and motivo in (4, 5, 6, 8))))
        if tipo in range(5, 16) and bp == 2:
            potencial.add(pid)
            if motivo in range(1, 9):
                u1.append((e, u, w, int(motivo in (1, 2, 6, 8))))
                c2[pid] = max(c2.get(pid, 0), int(motivo in (1, 2, 6, 8)))
            else:
                excluidas.append((motivo, w))
    u4 = [(personas[p]['EST_DIS'], personas[p]['UPM_DIS'],
           float(personas[p]['FAC_ELE']), y) for p, y in c2.items()]
    excl = {
        'u1_delitos_excluidos': len(excluidas),
        'u1_masa_excluida_fac_del': sum(w for _, w in excluidas),
        'u1_ns_nr': sum(m == 99 for m, _ in excluidas),
        'u1_blancos': sum(m is None for m, _ in excluidas),
        'u1_otros_codigos': sum(m not in (None, 99) for m, _ in excluidas),
        'personas_sin_u1_por_exclusion': len(potencial - c2.keys()),
        'masa_personas_sin_u1_fac_ele': sum(float(personas[p]['FAC_ELE']) for p in potencial - c2.keys()),
        'evasion_bp20_fuera': sum(codigo(f['BP1_20']) not in (1, 2) for f in tablas['modulo']),
        'evasion_ns_nr_blanco': sum(codigo(f['BP1_20']) == 2 and codigo(f['BP1_23']) in (None, 99) for f in tablas['modulo']),
        'evasion_masa_ns_nr_blanco_fac_del': sum(float(f['FAC_DEL']) for f in tablas['modulo'] if codigo(f['BP1_20']) == 2 and codigo(f['BP1_23']) in (None, 99)),
    }
    return {'DENUNCIA_U4': u4, 'EVASION_NORMA': delitos}, sorted(marco), u1, excl


def soporte(rows):
    keys = set((e, u) for e, u, _, _ in rows)
    es = sorted(set(e for e, _ in keys))
    ws = np.array([w for _, _, w, _ in rows], dtype=float)
    total = float(ws.sum())
    return {'n': len(rows), 'numerador_n': sum(y for _, _, _, y in rows),
            'masa': total, 'punto': sum(w*y for _, _, w, y in rows)/total if total else None,
            'n_efectivo_kish': float(total**2/(ws@ws)) if total else None,
            'estratos': len(es), 'upm': len(keys),
            'singleton_soporte': sum(sum(k[0] == e for k in keys) == 1 for e in es)}


def medir(tablas, contrato):
    universos, marco, u1, excl = construir(tablas)
    indices = {k: i for i, k in enumerate(marco)}
    nums = np.zeros((len(marco), 2))
    dens = np.zeros_like(nums)
    diag = {'familias': {}, 'exclusiones': excl, 'u1': soporte(u1)}
    for j, name in enumerate(FAMILIAS):
        rows = universos[name]
        diag['familias'][name] = soporte(rows)
        for e, u, w, y in rows:
            i = indices[(e, u)]
            nums[i, j] += w*y
            dens[i, j] += w
    b = contrato['replicas']
    rng = np.random.Generator(np.random.PCG64(contrato['semilla']))
    num, den = np.zeros((b, 2)), np.zeros((b, 2))
    estratos = sorted(set(e for e, _ in marco))
    single = 0
    for e in estratos:
        pos = np.array([i for i, k in enumerate(marco) if k[0] == e])
        k = len(pos)
        if k == 1:
            single += 1
            num += nums[pos[0]]
            den += dens[pos[0]]
        else:
            sample = pos[rng.integers(0, k, size=(b, k))]
            num += nums[sample].sum(axis=1)
            den += dens[sample].sum(axis=1)
    with np.errstate(divide='ignore', invalid='ignore'):
        reps = num/den
    diag['diseno'] = {'estratos_marco': len(estratos), 'upm_marco': len(marco),
                      'singleton_marco': single, 'replicas_comunes': b,
                      'marco': 'tper_vic2 completo; dominios conservados con ceros'}
    salida = {}
    for j, name in enumerate(FAMILIAS):
        valid = reps[:, j][np.isfinite(reps[:, j])]
        salida[name] = reps[:, j]
        d = diag['familias'][name]
        d['singleton_marco'] = single
        d['replicas_validas'] = len(valid)
        d['ic_diagnostico'] = np.quantile(valid, [.025, .975]).tolist() if len(valid) else None
        gates = contrato['gates'][name]
        d['estimable'] = bool(single == 0 and d['n'] >= gates['n'] and
                              d['estratos'] >= 100 and d['upm'] >= 1000 and
                              len(valid) >= max(1000, .95*b))
        d['estado'] = 'CONTRASTE-DISPONIBLE' if d['estimable'] else 'NO-ESTIMABLE'
    return diag, salida


def activacion(meta):
    """Aceptación previa de metadatos; no abre ni descarga una reserva."""
    requerido = {'id': 'envipe_2027', 'estado': 'RESERVADA', 'instrumento': 'ENVIPE',
                 'familias': list(FAMILIAS), 'aperturas': 1,
                 'comparabilidad': 'VERIFICADA', 'autorizacion_ola': 'FIRMADA'}
    return all(meta.get(k) == v for k, v in requerido.items()) and all(
        isinstance(meta.get(k), str) and len(meta[k]) == 64
        for k in ('descriptor_sha256', 'cuestionario_sha256', 'commit2_sha256'))
