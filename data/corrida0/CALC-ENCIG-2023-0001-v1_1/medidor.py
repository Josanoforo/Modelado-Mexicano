"""`CALC-ENCIG-2023-0001-v1_1` -- mordida por canal (familia B de `CALC-ENCIG-0001`)
sobre la ola ENCIG 2023, unidad EVENTO DE TRAMITE, ponderador FAC_TRA de sec_7.
Sucesora de `CALC-ENCIG-0001` autorizada por el OBJETO 4 (D1 opcion (b)).

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

SUCESION v1.1 (`ACTO GEN2-MEDICION-DEMANDA-2`, CAJA, 15/sep/2026), CONGELADA EN
UN COMMIT PROPIO DESPUES de sellar la corrida v1_0 y ANTES de correr esta. La
v1_0 sello `B-VEREDICTO = NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA:P8_4` porque este
mismo codigo trataba como «fuera de mapa» todo texto no numerico distinto de
''/'b', y el ZIP de 2023 escribe el blanco como el literal 'NA' (soporte crudo
observado por la v1_0: P8_4 = {'0','1','NA'}, P7_3 = {1..9,'NA'}, ningun '').
UNICO CAMBIO respecto al medidor v1_0: los tokens que cuentan como blanco se
leen de `contrato.parametros.codificacion.blanco_literal` ('', 'b', 'NA') en
vez de fijarse en el codigo. El resto es byte a byte el mismo. La corrida v1_0
NO se reescribe (E.3); `repite_de` la deja SUPERADA en el registro. Spec humana sellada: `forense/prereg-caja/ENCIG-MORDIDA-2023-spec-v1_0.md`
(sha `ea4379e5…`), sucesora de `ENCIG-MORDIDA-spec-v1_0.md` (sha `00c7c4a6…`,
intacta).

Lo unico abierto al escribir este archivo, ademas del contrato: la LISTA de
miembros del ZIP (6 CSV, tamanos), y las columnas de sec_7 (51) y sec_8 (25)
segun `data/inventario-reactivos-v1_2.tsv`. Ningun valor de ninguna fila.
El codigo hereda, funcion por funcion, el de `data/corrida0/CALC-ENCIG-0001/medidor.py`
(lector csv en orden de archivo, `_p` en orden fijo de fila, `_ic` bootstrap
de UPM con reemplazo dentro de estrato) -- misma familia B, otra ola, otra
semilla (20260915).

Lo que decide el CODIGO y no la spec, declarado para que se pueda refutar:
  · JOIN: `p84` se indexa por ID_TRA de sec_8 (unica, o el join es
    NO-ESTIMABLE-LLAVE-NO-UNICA). Una fila de sec_7 esta EMPAREJADA si su
    ID_TRA existe en sec_8, tenga o no P8_4 valido; el P8_4 blanco de la pareja
    se cuenta en B-N-P84-BLANCO (fuera de U_B). La llave de control
    (ID_VIV, ID_PER, ID_TRA, N_TRA) se computa en paralelo sobre los mismos dos
    archivos: G-JOIN-LLAVE-CONTROL-COINCIDE compara el CONJUNTO de filas de
    sec_7 emparejadas por una y por otra; DIFIERE -> JOIN-NO-EXACTO y las ramas
    B salen NO-ESTIMABLE-LLAVE-NO-UNICA (no se elige llave).
  · CODIGO FUERA DE MAPA: se juzga sobre el soporte de la columna ENTERA
    (P8_4 en sec_8, P7_3 en sec_7), blanco aparte: cualquier entero fuera de
    {0,1} / {1..9} -> NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA:<col>. Un texto no
    numerico que NO este en `blanco_literal` tambien es fuera de mapa; 'NA'
    SI esta (declarado en la spec v1_1) y cuenta como blanco.
  · G-UNIVERSO-DECLARADO censa lo que las columnas DECLARADAS permiten:
    entidades distintas (CVE_ENT) y estratos/UPM de diseno de sec_7. No hay
    columna de area declarada en la spec y NO se abre ninguna otra: se escribe
    'AREAS:NO-DECLARADA-EN-SPEC'.
  · B-SUMA-*: 'SI' si |p + p_normal - 1| <= 1e-9 (los dos se cuentan sobre el
    mismo denominador; solo hay redondeo de float64), 'NO:<residuo>' si no.
  · B-ADOPCION: LISTADO-PARA-MESA-CON-RESERVA cuando B-COBERTURA < 0.5 -- la
    mayoria de los eventos de tramite no tiene observacion de P8_4 y el
    estimando es condicional al grupo observado por 8.3, como la spec advierte
    (2025 dio 0.20); LISTADO-PARA-MESA-ESTIMABLE si la cobertura es >= 0.5 y
    el join exacto; NO-ADOPTABLE-NO-ESTIMABLE sin punto. El umbral 0.5 es del
    codigo, no de la spec, y se declara aqui.
  · B-N-SIN-DISENO se cuenta sobre U_B entero (incluido el residuo de canal).
"""
from __future__ import annotations

