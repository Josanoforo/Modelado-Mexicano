#!/usr/bin/env python3
"""HITO D · R7.2 -- ocho olas ENVIPE (2018-2025), pareo de identificabilidad.

Especificación: forense/notas/2026-08-04-r7-2-ocho-olas.md.

Reproduce primero la brecha de la ola 2025 (`hitoD-R7.2-revision-v1_0.md §2.4`),
luego agrupa las ocho olas y mide la brecha de denuncia (BP1_20) asegurado vs.
no_asegurado (BP2_1), dentro de BPCOD=01, CONDICIONADA por identificabilidad
del agresor (BP1_12_1: 0=conocido, 1=desconocido, dentro de la submuestra que
presenció el delito) -- el pareo que 2025 sola no podía ejecutar (n=121/124).

Formato de fila de TMod_Vic: dos variantes por año (verificado, no asumido):
- 2018-2023: filas separadas por '\n' real, pero cada campo trae un '\r'
  final DENTRO de las comillas (artefacto de exportación de INEGI). Se
  parsea con newline='' para que el csv module trate ese '\r' como
  contenido literal (no como separador de fila), y se recorta después.
- 2024-2025: formato limpio, el recorte es un no-op.

Corre desde la raíz del repo: python3 tests/hitoD_r7_2_ocho_olas.py
Requiere data/raw (symlink) -> envipe{2018..2025}_csv.zip.
"""
import csv
import io
import sys
import zipfile

sys.path.insert(0, "tests")
from svystat import prop_ultimate_cluster  # noqa: E402

YEARS = list(range(2018, 2026))

TMOD_PATH = {
    2018: 'conjunto_de_datos_tmod_vic_envipe_2018/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe_2018.csv',
    2019: 'conjunto_de_datos_TMod_Vic_ENVIPE_2019/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2019.csv',
    2020: 'conjunto_de_datos_TMod_Vic_ENVIPE_2020/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2020.csv',
    2021: 'conjunto_de_datos_TMod_Vic_ENVIPE_2021/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2021.csv',
    2022: 'conjunto_de_datos_TMod_Vic_ENVIPE_2022/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2022.csv',
    2023: 'tmod_vic_envipe2023/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2023.csv',
    2024: 'tmod_vic_envipe2024/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2024.csv',
    2025: 'tmod_vic_envipe2025/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2025.csv',
}


def read_tmod_vic(year):
    zpath = f"data/raw/envipe{year}_csv.zip"
    z = zipfile.ZipFile(zpath)
    with z.open(TMOD_PATH[year]) as f:
        raw = f.read()
    text = raw.decode('latin-1')
    if text.startswith('﻿'):
        text = text[1:]
    reader = csv.DictReader(io.StringIO(text, newline=''))
    return [{k: (v.rstrip('\r\n') if v is not None else v) for k, v in r.items()} for r in reader]


def bp2_1_universe(rows):
    from collections import Counter
    by_code = {}
    for r in rows:
        by_code.setdefault(r['BPCOD'], Counter())[r.get('BP2_1', '')] += 1
    return by_code


def denuncia_por_cobertura(rows):
    sub = [r for r in rows if r['BPCOD'] == '01' and r.get('BP2_1') in ('1', '2')]
    out = {}
    for grupo, etiqueta in (('1', 'asegurado'), ('2', 'no_asegurado')):
        est_rows = []
        for r in sub:
            if r['BP2_1'] != grupo:
                continue
            bp1_20 = r.get('BP1_20', '')
            if bp1_20 not in ('1', '2'):
                continue
            est_rows.append((r['EST_DIS'], r['UPM_DIS'], float(r['FAC_DEL']), 1.0 if bp1_20 == '1' else 0.0))
        res = prop_ultimate_cluster(est_rows)
        out[etiqueta] = {'n': len(est_rows), 'n_pond': sum(w for *_, w, _y in est_rows) if False else sum(r[2] for r in est_rows), **res}
    return out


