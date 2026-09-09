"""`CALC-ENVIPE-0001` — tasa de no-denuncia por miedo o desconfianza, ENVIPE 2025.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO EN EL COMMIT-1 DE `ACTO GEN2-LOTE-ENVIPE-1`, ANTES DE
LEER UN SOLO BYTE DE MICRODATO. Spec sellada que lo gobierna:
`forense/prereg-caja/ENVIPE-DENUNCIA-spec-v1_0.md`
(`prereg-caja-ENVIPE-DENUNCIA`, sha `e404e7b5…`).

Lo unico abierto al escribir este archivo: manifiesto, descriptor
(`diccionario_de_datos/*`), catalogos (`catalogos/*`), metadato
(`metadatos/*.txt`), la lista de miembros del ZIP y los PDF de cuestionario.
NINGUN `conjunto_de_datos/*.csv`.

Releva la demanda `CORR-0009` (`RES-0027`/`RES-0028`). NO mide
`RES-0039..0042` (otra apertura, ver §7.4 de la sellada). NO toca
`milpa/tramite.yaml` ni ningun sello previo.
"""
from __future__ import annotations

import csv
import io
import zipfile

import numpy as np

# ── constantes de la spec congelada ───────────────────────────────────────

ZIP_ID = "envipe2025_csv"
T_MOD = "tmod_vic_envipe2025/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2025.csv"
T_PER = "tper_vic2_envipe2025/conjunto_de_datos/conjunto_de_datos_tper_vic2_envipe2025.csv"

COLS_MOD = ["ID_PER", "ID_DEL", "BPCOD", "BP1_20", "BP1_23",
            "FAC_DEL", "EST_DIS", "UPM_DIS"]
COLS_PER = ["ID_PER", "FAC_ELE", "EST_DIS", "UPM_DIS"]

BPCOD_PERSONALES = {5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15}
C1_UNO = {1, 2, 6}                 # miedo agresor · miedo extorsion · desconfianza
C1_CERO = {3, 4, 5, 7, 8}
C2_UNO = {1, 2, 6, 8}              # + actitud hostil de la autoridad (particion GEN1)
C2_CERO = {3, 4, 5, 7}
U1_CODIGOS = {1, 2, 3, 4, 5, 6, 7, 8}
COD_OTRA = 9
COD_NSNR = 99


# ── utilidades ────────────────────────────────────────────────────────────

def _num(v):
    """`NO-ESTIMABLE` viaja como `null`, nunca como NaN ni como cadena."""
    if v is None:
        return None
    f = float(v)
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _norm(col: str) -> str:
    """Los CSV de INEGI vienen UTF-8 con BOM y se leen en latin-1 (nunca
    falla; todos los campos de esta spec son ASCII)."""
    return col.lstrip("﻿").lstrip("ï»¿").strip().upper()


def _codigo(s):
    """`BP1_23`/`BPCOD`/`BP1_20` -> entero, o None si blanco/no numerico.

    El descriptor declara `BP1_23` como Numerico(2) con claves `01..09`, `99`
    y `b` (blanco). En el CSV eso puede venir con o sin cero a la izquierda,
    vacio, o con la letra `b`. Ninguna de esas formas se imputa a un codigo:
    lo que no es un entero es BLANCO y se cuenta aparte."""
    if s is None:
        return None
    t = str(s).strip()
    if not t:
        return None
    try:
        return int(t)
    except ValueError:
        return None