import csv
import io
import zipfile

import numpy as np

ZIP_ID = "encig23_base_datos_csv"
P = "RESULT-ENCIG23-MOR-"
M_S7 = "encig2023_04_sec_7.csv"
M_S8 = "encig2023_05_sec_8.csv"
COLS_S7 = ["ID_TRA", "NT_TIPO", "N_TRA", "P7_3", "FAC_TRA", "EST_DIS", "UPM_DIS",
           "CVE_ENT", "UPM", "V_SEL", "R_ELE", "ID_VIV", "ID_PER"]
COLS_S8 = ["ID_TRA", "P8_4", "ID_VIV", "ID_PER", "N_TRA", "FAC_P18"]
MAPA_P73 = set(range(1, 10))
MAPA_P84 = {0, 1}
UMBRAL_SUMA = 1.0e-9
UMBRAL_COBERTURA = 0.5


# ── utilidades (heredadas de CALC-ENCIG-0001/medidor.py) ──────────────────

def _num(v):
    if v is None:
        return None
    f = float(v)
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _norm(col: str) -> str:
    return col.lstrip("﻿").lstrip("ï»¿").strip().strip('"').upper()


BLANCOS = {"", "b"}        # se REEMPLAZA desde el contrato en medir(); default = v1_0


def _codigo(s):
    if s is None:
        return None
    t = s.strip().strip('"')
    if t in BLANCOS or t.lower() in BLANCOS:
        return None
    try:
        return int(t)
    except ValueError:
        return "FUERA"           # texto no numerico: fuera de mapa, se cuenta


def _peso(s):
    if s is None:
        return None
    t = s.strip().replace(",", "")
    if not t:
        return None
    try:
        f = float(t)
    except ValueError:
        return None
    if f != f or f in (float("inf"), float("-inf")) or f <= 0:
        return None
    return f


def _llave(s):
    if s is None:
        return None
    t = s.strip().strip('"')
    return t or None


def _abre(zf, miembro, cols):
    """(filas, n_filas, ausentes, n_columnas). Orden de archivo conservado."""
    with zf.open(miembro) as fh:
        txt = io.TextIOWrapper(fh, encoding="latin-1", newline="")
        rd = csv.reader(txt)
        try:
            cab = [_norm(c) for c in next(rd)]
        except StopIteration:
            return [], 0, list(cols), 0
        idx, ausentes = {}, []
        for c in cols:
            if c in cab:
                idx[c] = cab.index(c)
            else:
                ausentes.append(c)
        orden = [idx.get(c) for c in cols]
        filas, n = [], 0
        for fila in rd:
            if not fila:
                continue
            n += 1
            filas.append(tuple((fila[i] if (i is not None and i < len(fila)) else None)
                               for i in orden))
        return filas, n, ausentes, len(cab)


def _unica(claves):
    vistos, repetidos = set(), set()
    n = 0
    for k in claves:
        n += 1
        if k in vistos:
            repetidos.add(k)
        else:
            vistos.add(k)
    g = len(vistos)
    return ("UNICA" if g == n else f"NO-UNICA:{g}/{n}"), g, n, len(repetidos)