def identificabilidad_por_cobertura(rows):
    sub = [r for r in rows if r['BPCOD'] == '01' and r.get('BP2_1') in ('1', '2')]
    out = {}
    for grupo, etiqueta in (('1', 'asegurado'), ('2', 'no_asegurado')):
        obs = [r for r in sub if r['BP2_1'] == grupo and r.get('BP1_12_1') in ('0', '1')]
        n = len(obs)
        if n == 0:
            out[etiqueta] = {'n': 0}
            continue
        est_rows = [(r['EST_DIS'], r['UPM_DIS'], float(r['FAC_DEL']), 1.0 if r['BP1_12_1'] == '0' else 0.0) for r in obs]
        res = prop_ultimate_cluster(est_rows)
        out[etiqueta] = {'n': n, **res}
    return out


def brecha_de(cellA, cellB):
    d = cellA['p_hat'] - cellB['p_hat']
    se = (cellA['se'] ** 2 + cellB['se'] ** 2) ** 0.5
    lo = d - 1.959963985 * se
    hi = d + 1.959963985 * se
    return d, se, (lo, hi)


def subsample_identificable(year):
    """Filas de BPCOD=01, BP2_1 válida, BP1_12_1 observable, BP1_20 válida --
    la submuestra sobre la que se puede condicionar por identificabilidad."""
    rows = read_tmod_vic(year)
    sub = [r for r in rows if r['BPCOD'] == '01' and r.get('BP2_1') in ('1', '2')]
    obs = [r for r in sub if r.get('BP1_12_1') in ('0', '1')]
    out = []
    for r in obs:
        bp1_20 = r.get('BP1_20', '')
        if bp1_20 not in ('1', '2'):
            continue
        out.append({
            'asegurado': r['BP2_1'] == '1',
            'conocido': r['BP1_12_1'] == '0',
            'denuncio': bp1_20 == '1',
            'w': float(r['FAC_DEL']),
            'est': f"{year}_{r['EST_DIS']}",
            'upm': f"{year}_{r['UPM_DIS']}",
        })
    return out


def cell_stat(records, asegurado, conocido):
    rows = [(r['est'], r['upm'], r['w'], 1.0 if r['denuncio'] else 0.0)
            for r in records if r['asegurado'] == asegurado and r['conocido'] == conocido]
    n = len(rows)
    if n == 0:
        return {'n': 0}
    res = prop_ultimate_cluster(rows)
    return {'n': n, 'n_pond': sum(r[2] for r in rows), **res}


def paso_1_reproduce_2025():
    print("=" * 70)
    print("PASO 1 -- reproduce 2025 (control, contra hitoD-R7.2-revision-v1_0.md §2.4)")
    print("=" * 70)
    rows = read_tmod_vic(2025)
    universo = bp2_1_universe(rows)
    fuera = sum(sum(c.values()) for code, c in universo.items() if code != '01')
    blanco = sum(c.get('', 0) for code, c in universo.items() if code != '01')
    print(f"BP2_1 fuera de BPCOD=01: {fuera} filas, {blanco} en blanco -- {'DEGENERADA' if fuera == blanco else 'NO degenerada'}")
    den = denuncia_por_cobertura(rows)
    for k, v in den.items():
        lo, hi = v['ic95']
        print(f"  {k}: n={v['n']} p={v['p_hat']*100:.1f}% se={v['se']*100:.2f}pp IC95=[{lo*100:.1f}%,{hi*100:.1f}%]")
    d, se, (lo, hi) = brecha_de(den['asegurado'], den['no_asegurado'])
    print(f"  BRECHA = {d*100:.1f}pp se={se*100:.2f}pp IC95=[{lo*100:.1f}pp,{hi*100:.1f}pp]")
    ok = abs(d * 100 - 11.9) < 0.05 and abs(lo * 100 - 6.4) < 0.05 and abs(hi * 100 - 17.4) < 0.05
    print(f"  REPRODUCE 11.9pp IC[6.4,17.4]: {'SI' if ok else 'NO -- PARO'}")
    if not ok:
        sys.exit(1)
    ident = identificabilidad_por_cobertura(rows)
    for k, v in ident.items():
        lo, hi = v['ic95']
        print(f"  identificabilidad {k}: n={v['n']} %conocido={v['p_hat']*100:.1f}% IC95=[{lo*100:.1f}%,{hi*100:.1f}%]")
    return ok


