"""`CALC-R-<celda>` — el árbitro `R` de una celda ENVIPE del marco `M`.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO EN EL COMMIT-1 DE `ACTO GEN2-R-SERIE-CSV`, ANTES DE
LEER UN SOLO BYTE DE MICRODATO. Spec sellada que lo gobierna:
`forense/prereg-caja/R-ENVIPE-SERIE-spec-v1_0.md`
(`prereg-caja-R-ENVIPE-SERIE`, sha `b9a29cf6…`).

Este archivo es BYTE-IDENTICO en los tres `CALC-R-CIV-M-{10,12,13}`: todo lo
especifico de la ola (miembro del ZIP, id de payload, codigos) entra por
`contrato["parametros"]`. Que los tres `script_blob_sha256` coincidan en los
tres `sello.json` es la prueba de que las tres olas corrieron el mismo codigo
(spec sellada, 5.3).

Lo unico abierto al escribir este archivo: el manifiesto, los tres
`diccionario_de_datos/*`, los tres `catalogos/*`, los tres `metadatos/*.txt`,
la lista de miembros de los tres ZIP, los tres `cuest_modulo_envipe20NN.pdf` y
`data/inventario-reactivos-v1_2.tsv`. NINGUN `conjunto_de_datos/*.csv`.

NO abre `tools/arbitra.py` ni los JSON de `forense/prereg-duelo-v2/corridas-R/`:
el control positivo contra GEN1 lo corre un script aparte DESPUES de sellar
(spec sellada, 6.1). Este medidor no recibe el valor GEN1 por ninguna via.
"""
from __future__ import annotations

import csv
import io
import sys
import zipfile
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "tests"))
from svystat import prop_ultimate_cluster  # noqa: E402  -- varianza SELLADA, no se reimplementa

SEP = "␟"   # separador de llave compuesta: no aparece en el dato


# ── utilidades ────────────────────────────────────────────────────────────

def _norm(col: str) -> str:
    """Los CSV de INEGI vienen con BOM segun la ola; el nombre de columna se
    normaliza a mayusculas sin BOM ni espacios."""
    return col.lstrip("﻿").lstrip("ï»¿").strip().upper()


def _texto(crudo: bytes) -> str:
    """UTF-8 y, si no, latin-1 -- POR ARCHIVO. Un `.zip` de INEGI mezcla las
    dos codificaciones entre catalogos y microdato, y entre olas: 2021 y 2023
    traen el catalogo en latin-1 y 2024 en UTF-8. Una codificacion fija para
    el ZIP entero convierte un acento en un fallo."""
    try:
        return crudo.decode("utf-8")
    except UnicodeDecodeError:
        return crudo.decode("latin-1")


def _codigo(s):
    """`BP1_23`/`BPCOD`/`BP1_20` -> entero, o None si blanco / no numerico.

    El descriptor declara `BP1_23` como Numerico(2) con claves `01..09`, `99`
    y (en 2023/2024) `b`. En el CSV eso puede venir con o sin cero a la
    izquierda, vacio, o con la letra `b`. Ninguna de esas formas se imputa a
    un codigo: lo que no es un entero es BLANCO y se cuenta aparte."""
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
    """(filas, faltantes). `filas` son dicts con SOLO las columnas pedidas, en
    el orden del archivo -- las sumas van en orden fijo de fila."""
    texto = _texto(zf.read(miembro))
    lector = csv.reader(io.StringIO(texto, newline=""))
    cabecera = [_norm(c) for c in next(lector)]
    idx, faltantes = {}, []
    for c in columnas:
        if c in cabecera:
            idx[c] = cabecera.index(c)
        else:
            faltantes.append(c)
    filas = []
    ancho = len(cabecera)
    if not faltantes:
        for fila in lector:
            if len(fila) < ancho:
                fila = fila + [""] * (ancho - len(fila))
            filas.append({c: fila[i] for c, i in idx.items()})
    else:
        for _fila in lector:          # se cuentan igual: el negativo declara universo
            filas.append({})
    return filas, faltantes