def _soporte(codigos):
    cnt = {}
    for c in codigos:
        k = "b" if c is None else str(c)
        cnt[k] = cnt.get(k, 0) + 1
    return ";".join(f"{k}:{cnt[k]}" for k in sorted(cnt, key=lambda x: (x == "b", x == "FUERA", x)))


def _p(w, d):
    sw = 0.0
    swd = 0.0
    for wi, di in zip(w, d):
        sw += wi
        if di:
            swd += wi
    return (swd / sw) if sw > 0 else None, sw


def _ic(w, d, est, upm, replicas, seed):
    cl = {}
    n_sin = 0
    for wi, di, e, u in zip(w, d, est, upm):
        if e is None or u is None:
            n_sin += 1
            continue
        a = cl.setdefault((e, u), [0.0, 0.0])
        a[0] += wi
        if di:
            a[1] += wi
    if not cl:
        return None, None, 0, 0, 0, "NO-ESTIMABLE-DISENO-INCOMPLETO", n_sin
    estratos = {}
    for (e, u), (sw, swd) in cl.items():
        estratos.setdefault(e, []).append((sw, swd))
    n_est, n_upm = len(estratos), len(cl)
    n_unica = sum(1 for v in estratos.values() if len(v) == 1)
    bloques = [np.asarray(estratos[e], dtype=float) for e in sorted(estratos)]
    rng = np.random.Generator(np.random.PCG64(seed))
    reps = np.empty(replicas, dtype=float)
    for r in range(replicas):
        tw = 0.0
        twd = 0.0
        for b in bloques:
            k = b.shape[0]
            sel = b[rng.integers(0, k, size=k)]
            tw += float(sel[:, 0].sum())
            twd += float(sel[:, 1].sum())
        reps[r] = (twd / tw) if tw > 0 else np.nan
    fin = reps[np.isfinite(reps)]
    if fin.size == 0:
        return None, None, n_est, n_upm, n_unica, "NO-ESTIMABLE-DISENO-INCOMPLETO", n_sin
    met = "IC-CON-ESTRATOS-DE-UPM-UNICA" if n_unica > 0 else "IC-BOOTSTRAP-UPM-EN-ESTRATO"
    return (float(np.percentile(fin, 2.5)), float(np.percentile(fin, 97.5)),
            n_est, n_upm, n_unica, met, n_sin)


# ── el medidor ────────────────────────────────────────────────────────────

CEROS_B = ["B-N-EMPAREJADAS", "B-N-SEC7-SIN-PAREJA", "B-N-U", "B-N-P84-BLANCO",
           "B-N-SIN-PONDERADOR", "B-N-SIN-DISENO", "B-N-RESIDUO-CANAL",
           "B-N-EVENTOS-DESCARTADOS-POR-DEDUP", "B-N-PRE-SD", "B-N-DIG-SD", "B-N-PRE-CD",
           "B-N-DIG-CD", "B-N-ESTRATOS-PRE-SD", "B-N-UPM-PRE-SD", "B-N-ESTRATOS-UPM-UNICA-PRE-SD",
           "B-N-ESTRATOS-DIG-SD", "B-N-UPM-DIG-SD", "B-N-ESTRATOS-UPM-UNICA-DIG-SD"]
NULOS_B = ["B-COBERTURA", "B-P-RESIDUO-CANAL", "B-MASA-FAC-TRA-U", "B-P-PRE-SD", "B-IC-LO-PRE-SD",
           "B-IC-HI-PRE-SD", "B-P-DIG-SD", "B-IC-LO-DIG-SD", "B-IC-HI-DIG-SD", "B-P-PRE-CD",
           "B-P-DIG-CD", "B-P-NORMAL-PRE-SD", "B-P-NORMAL-DIG-SD", "B-DIFERENCIA-PRE-DIG-SD",
           "B-RAZON-PRE-DIG-SD", "B-DELTA-2023-VS-2025-PRE-SD", "B-DELTA-2023-VS-2025-DIG-SD"]
TEXTOS_B = {"B-VEREDICTO-CANAL": "NO-APLICA", "B-SUMA-PRE-SD": "NO-APLICA", "B-SUMA-DIG-SD": "NO-APLICA",
            "B-METODO-IC": "NO-ESTIMABLE-DISENO-INCOMPLETO", "H1-VEREDICTO": "H1-NO-EVALUABLE",
            "B-ADOPCION": "NO-ADOPTABLE-NO-ESTIMABLE"}