def paso_2_comparabilidad():
    print()
    print("=" * 70)
    print("PASO 2 -- comparabilidad año x variable")
    print("=" * 70)
    targets = ['BPCOD', 'BP2_1', 'BP1_12_1', 'BP1_12_2', 'BP1_12_3', 'BP1_12_4', 'BP1_12_5',
               'BP1_13', 'BP1_20', 'FAC_DEL', 'UPM_DIS', 'EST_DIS', 'RESUL_H']
    for y in YEARS:
        rows = read_tmod_vic(y)
        header = set(rows[0].keys()) if rows else set()
        faltan = [t for t in targets if t not in header]
        resul_h = set(r.get('RESUL_H') for r in rows)
        n_est = len(set(r['EST_DIS'] for r in rows))
        blanco_marker = None
        u = bp2_1_universe(rows)
        fuera = [(code, c) for code, c in u.items() if code != '01']
        markers = set()
        for code, c in fuera:
            for k in c:
                markers.add(k)
        print(f"{y}: faltan={faltan or 'ninguno'} RESUL_H={resul_h} n_EST_DIS={n_est} marcador_blanco_fuera_BPCOD01={markers}")


def paso_3_agrupado():
    print()
    print("=" * 70)
    print("PASO 3 -- agrupado, brecha pareada por identificabilidad")
    print("=" * 70)
    all_records = []
    print("-- por año (submuestra con identificabilidad observable) --")
    for y in YEARS:
        recs = subsample_identificable(y)
        all_records.extend(recs)
        n_a = sum(1 for r in recs if r['asegurado'])
        n_na = sum(1 for r in recs if not r['asegurado'])
        n_a_c = sum(1 for r in recs if r['asegurado'] and r['conocido'])
        n_na_c = sum(1 for r in recs if not r['asegurado'] and r['conocido'])
        print(f"  {y}: asegurado n={n_a} (conocido={n_a_c})  no_asegurado n={n_na} (conocido={n_na_c})")

    print(f"\nAgrupado, n total submuestra identificabilidad observable = {len(all_records)}")
    resultado = {}
    for conocido_flag, etiqueta in ((True, 'CONOCIDO'), (False, 'DESCONOCIDO')):
        print(f"\n-- estrato identificabilidad: {etiqueta} --")
        cA = cell_stat(all_records, True, conocido_flag)
        cB = cell_stat(all_records, False, conocido_flag)
        for lbl, c in (('asegurado', cA), ('no_asegurado', cB)):
            if c['n']:
                singleton = c.get('n_estratos_singleton', 0)
                nest = c.get('n_estratos', 0)
                print(f"  {lbl}: n={c['n']} n_pond={c['n_pond']:.0f} p={c['p_hat']*100:.1f}% se={c['se']*100:.2f}pp "
                      f"n_estratos={nest} singleton={singleton} ({100*singleton/nest:.0f}%)" if nest else f"  {lbl}: n={c['n']}")
            else:
                print(f"  {lbl}: n=0")
        resultado[etiqueta] = (cA, cB)
        if cA['n'] and cB['n']:
            d, se, (lo, hi) = brecha_de(cA, cB)
            print(f"  BRECHA ({etiqueta}) = {d*100:.1f}pp se={se*100:.2f}pp IC95=[{lo*100:.1f}pp,{hi*100:.1f}pp]"
                  f"  {'-- CRUZA 20' if hi*100 >= 20 else '-- no cruza 20'}")
    return resultado


if __name__ == '__main__':
    paso_1_reproduce_2025()
    paso_2_comparabilidad()
    paso_3_agrupado()