def _flotante(s):
    if s is None:
        return None
    t = str(s).strip()
    if not t:
        return None
    try:
        f = float(t)
    except ValueError:
        return None
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _lee_tabla(zf: zipfile.ZipFile, miembro: str, columnas: list[str]):
    """Devuelve (filas, faltantes). `filas` es una lista de dicts con SOLO las
    columnas pedidas, en el orden del archivo (sumas en orden fijo). No usa
    el modulo `csv` sobre el archivo entero por columnas ajenas: lo lee con
    `csv.reader`, que respeta comillas, y se queda con los indices pedidos."""
    crudo = zf.read(miembro)
    texto = crudo.decode("latin-1")
    lector = csv.reader(io.StringIO(texto, newline=""))
    cabecera = [_norm(c) for c in next(lector)]
    idx = {}
    faltantes = []
    for c in columnas:
        if c in cabecera:
            idx[c] = cabecera.index(c)
        else:
            faltantes.append(c)
    filas = []
    if not faltantes:
        ancho = len(cabecera)
        for fila in lector:
            if len(fila) < ancho:
                fila = fila + [""] * (ancho - len(fila))
            filas.append({c: fila[i] for c, i in idx.items()})
    else:
        # se cuentan las filas igual, para que el negativo declare universo
        for fila in lector:
            filas.append({})
    return filas, faltantes


def _p_ponderada(desenlace, peso):
    sw = float(np.sum(peso))
    if sw <= 0:
        return None, sw
    return float(np.sum(peso * desenlace) / sw), sw


def _ic_bootstrap(desenlace, peso, estrato, upm, replicas, semilla):
    """Bootstrap de UPM CON REEMPLAZO dentro de estrato, conservando el numero
    de UPM por estrato; percentiles 2.5/97.5.

    Un estrato con UNA sola UPM se re-muestrea a si mismo: aporta varianza
    cero, no se colapsa con otro estrato ni se descarta (regla §3.4 de la
    sellada). Su conteo lo devuelve el tercer elemento de la tupla."""
    if len(desenlace) == 0:
        return None, None, 0, 0, 0
    rng = np.random.Generator(np.random.PCG64(semilla))
    wd = peso * desenlace
    # agregados por (estrato, upm), en orden fijo
    claves = np.array([f"{e}␟{u}" for e, u in zip(estrato, upm)])
    upm_unicas, inverso = np.unique(claves, return_inverse=True)
    sw_upm = np.bincount(inverso, weights=peso, minlength=len(upm_unicas))
    swd_upm = np.bincount(inverso, weights=wd, minlength=len(upm_unicas))
    estr_de_upm = np.array([k.split("␟")[0] for k in upm_unicas])
    estratos = np.unique(estr_de_upm)
    n_upm_unica = 0
    acc_sw = np.zeros(replicas, dtype=float)
    acc_swd = np.zeros(replicas, dtype=float)
    for e in estratos:                       # orden fijo: np.unique ordena
        pos = np.flatnonzero(estr_de_upm == e)
        k = len(pos)
        if k == 1:
            n_upm_unica += 1
            acc_sw += sw_upm[pos[0]]
            acc_swd += swd_upm[pos[0]]
            continue
        elegidas = rng.integers(0, k, size=(replicas, k))
        acc_sw += sw_upm[pos][elegidas].sum(axis=1)
        acc_swd += swd_upm[pos][elegidas].sum(axis=1)
    validas = acc_sw > 0
    if not validas.any():
        return None, None, n_upm_unica, len(estratos), len(upm_unicas)
    ps = acc_swd[validas] / acc_sw[validas]
    lo = float(np.percentile(ps, 2.5))
    hi = float(np.percentile(ps, 97.5))
    return lo, hi, n_upm_unica, len(estratos), len(upm_unicas)


# ── medidor ───────────────────────────────────────────────────────────────