def _p_ponderada(w, d):
    sw = float(np.sum(w))
    if sw <= 0:
        return None, sw
    return float(np.sum(w * d) / sw), sw


def _ic_bootstrap(d, w, estrato, upm, replicas, semilla):
    """Bootstrap de UPM CON REEMPLAZO dentro de estrato, conservando el numero
    de UPM por estrato; percentiles 2.5/97.5. Es el metodo con el que la ola
    2025 fijo su IC (`prereg-caja-ENVIPE-DENUNCIA` 3.4) y se replica aqui para
    que la columna de IC de la serie sea homogenea con ese punto.

    Un estrato con UNA sola UPM se re-muestrea a si mismo: aporta varianza
    cero, no se colapsa ni se descarta."""
    if len(d) == 0:
        return None, None
    rng = np.random.Generator(np.random.PCG64(semilla))
    wd = w * d
    claves = np.array([f"{e}{SEP}{u}" for e, u in zip(estrato, upm)])
    upm_unicas, inverso = np.unique(claves, return_inverse=True)
    sw_upm = np.bincount(inverso, weights=w, minlength=len(upm_unicas))
    swd_upm = np.bincount(inverso, weights=wd, minlength=len(upm_unicas))
    estr_de_upm = np.array([k.split(SEP)[0] for k in upm_unicas])
    acc_sw = np.zeros(replicas, dtype=float)
    acc_swd = np.zeros(replicas, dtype=float)
    for e in np.unique(estr_de_upm):          # orden fijo: np.unique ordena
        pos = np.flatnonzero(estr_de_upm == e)
        k = len(pos)
        if k == 1:
            acc_sw += sw_upm[pos[0]]
            acc_swd += swd_upm[pos[0]]
            continue
        elegidas = rng.integers(0, k, size=(replicas, k))
        acc_sw += sw_upm[pos][elegidas].sum(axis=1)
        acc_swd += swd_upm[pos][elegidas].sum(axis=1)
    validas = acc_sw > 0
    if not validas.any():
        return None, None
    ps = acc_swd[validas] / acc_sw[validas]
    return float(np.percentile(ps, 2.5)), float(np.percentile(ps, 97.5))


def _perfil_diseno(regs):
    """El descriptor de INEGI ya mintio sobre la longitud de EST_DIS/UPM_DIS
    en la ola 2025. Esto mide el perfil REAL sobre el universo, para que la
    discrepancia quede medida y no supuesta (spec sellada, 3.4)."""
    def perfil(campo):
        cuenta = {}
        bordes = 0
        for r in regs:
            v = r[campo]
            cuenta[len(v)] = cuenta.get(len(v), 0) + 1
            if v != v.strip():
                bordes += 1
        piezas = ";".join(f"len{k}={cuenta[k]}" for k in sorted(cuenta))
        return f"{piezas};bordes_con_espacio={bordes}"
    return f"EST_DIS[{perfil('e')}] UPM_DIS[{perfil('u')}]"


# ── medidor ───────────────────────────────────────────────────────────────