def medir(inputs, contrato):
    R = {}

    def put(suf, val):
        R[P + suf] = val

    par = contrato.get("parametros") or {}
    replicas = int(par.get("bootstrap_replicas", 2000))
    seed = int(contrato["seed"]["valor"])
    ref25 = par["valores_2025_referencia"]
    cod = par["codificacion"]
    B_UNO = {int(x) for x in cod["B_uno"]}
    B_CERO = {int(x) for x in cod["B_cero"]}
    B_PRE = {int(x) for x in cod["B_canal_presencial"]}
    B_DIG = {int(x) for x in cod["B_canal_digital"]}
    global BLANCOS
    BLANCOS = {str(x) for x in cod.get("blanco_literal", ["", "b"])}

    zf = zipfile.ZipFile(inputs[ZIP_ID]["ruta_absoluta"])
    nombres = zf.namelist()
    put("G-N-MIEMBROS-ZIP", len(nombres))

    def rendirse(ver_join, ver_b):
        for s in CEROS_B:
            R.setdefault(P + s, 0)
        for s in NULOS_B:
            R.setdefault(P + s, None)
        for s, v in TEXTOS_B.items():
            R.setdefault(P + s, v)
        R.setdefault(P + "G-VEREDICTO-JOIN", ver_join)
        put("B-VEREDICTO", ver_b)
        return R

    faltantes_miembro = [m for m in (M_S7, M_S8) if m not in nombres]
    if faltantes_miembro:
        for s in ["G-N-FILAS-SEC7", "G-N-FILAS-SEC8", "G-N-COLUMNAS-SEC7", "G-N-COLUMNAS-SEC8",
                  "G-N-IDTRA-REPETIDOS-SEC7"]:
            put(s, 0)
        razon = "NO-ESTIMABLE-MIEMBRO-AUSENTE:" + ";".join(faltantes_miembro)
        for s in ["G-COLUMNAS-AUSENTES", "G-PONDERADOR-POR-ARCHIVO", "G-LLAVE-SEC7-DECLARADA-UNICA",
                  "G-LLAVE-SEC7-IDTRA-NTTIPO-UNICA", "G-LLAVE-SEC7-IDTRA-UNICA",
                  "G-LLAVE-SEC8-IDTRA-UNICA", "G-JOIN-LLAVE-CONTROL-COINCIDE", "G-SOPORTE-P84",
                  "G-SOPORTE-P73", "G-UNIVERSO-DECLARADO"]:
            put(s, razon)
        return rendirse(razon, razon)

    # ── lectura ───────────────────────────────────────────────────────────
    s7, n_s7, falta7, nc7 = _abre(zf, M_S7, COLS_S7)
    s8, n_s8, falta8, nc8 = _abre(zf, M_S8, COLS_S8)
    i7 = {c: i for i, c in enumerate(COLS_S7)}
    i8 = {c: i for i, c in enumerate(COLS_S8)}
    put("G-N-FILAS-SEC7", n_s7); put("G-N-FILAS-SEC8", n_s8)
    put("G-N-COLUMNAS-SEC7", nc7); put("G-N-COLUMNAS-SEC8", nc8)
    ausentes = [f"{M_S7}:{c}" for c in falta7] + [f"{M_S8}:{c}" for c in falta8 if c != "FAC_P18"]
    put("G-COLUMNAS-AUSENTES", "NINGUNA" if not ausentes else ";".join(ausentes))
    put("G-PONDERADOR-POR-ARCHIVO",
        "FAC-TRA-DE-SEC7-Y-FAC-P18-SIN-USAR" if "FAC_TRA" not in falta7 else f"FAC-TRA-AUSENTE:{M_S7}")

    # ── guardias de llave ─────────────────────────────────────────────────
    dec = ["CVE_ENT", "UPM", "V_SEL", "R_ELE", "N_TRA"]
    if not any(c in falta7 for c in dec):
        put("G-LLAVE-SEC7-DECLARADA-UNICA", _unica(tuple(_llave(r[i7[c]]) for c in dec) for r in s7)[0])
    else:
        put("G-LLAVE-SEC7-DECLARADA-UNICA", "NO-ESTIMABLE-COLUMNA-AUSENTE")
    if "ID_TRA" not in falta7 and "NT_TIPO" not in falta7:
        put("G-LLAVE-SEC7-IDTRA-NTTIPO-UNICA",
            _unica((_llave(r[i7["ID_TRA"]]), _llave(r[i7["NT_TIPO"]])) for r in s7)[0])
    else:
        put("G-LLAVE-SEC7-IDTRA-NTTIPO-UNICA", "NO-ESTIMABLE-COLUMNA-AUSENTE")
    if "ID_TRA" not in falta7:
        v7, _, _, rep7 = _unica(_llave(r[i7["ID_TRA"]]) for r in s7)
        put("G-LLAVE-SEC7-IDTRA-UNICA", v7); put("G-N-IDTRA-REPETIDOS-SEC7", rep7)
    else:
        put("G-LLAVE-SEC7-IDTRA-UNICA", "NO-ESTIMABLE-COLUMNA-AUSENTE"); put("G-N-IDTRA-REPETIDOS-SEC7", 0)
    if "ID_TRA" not in falta8:
        v8 = _unica(_llave(r[i8["ID_TRA"]]) for r in s8)[0]
    else:
        v8 = "NO-ESTIMABLE-COLUMNA-AUSENTE"
    put("G-LLAVE-SEC8-IDTRA-UNICA", v8)

    # ── soportes (columna entera) ─────────────────────────────────────────
    cods84 = [_codigo(r[i8["P8_4"]]) for r in s8] if "P8_4" not in falta8 else []
    cods73 = [_codigo(r[i7["P7_3"]]) for r in s7] if "P7_3" not in falta7 else []
    put("G-SOPORTE-P84", _soporte(cods84) if cods84 else "NO-ESTIMABLE-COLUMNA-AUSENTE")
    put("G-SOPORTE-P73", _soporte(cods73) if cods73 else "NO-ESTIMABLE-COLUMNA-AUSENTE")
    fuera84 = {c for c in cods84 if c is not None and (c == "FUERA" or c not in MAPA_P84)}
    fuera73 = {c for c in cods73 if c is not None and (c == "FUERA" or c not in MAPA_P73)}

    # ── universo declarado (solo columnas declaradas) ─────────────────────
    ents = {_llave(r[i7["CVE_ENT"]]) for r in s7 if "CVE_ENT" not in falta7} - {None}
    ests = {_llave(r[i7["EST_DIS"]]) for r in s7 if "EST_DIS" not in falta7} - {None}
    upms = {(_llave(r[i7["EST_DIS"]]), _llave(r[i7["UPM_DIS"]])) for r in s7
            if "EST_DIS" not in falta7 and "UPM_DIS" not in falta7}
    put("G-UNIVERSO-DECLARADO",
        f"ENTIDADES:{len(ents)};EST_DIS:{len(ests)};UPM_DIS:{len(upms)};AREAS:NO-DECLARADA-EN-SPEC")

    # ── join: llave primaria y llave de control en paralelo ───────────────
    faltan_b = ([c for c in ["ID_TRA", "P7_3", "FAC_TRA"] if c in falta7]
                + [c for c in ["ID_TRA", "P8_4"] if c in falta8])
    if faltan_b:
        razon = "NO-ESTIMABLE-COLUMNA-AUSENTE:" + ";".join(faltan_b)
        put("G-JOIN-LLAVE-CONTROL-COINCIDE", razon)
        return rendirse("COLUMNAS-AUSENTES:" + ";".join(faltan_b), razon)
    if not v8.startswith("UNICA"):
        put("G-JOIN-LLAVE-CONTROL-COINCIDE", "NO-APLICA")
        return rendirse("NO-ESTIMABLE-LLAVE-NO-UNICA", "NO-ESTIMABLE-LLAVE-NO-UNICA")

    p84 = {}
    for r in s8:
        p84[_llave(r[i8["ID_TRA"]])] = _codigo(r[i8["P8_4"]])
    ctrl_ok = not any(c in falta7 for c in ("ID_VIV", "ID_PER", "N_TRA")) and \
        not any(c in falta8 for c in ("ID_VIV", "ID_PER", "N_TRA"))
    if ctrl_ok:
        ctrl8 = {(_llave(r[i8["ID_VIV"]]), _llave(r[i8["ID_PER"]]), _llave(r[i8["ID_TRA"]]),
                  _llave(r[i8["N_TRA"]])) for r in s8}
        emp_prim = {i for i, r in enumerate(s7) if _llave(r[i7["ID_TRA"]]) in p84}
        emp_ctrl = {i for i, r in enumerate(s7)
                    if (_llave(r[i7["ID_VIV"]]), _llave(r[i7["ID_PER"]]), _llave(r[i7["ID_TRA"]]),
                        _llave(r[i7["N_TRA"]])) in ctrl8}
        if emp_prim == emp_ctrl:
            put("G-JOIN-LLAVE-CONTROL-COINCIDE", "COINCIDE")
            join_exacto = True
        else:
            put("G-JOIN-LLAVE-CONTROL-COINCIDE", f"DIFIERE:{len(emp_prim)}/{len(emp_ctrl)}")
            join_exacto = False
    else:
        put("G-JOIN-LLAVE-CONTROL-COINCIDE", "NO-ESTIMABLE-COLUMNA-AUSENTE")
        join_exacto = True      # la llave primaria es unica; el control no es evaluable

    if not join_exacto:
        return rendirse("JOIN-NO-EXACTO", "NO-ESTIMABLE-LLAVE-NO-UNICA")
    put("G-VEREDICTO-JOIN", "JOIN-EXACTO")

    if fuera84:
        return rendirse("JOIN-EXACTO", "NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA:P8_4")
    if fuera73:
        return rendirse("JOIN-EXACTO", "NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA:P7_3")

    # ── familia B, rama SD ────────────────────────────────────────────────
    filas = []          # (w, d, canal, est, upm, id_tra)
    n_sin_pareja = n_emp = n_blanco = n_sinpond = n_res = n_sin_dis = 0
    w_res = 0.0
    for r in s7:
        k = _llave(r[i7["ID_TRA"]])
        if k not in p84:
            n_sin_pareja += 1
            continue
        n_emp += 1
        c = p84[k]
        if c is None:
            n_blanco += 1
            continue
        pw = _peso(r[i7["FAC_TRA"]])
        if pw is None:
            n_sinpond += 1
            continue
        canal = _codigo(r[i7["P7_3"]])
        e = _llave(r[i7["EST_DIS"]]) if "EST_DIS" not in falta7 else None
        u = _llave(r[i7["UPM_DIS"]]) if "UPM_DIS" not in falta7 else None
        if e is None or u is None:
            n_sin_dis += 1
        d = 1 if c in B_UNO else 0
        if canal in B_PRE:
            filas.append((pw, d, "PRE", e, u, k))
        elif canal in B_DIG:
            filas.append((pw, d, "DIG", e, u, k))
        else:
            n_res += 1
            w_res += pw

    put("B-N-EMPAREJADAS", n_emp); put("B-N-SEC7-SIN-PAREJA", n_sin_pareja)
    put("B-COBERTURA", _num(n_emp / n_s7) if n_s7 else None)
    put("B-N-P84-BLANCO", n_blanco); put("B-N-SIN-PONDERADOR", n_sinpond)
    put("B-N-SIN-DISENO", n_sin_dis); put("B-N-RESIDUO-CANAL", n_res)
    n_u = len(filas) + n_res
    put("B-N-U", n_u)
    masa = sum(f[0] for f in filas) + w_res
    put("B-MASA-FAC-TRA-U", _num(masa) if n_u else None)
    p_res = (w_res / masa) if masa > 0 else None
    put("B-P-RESIDUO-CANAL", _num(p_res))
    put("B-VEREDICTO-CANAL",
        "CANAL-DICOTOMICO-EN-EL-INSTRUMENTO" if p_res == 0 else "DICOTOMIA-ES-PROPIEDAD-DEL-RECORTE")

    if not filas:
        return rendirse("JOIN-EXACTO", "NO-ESTIMABLE-UNIVERSO-VACIO")

    vistos, cd, n_desc = set(), [], 0
    for f in filas:
        if f[5] in vistos:
            n_desc += 1
            continue
        vistos.add(f[5]); cd.append(f)
    put("B-N-EVENTOS-DESCARTADOS-POR-DEDUP", n_desc)

    metodos = []

    def brazo(fs, canal, suf, con_ic):
        sel = [f for f in fs if f[2] == canal]
        put(f"B-N-{suf}", len(sel))
        if not sel:
            put(f"B-P-{suf}", None)
            if con_ic:
                put(f"B-P-NORMAL-{suf}", None); put(f"B-SUMA-{suf}", "NO-ESTIMABLE-UNIVERSO-VACIO")
                put(f"B-IC-LO-{suf}", None); put(f"B-IC-HI-{suf}", None)
                put(f"B-N-ESTRATOS-{suf}", 0); put(f"B-N-UPM-{suf}", 0)
                put(f"B-N-ESTRATOS-UPM-UNICA-{suf}", 0)
            return None
        w = [f[0] for f in sel]; d = [f[1] for f in sel]; nd = [1 - f[1] for f in sel]
        p, _ = _p(w, d)
        put(f"B-P-{suf}", _num(p))
        if con_ic:
            pn, _ = _p(w, nd)
            put(f"B-P-NORMAL-{suf}", _num(pn))
            res = abs(p + pn - 1.0)
            put(f"B-SUMA-{suf}", "SI" if res <= UMBRAL_SUMA else f"NO:{res:.3e}")
            lo, hi, ne, nu, nun, met, _ = _ic(w, d, [f[3] for f in sel], [f[4] for f in sel],
                                              replicas, seed)
            put(f"B-IC-LO-{suf}", _num(lo)); put(f"B-IC-HI-{suf}", _num(hi))
            put(f"B-N-ESTRATOS-{suf}", ne); put(f"B-N-UPM-{suf}", nu)
            put(f"B-N-ESTRATOS-UPM-UNICA-{suf}", nun)
            metodos.append(met)
        return p

    p_pre = brazo(filas, "PRE", "PRE-SD", True)
    p_dig = brazo(filas, "DIG", "DIG-SD", True)
    brazo(cd, "PRE", "PRE-CD", False)
    brazo(cd, "DIG", "DIG-CD", False)

    put("B-DIFERENCIA-PRE-DIG-SD", _num(None if p_pre is None or p_dig is None else p_pre - p_dig))
    put("B-RAZON-PRE-DIG-SD", _num(None if p_pre is None or not p_dig else p_pre / p_dig))
    put("B-METODO-IC",
        "IC-CON-ESTRATOS-DE-UPM-UNICA" if "IC-CON-ESTRATOS-DE-UPM-UNICA" in metodos
        else (metodos[0] if metodos else "NO-ESTIMABLE-DISENO-INCOMPLETO"))
    put("B-DELTA-2023-VS-2025-PRE-SD",
        _num(None if p_pre is None else p_pre - float(ref25["B-P-PRE-SD"])))
    put("B-DELTA-2023-VS-2025-DIG-SD",
        _num(None if p_dig is None else p_dig - float(ref25["B-P-DIG-SD"])))
    if p_pre is None or p_dig is None:
        put("H1-VEREDICTO", "H1-NO-EVALUABLE")
    else:
        put("H1-VEREDICTO", "H1-SOSTENIDA" if p_pre > p_dig else "H1-NO-SOSTENIDA")
    put("B-VEREDICTO", "TASA-REPORTADA")

    cob = R[P + "B-COBERTURA"]
    if p_pre is None or p_dig is None:
        put("B-ADOPCION", "NO-ADOPTABLE-NO-ESTIMABLE")
    elif cob is not None and cob < UMBRAL_COBERTURA:
        put("B-ADOPCION", "LISTADO-PARA-MESA-CON-RESERVA")
    else:
        put("B-ADOPCION", "LISTADO-PARA-MESA-ESTIMABLE")
    return R