def medir(inputs, contrato):
    par = contrato["parametros"]
    replicas = int(par["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    p_gen1 = float(par["valor_gen1_referencia"])
    tol_replica = float(par["umbral_replica_gen1"])
    grano = int(par["grano_milpa_decimales"])

    ids = [f"RESULT-ENVIPE-DEN-{s}" for s in par["sufijos_result"]]
    out = {k: None for k in ids}
    for k in ("VEREDICTO", "VEREDICTO-EXHAUSTIVIDAD", "REPRODUCE-GEN1",
              "METODO-IC", "ADOPCION-P3"):
        out[f"RESULT-ENVIPE-DEN-{k}"] = "NO-ESTIMABLE"
    for k in ("N-FILAS-MODULO", "N-BPCOD-05-15", "N-NO-DENUNCIO", "N-U1",
              "N-BP1-23-09", "N-BP1-23-99", "N-BP1-23-BLANCO",
              "N-SIN-PONDERADOR", "N-SIN-DISENO", "N-U3", "N-PERSONAS-U4",
              "N-ESTRATOS-U1", "N-UPM-U1", "N-ESTRATOS-UPM-UNICA-U1"):
        out[f"RESULT-ENVIPE-DEN-{k}"] = 0

    def para(veredicto):
        out["RESULT-ENVIPE-DEN-VEREDICTO"] = veredicto
        out["RESULT-ENVIPE-DEN-ADOPCION-P3"] = "NO-ADOPTABLE-NO-ESTIMABLE"
        return out

    zf = zipfile.ZipFile(inputs[ZIP_ID]["ruta_absoluta"])
    mod, faltan_mod = _lee_tabla(zf, T_MOD, COLS_MOD)
    per, faltan_per = _lee_tabla(zf, T_PER, COLS_PER)
    out["RESULT-ENVIPE-DEN-N-FILAS-MODULO"] = len(mod)
    if faltan_mod or faltan_per:
        faltan = ",".join(faltan_mod + faltan_per)
        return para(f"NO-ESTIMABLE-COLUMNA-AUSENTE:{faltan}")

    # ── universo, paso a paso, contando antes y despues ───────────────────
    personales = [f for f in mod if _codigo(f["BPCOD"]) in BPCOD_PERSONALES]
    out["RESULT-ENVIPE-DEN-N-BPCOD-05-15"] = len(personales)
    no_den = [f for f in personales if _codigo(f["BP1_20"]) == 2]
    out["RESULT-ENVIPE-DEN-N-NO-DENUNCIO"] = len(no_den)

    n_blanco = n_otra = n_nsnr = 0
    n_sin_pond = n_sin_dis = 0
    u1, u3 = [], []
    for f in no_den:
        cod = _codigo(f["BP1_23"])
        if cod is None:
            n_blanco += 1
            continue
        w = _flotante(f["FAC_DEL"])
        if w is None or w <= 0:
            n_sin_pond += 1
            continue
        e = str(f["EST_DIS"]).strip()
        u = str(f["UPM_DIS"]).strip()
        if not e or not u:
            n_sin_dis += 1
        reg = {"cod": cod, "w": w, "e": e, "u": u, "id_per": f["ID_PER"]}
        if cod in U1_CODIGOS:
            u1.append(reg)
            u3.append(reg)
        elif cod == COD_OTRA:
            n_otra += 1
            u3.append(reg)
        elif cod == COD_NSNR:
            n_nsnr += 1
            u3.append(reg)
    out["RESULT-ENVIPE-DEN-N-U1"] = len(u1)
    out["RESULT-ENVIPE-DEN-N-U3"] = len(u3)
    out["RESULT-ENVIPE-DEN-N-BP1-23-09"] = n_otra
    out["RESULT-ENVIPE-DEN-N-BP1-23-99"] = n_nsnr
    out["RESULT-ENVIPE-DEN-N-BP1-23-BLANCO"] = n_blanco
    out["RESULT-ENVIPE-DEN-N-SIN-PONDERADOR"] = n_sin_pond
    out["RESULT-ENVIPE-DEN-N-SIN-DISENO"] = n_sin_dis
    if not u1:
        return para("NO-ESTIMABLE-UNIVERSO-VACIO")

    cod1 = np.array([r["cod"] for r in u1])
    w1 = np.array([r["w"] for r in u1], dtype=float)
    e1 = np.array([r["e"] for r in u1])
    m1 = np.array([r["u"] for r in u1])
    masa1 = float(np.sum(w1))
    out["RESULT-ENVIPE-DEN-MASA-FAC-DEL-U1"] = _num(masa1)
    if masa1 <= 0:
        return para("NO-ESTIMABLE-COLUMNA-VACIA:FAC_DEL")

    d_c1 = np.isin(cod1, list(C1_UNO)).astype(float)
    d_c2 = np.isin(cod1, list(C2_UNO)).astype(float)
    d_comp = np.isin(cod1, list(C2_CERO)).astype(float)

    p_c1, _ = _p_ponderada(d_c1, w1)
    p_c2, _ = _p_ponderada(d_c2, w1)
    p_comp, _ = _p_ponderada(d_comp, w1)
    out["RESULT-ENVIPE-DEN-P-C1-U1"] = _num(p_c1)
    out["RESULT-ENVIPE-DEN-P-C2-U1"] = _num(p_c2)
    out["RESULT-ENVIPE-DEN-P-COMPLEMENTO-C2-U1"] = _num(p_comp)
    out["RESULT-ENVIPE-DEN-DELTA-C2-C1"] = _num(p_c2 - p_c1)
    suma = p_c2 + p_comp
    out["RESULT-ENVIPE-DEN-SUMA-C2-U1"] = _num(suma)

    # ── diseno e IC ───────────────────────────────────────────────────────
    if n_sin_dis == len(u1):
        out["RESULT-ENVIPE-DEN-METODO-IC"] = "NO-ESTIMABLE-DISENO-INCOMPLETO"
        lo1 = hi1 = lo2 = hi2 = None
        n_est = n_upm = n_una = 0
    else:
        lo1, hi1, n_una, n_est, n_upm = _ic_bootstrap(
            d_c1, w1, e1, m1, replicas, semilla)
        lo2, hi2, _, _, _ = _ic_bootstrap(d_c2, w1, e1, m1, replicas, semilla)
        out["RESULT-ENVIPE-DEN-METODO-IC"] = (
            "IC-CON-ESTRATOS-DE-UPM-UNICA" if n_una > 0
            else "IC-BOOTSTRAP-UPM-EN-ESTRATO")
    out["RESULT-ENVIPE-DEN-IC-LO-C1-U1"] = _num(lo1)
    out["RESULT-ENVIPE-DEN-IC-HI-C1-U1"] = _num(hi1)
    out["RESULT-ENVIPE-DEN-IC-LO-C2-U1"] = _num(lo2)
    out["RESULT-ENVIPE-DEN-IC-HI-C2-U1"] = _num(hi2)
    out["RESULT-ENVIPE-DEN-N-ESTRATOS-U1"] = int(n_est)
    out["RESULT-ENVIPE-DEN-N-UPM-U1"] = int(n_upm)
    out["RESULT-ENVIPE-DEN-N-ESTRATOS-UPM-UNICA-U1"] = int(n_una)

    # ── U3: descomposicion del universo completo ──────────────────────────
    cod3 = np.array([r["cod"] for r in u3])
    w3 = np.array([r["w"] for r in u3], dtype=float)
    p_c2_u3, _ = _p_ponderada(np.isin(cod3, list(C2_UNO)).astype(float), w3)
    p_otra_u3, _ = _p_ponderada((cod3 == COD_OTRA).astype(float), w3)
    p_nsnr_u3, _ = _p_ponderada((cod3 == COD_NSNR).astype(float), w3)
    out["RESULT-ENVIPE-DEN-P-C2-U3"] = _num(p_c2_u3)
    out["RESULT-ENVIPE-DEN-P-OTRA-U3"] = _num(p_otra_u3)
    out["RESULT-ENVIPE-DEN-P-NSNR-U3"] = _num(p_nsnr_u3)

    # ── veredicto de exhaustividad (§6.2 de la sellada) ───────────────────
    if abs(suma - 1.0) > 1.0e-9:
        out["RESULT-ENVIPE-DEN-VEREDICTO-EXHAUSTIVIDAD"] = "NO-EXHAUSTIVAS"
    elif (n_otra + n_nsnr + n_blanco) > 0:
        out["RESULT-ENVIPE-DEN-VEREDICTO-EXHAUSTIVIDAD"] = \
            "EXHAUSTIVAS-Y-EXCLUYENTES-SOLO-BAJO-U1"
    else:
        out["RESULT-ENVIPE-DEN-VEREDICTO-EXHAUSTIVIDAD"] = \
            "EXHAUSTIVAS-EN-EL-UNIVERSO-COMPLETO"

    # ── U4: unidad persona, regla de colapso GEN1 verbatim ────────────────
    por_persona_c1, por_persona_c2 = {}, {}
    for r in u1:
        pid = r["id_per"]
        por_persona_c1[pid] = max(por_persona_c1.get(pid, 0),
                                  1 if r["cod"] in C1_UNO else 0)
        por_persona_c2[pid] = max(por_persona_c2.get(pid, 0),
                                  1 if r["cod"] in C2_UNO else 0)
    filas_per = []
    for f in per:
        pid = f["ID_PER"]
        if pid not in por_persona_c2:
            continue
        w = _flotante(f["FAC_ELE"])
        if w is None or w <= 0:
            continue
        filas_per.append({"pid": pid, "w": w,
                          "e": str(f["EST_DIS"]).strip(),
                          "u": str(f["UPM_DIS"]).strip(),
                          "d1": por_persona_c1[pid],
                          "d2": por_persona_c2[pid]})
    out["RESULT-ENVIPE-DEN-N-PERSONAS-U4"] = len(filas_per)
    if filas_per:
        w4 = np.array([r["w"] for r in filas_per], dtype=float)
        d4_1 = np.array([r["d1"] for r in filas_per], dtype=float)
        d4_2 = np.array([r["d2"] for r in filas_per], dtype=float)
        e4 = np.array([r["e"] for r in filas_per])
        m4 = np.array([r["u"] for r in filas_per])
        p4_1, masa4 = _p_ponderada(d4_1, w4)
        p4_2, _ = _p_ponderada(d4_2, w4)
        out["RESULT-ENVIPE-DEN-MASA-FAC-ELE-U4"] = _num(masa4)
        out["RESULT-ENVIPE-DEN-P-C1-U4"] = _num(p4_1)
        out["RESULT-ENVIPE-DEN-P-C2-U4"] = _num(p4_2)
        lo4, hi4, _, _, _ = _ic_bootstrap(d4_2, w4, e4, m4, replicas, semilla)
        out["RESULT-ENVIPE-DEN-IC-LO-C2-U4"] = _num(lo4)
        out["RESULT-ENVIPE-DEN-IC-HI-C2-U4"] = _num(hi4)

        # ── control positivo externo (§6.1) ───────────────────────────────
        delta = p4_2 - p_gen1
        out["RESULT-ENVIPE-DEN-DELTA-VS-GEN1"] = _num(delta)
        out["RESULT-ENVIPE-DEN-REPRODUCE-GEN1"] = (
            "REPRODUCE" if abs(delta) <= tol_replica else "NO-REPRODUCE")

        # ── adopcion P3 (§5 bloque H) ─────────────────────────────────────
        delta_grano = round(p4_2, grano) - p_gen1
        out["RESULT-ENVIPE-DEN-ADOPCION-P3-DELTA"] = _num(delta_grano)
        if abs(delta) > tol_replica:
            out["RESULT-ENVIPE-DEN-ADOPCION-P3"] = "NO-ADOPTABLE-POR-DISCREPANCIA"
        elif abs(delta_grano) > 0:
            out["RESULT-ENVIPE-DEN-ADOPCION-P3"] = "NO-ADOPTABLE-POR-GRANO"
        else:
            out["RESULT-ENVIPE-DEN-ADOPCION-P3"] = "ADOPTABLE-POR-REPLICA"
    else:
        out["RESULT-ENVIPE-DEN-REPRODUCE-GEN1"] = "NO-COMPARABLE"
        out["RESULT-ENVIPE-DEN-ADOPCION-P3"] = "NO-ADOPTABLE-NO-ESTIMABLE"

    out["RESULT-ENVIPE-DEN-VEREDICTO"] = "TASA-REPORTADA"
    return out