def medir(inputs, contrato):
    par = contrato["parametros"]
    celda = str(par["id_celda"])
    P = f"RESULT-R-{celda}-"
    miembro = str(par["tabla_miembro"])
    zip_id = str(par["payload_id"])
    replicas = int(par["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    umbral_cv = float(par["umbral_cv_skip"])

    cod = par["codificacion"]
    CR_UNO = {int(c) for c in cod["CR_uno"]}
    CR_CERO = {int(c) for c in cod["CR_cero"]}
    UR = CR_UNO | CR_CERO
    C1_UNO = {int(c) for c in cod["C1_uno"]}
    C1_CERO = {int(c) for c in cod["C1_cero"]}
    C2_UNO = {int(c) for c in cod["C2_uno"]}
    C2_CERO = {int(c) for c in cod["C2_cero"]}
    U1 = C1_UNO | C1_CERO
    PERSONALES = {int(c) for c in cod["bpcod_personales"]}
    HOGAR = {int(c) for c in cod["bpcod_hogar"]}
    COD_NSNR = int(cod["codigo_nsnr"])
    COLS = list(par["columnas"])

    ids = [P + s for s in par["sufijos_result"]]
    out = {k: None for k in ids}
    for s in ("N-FILAS-TABLA", "N-BP1-23-01-09", "N-BP1-23-99", "N-BP1-23-BLANCO",
              "N-SIN-PONDERADOR", "N-SIN-DISENO", "N-INCONSISTENTES-BP1-20",
              "N-CODIGO-FUERA-DE-CATALOGO", "N-BPCOD-01-04", "N-BPCOD-05-15",
              "N", "N-ESTRATOS", "N-UPM",
              "N-ESTRATOS-UPM-UNICA", "N-U1", "N-ESTRATOS-UPM-UNICA-U1"):
        out[P + s] = 0
    for s in ("METODO-IC", "PERFIL-DISENO", "VEREDICTO-CV"):
        out[P + s] = "NO-ESTIMABLE"
    out[P + "ESTADO"] = "NO-ESTIMABLE"

    def para(estado):
        out[P + "ESTADO"] = estado
        return out

    zf = zipfile.ZipFile(inputs[zip_id]["ruta_absoluta"])
    filas, faltan = _lee_tabla(zf, miembro, COLS)
    out[P + "N-FILAS-TABLA"] = len(filas)
    if faltan:
        return para("NO-ESTIMABLE-COLUMNA-AUSENTE:" + ",".join(faltan))

    # ── embudo, contando antes y despues de cada filtro ───────────────────
    n_blanco = n_nsnr = n_sin_pond = n_incons = 0
    n_cod_01_09 = n_fuera_cat = 0
    ur, u1 = [], []
    for f in filas:
        cod23 = _codigo(f["BP1_23"])
        if cod23 is None:
            n_blanco += 1
            continue
        if cod23 == COD_NSNR:
            n_nsnr += 1
            continue
        if cod23 not in UR:
            n_fuera_cat += 1               # codigo que el catalogo de la ola no declara
            continue
        n_cod_01_09 += 1
        if _codigo(f["BP1_20"]) != 2:
            n_incons += 1
        w = _flotante(f["FAC_DEL"])
        if w is None or w <= 0:
            n_sin_pond += 1
            continue
        reg = {"cod": cod23, "w": w,
               "e": str(f["EST_DIS"]).strip(), "u": str(f["UPM_DIS"]).strip(),
               "bpcod": _codigo(f["BPCOD"])}
        ur.append(reg)
        if (reg["bpcod"] in PERSONALES and _codigo(f["BP1_20"]) == 2
                and cod23 in U1):
            u1.append(reg)

    out[P + "N-BP1-23-01-09"] = n_cod_01_09
    out[P + "N-BP1-23-99"] = n_nsnr
    out[P + "N-BP1-23-BLANCO"] = n_blanco
    out[P + "N-SIN-PONDERADOR"] = n_sin_pond
    out[P + "N-CODIGO-FUERA-DE-CATALOGO"] = n_fuera_cat
    out[P + "N-INCONSISTENTES-BP1-20"] = n_incons
    out[P + "N"] = len(ur)
    out[P + "N-U1"] = len(u1)
    out[P + "N-BPCOD-01-04"] = sum(1 for r in ur if r["bpcod"] in HOGAR)
    out[P + "N-BPCOD-05-15"] = sum(1 for r in ur if r["bpcod"] in PERSONALES)
    out[P + "N-SIN-DISENO"] = sum(1 for r in ur if not r["e"] or not r["u"])

    if n_cod_01_09 == 0 and n_nsnr == 0:
        return para("NO-ESTIMABLE-COLUMNA-VACIA:BP1_23")
    if not ur:
        return para("NO-ESTIMABLE-UNIVERSO-VACIO")

    out[P + "PERFIL-DISENO"] = _perfil_diseno(ur)

    # ── estimando PRIMARIO: el arbitro R ──────────────────────────────────
    w = np.array([r["w"] for r in ur], dtype=float)
    d = np.array([1.0 if r["cod"] in CR_UNO else 0.0 for r in ur], dtype=float)
    est = [r["e"] for r in ur]
    upm = [r["u"] for r in ur]

    punto, masa = _p_ponderada(w, d)
    out[P + "MASA-FAC-DEL"] = masa
    out[P + "PUNTO"] = punto

    uc = prop_ultimate_cluster(zip(est, upm, w.tolist(), d.tolist()))
    if uc is None:
        out[P + "METODO-IC"] = "NO-ESTIMABLE-DISENO-INCOMPLETO"
    else:
        out[P + "EE"] = uc["se"]
        out[P + "IC-LO"] = uc["ic95"][0]
        out[P + "IC-HI"] = uc["ic95"][1]
        out[P + "N-ESTRATOS"] = uc["n_estratos"]
        out[P + "N-UPM"] = uc["n_upm_total"]
        out[P + "N-ESTRATOS-UPM-UNICA"] = uc["n_estratos_singleton"]
        out[P + "METODO-IC"] = ("IC-CON-ESTRATOS-DE-UPM-UNICA"
                                if uc["n_estratos_singleton"] > 0
                                else "IC-ULTIMATE-CLUSTER")
        if punto and punto > 0:
            cv = uc["se"] / punto
            out[P + "CV"] = cv
            out[P + "VEREDICTO-CV"] = ("SKIP-POR-CV" if cv >= umbral_cv
                                       else "CV-ACEPTABLE")

    # ── estimando SECUNDARIO homologado a la ola 2025 (U1 / C1 y C2) ──────
    if u1:
        w1 = np.array([r["w"] for r in u1], dtype=float)
        d1 = np.array([1.0 if r["cod"] in C1_UNO else 0.0 for r in u1], dtype=float)
        d2 = np.array([1.0 if r["cod"] in C2_UNO else 0.0 for r in u1], dtype=float)
        e1 = [r["e"] for r in u1]
        u1u = [r["u"] for r in u1]

        p1, masa1 = _p_ponderada(w1, d1)
        p2, _ = _p_ponderada(w1, d2)
        out[P + "MASA-FAC-DEL-U1"] = masa1
        out[P + "P-C1-U1"] = p1
        out[P + "P-C2-U1"] = p2
        if p1 is not None and p2 is not None:
            out[P + "DELTA-C2-C1"] = p2 - p1

        uc1 = prop_ultimate_cluster(zip(e1, u1u, w1.tolist(), d1.tolist()))
        if uc1 is not None:
            out[P + "EE-C1-U1"] = uc1["se"]
            out[P + "IC-LO-C1-U1"] = uc1["ic95"][0]
            out[P + "IC-HI-C1-U1"] = uc1["ic95"][1]
            out[P + "N-ESTRATOS-UPM-UNICA-U1"] = uc1["n_estratos_singleton"]
        uc2 = prop_ultimate_cluster(zip(e1, u1u, w1.tolist(), d2.tolist()))
        if uc2 is not None:
            out[P + "EE-C2-U1"] = uc2["se"]

        lo, hi = _ic_bootstrap(d1, w1, e1, u1u, replicas, semilla)
        out[P + "IC-BOOT-LO-C1-U1"] = lo
        out[P + "IC-BOOT-HI-C1-U1"] = hi
        lo2, hi2 = _ic_bootstrap(d2, w1, e1, u1u, replicas, semilla)
        out[P + "IC-BOOT-LO-C2-U1"] = lo2
        out[P + "IC-BOOT-HI-C2-U1"] = hi2

    return para("CALCULADO")
