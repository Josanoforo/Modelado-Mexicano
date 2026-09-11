"""Medidor sucesor de la serie ENVIPE de razones de no denuncia, olas 2011–2022.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

Se congela antes del primer resultado de `ACTO GEN2-ENVIPE-SERIE-COMPLETA`.
Lo gobierna `prereg-caja-ENVIPE-SERIE-COMPLETA-v1_0`, sucesora por extensión
de las familias CSV/DBF históricas, que no se editan.

El mismo archivo se deposita byte a byte en los ocho CALC. Formato, miembro,
variables físicas, códigos y año entran por `contrato["parametros"]`.

Lee DBF desde su cabecera y CSV con normalización de BOM. No colapsa delitos a
personas, no interpola olas y no recibe ningún resultado histórico como entrada.
"""
from __future__ import annotations

import csv
import io
import struct
import sys
import zipfile
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "tests"))
from svystat import prop_ultimate_cluster  # noqa: E402  -- varianza SELLADA, no se reimplementa

SEP = "␟"   # separador de llave compuesta: no aparece en el dato

ACTIVO = 0x20      # marca de registro vivo en DBF
BORRADO = 0x2A     # '*' -- registro marcado como borrado


def _norm(col: str) -> str:
    return col.lstrip("﻿").lstrip("ï»¿").strip().upper()


def _texto(crudo: bytes) -> str:
    try:
        return crudo.decode("utf-8")
    except UnicodeDecodeError:
        return crudo.decode("latin-1")


def _lee_csv(crudo: bytes, columnas: list[str]):
    lector = csv.reader(io.StringIO(_texto(crudo), newline=""))
    cabecera = [_norm(c) for c in next(lector)]
    idx = {c: cabecera.index(c) for c in columnas if c in cabecera}
    faltantes = [c for c in columnas if c not in idx]
    filas = []
    ancho = len(cabecera)
    for fila in lector:
        if len(fila) < ancho:
            fila += [""] * (ancho - len(fila))
        filas.append({c: fila[i] for c, i in idx.items()} if not faltantes else {})
    perfil = f"csv;columnas={ancho};n_leidos={len(filas)}"
    return filas, faltantes, perfil


# ── lector DBF ────────────────────────────────────────────────────────────

def _lee_dbf(crudo: bytes, columnas: list[str]):
    """(filas, faltantes, perfil). Lee un DBF de ancho fijo desde bytes.

    El ancho y el orden de los campos salen del DESCRIPTOR DEL ARCHIVO, no del
    FD ni de una plantilla: un `.dbf` declara sus 32 bytes de cabecera y un
    descriptor de 32 bytes por campo, y esa es la autoridad.

    Todo valor se devuelve como TEXTO decodificado en latin-1 y sin recortar.
    latin-1 es total sobre bytes (no puede fallar) y preserva la longitud en
    caracteres: para llaves opacas como el estrato y la UPM eso es exactamente
    lo que se necesita, porque cualquier decodificacion multibyte cambiaria el
    ancho y podria fundir dos llaves distintas en una.

    Los registros marcados como BORRADOS (`*` en el primer byte) NO entran y se
    cuentan aparte: son parte del perfil, no del universo.
    """
    nrec, hlen, rlen = struct.unpack("<IHH", crudo[4:12])
    codepage = crudo[29]
    campos, pos = [], 32
    desplazamiento = 1                      # el byte 0 de cada registro es la marca
    while pos + 32 <= hlen and crudo[pos] != 0x0D:
        b = crudo[pos:pos + 32]
        nombre = b[0:11].split(b"\x00")[0].decode("latin-1").strip().upper()
        largo = b[16]
        campos.append((nombre, desplazamiento, largo))
        desplazamiento += largo
        pos += 32

    mapa = {n: (o, l) for n, o, l in campos}
    faltantes = [c for c in columnas if c not in mapa]
    perfil = (f"nrec_cabecera={nrec};rlen={rlen};hlen={hlen};"
              f"n_campos={len(campos)};codepage=0x{codepage:02x}")
    if faltantes:
        return [], faltantes, perfil

    filas, borrados, truncados = [], 0, 0
    inicio = hlen
    for i in range(nrec):
        a = inicio + i * rlen
        reg = crudo[a:a + rlen]
        if len(reg) < rlen:
            truncados += 1
            break
        marca = reg[0]
        if marca == BORRADO:
            borrados += 1
            continue
        filas.append({c: reg[mapa[c][0]:mapa[c][0] + mapa[c][1]].decode("latin-1")
                      for c in columnas})
    perfil += f";registros_borrados={borrados};registros_truncados={truncados};n_leidos={len(filas)}"
    return filas, [], perfil


# ── utilidades ────────────────────────────────────────────────────────────

def _codigo(s):
    """Texto de un campo DBF -> entero, o None si blanco / no numerico.

    En DBF los codigos numericos vienen rellenos con espacios a la izquierda o
    a la derecha segun el capturista, y el blanco es un campo de puros
    espacios. Nada de eso se imputa: lo que no es entero es BLANCO."""
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


def _p_ponderada(w, d):
    sw = float(np.sum(w))
    if sw <= 0:
        return None, sw
    return float(np.sum(w * d) / sw), sw


def _ic_bootstrap(d, w, estrato, upm, replicas, semilla):
    """Bootstrap de UPM CON REEMPLAZO dentro de estrato, conservando el numero
    de UPM por estrato; percentiles 2.5/97.5. Mismo metodo, misma semilla y
    mismo numero de replicas que fijaron el IC de la ola 2025 y el del trio
    CSV, para que la columna de IC de la serie sea homogenea en los trece
    puntos y no en cuatro.

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
    """Perfil REAL de las llaves opacas sobre el universo. El descriptor de
    INEGI ya mintio sobre la longitud de EST_DIS/UPM_DIS en la ola 2025; aqui
    ademas cambian de NOMBRE entre olas. Se mide, no se supone."""
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
    return f"ESTRATO[{perfil('e')}] UPM[{perfil('u')}]"


def _perfil_bpcod(filas, col_bpcod):
    """Distribucion de BPCOD codigo por codigo, ANTES de todo filtro.

    Es reporte ESTRUCTURAL, no estimacion: no lleva ponderador y no entra en
    ningun estimando. Existe porque el catalogo de BPCOD de 2012 esta corrido
    un lugar frente a 2013/2015, y si el corrimiento declarado en la spec
    estuviera mal, la forma de esta distribucion lo delata sin tocar el punto."""
    cuenta = {}
    for f in filas:
        c = _codigo(f[col_bpcod])
        k = "blanco" if c is None else f"{c:02d}"
        cuenta[k] = cuenta.get(k, 0) + 1
    return ";".join(f"{k}={cuenta[k]}" for k in sorted(cuenta))


# ── medidor ───────────────────────────────────────────────────────────────

def medir(inputs, contrato):
    par = contrato["parametros"]
    ola = str(par["ola_encuesta"])
    P = f"RESULT-ENVIPE-SERIE-{ola}-"
    miembro = str(par["tabla_miembro"])
    zip_id = str(par["payload_id"])
    replicas = int(par["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    umbral_cv = float(par["umbral_cv_skip"])

    # vinculo ROL -> NOMBRE FISICO, declarado por ola en el spec.yaml
    m = par["mapa_columnas"]
    C_BP1_23 = str(m["BP1_23"])
    C_BP1_20 = str(m["BP1_20"])
    C_BPCOD = str(m["BPCOD"])
    C_FAC = str(m["FAC_DEL"])
    C_EST = str(m["ESTRATO"])
    C_UPM = str(m["UPM"])

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
    COD_EXCLUIDOS = {int(c) for c in cod["codigos_nsnr"]}
    COLS = [C_BP1_23, C_BP1_20, C_BPCOD, C_FAC, C_EST, C_UPM]

    ids = [P + s for s in par["sufijos_result"]]
    out = {k: None for k in ids}
    for s in ("N-FILAS-TABLA", "N-RESPUESTA-01-09", "N-NSNR", "N-BLANCO",
              "N-SIN-PONDERADOR", "N-SIN-DISENO", "N-INCONSISTENTES-BP1-20",
              "N-CODIGO-FUERA-DE-CATALOGO", "N-BPCOD-HOGAR", "N-BPCOD-PERSONALES",
              "N", "N-ESTRATOS", "N-UPM",
              "N-ESTRATOS-UPM-UNICA", "N-U1", "N-ESTRATOS-UPM-UNICA-U1"):
        out[P + s] = 0
    for s in ("METODO-IC", "PERFIL-DISENO", "PERFIL-LECTURA", "PERFIL-BPCOD", "VEREDICTO-CV"):
        out[P + s] = "NO-ESTIMABLE"
    out[P + "ESTADO"] = "NO-ESTIMABLE"

    def para(estado):
        out[P + "ESTADO"] = estado
        return out

    zf = zipfile.ZipFile(inputs[zip_id]["ruta_absoluta"])
    lector = _lee_csv if str(par["formato"]).upper() == "CSV" else _lee_dbf
    filas, faltan, perfil_dbf = lector(zf.read(miembro), COLS)
    out[P + "PERFIL-LECTURA"] = perfil_dbf
    out[P + "N-FILAS-TABLA"] = len(filas)
    if faltan:
        return para("NO-ESTIMABLE-COLUMNA-AUSENTE:" + ",".join(faltan))

    out[P + "PERFIL-BPCOD"] = _perfil_bpcod(filas, C_BPCOD)

    # ── embudo, contando antes y despues de cada filtro ───────────────────
    n_blanco = n_nsnr = n_sin_pond = n_incons = 0
    n_cod_01_09 = n_fuera_cat = 0
    ur, u1 = [], []
    for f in filas:
        cod23 = _codigo(f[C_BP1_23])
        if cod23 is None:
            n_blanco += 1
            continue
        if cod23 in COD_EXCLUIDOS:
            n_nsnr += 1
            continue
        if cod23 not in UR:
            n_fuera_cat += 1               # codigo que el catalogo de la ola no declara
            continue
        n_cod_01_09 += 1
        if _codigo(f[C_BP1_20]) != 2:
            n_incons += 1
        w = _flotante(f[C_FAC])
        if w is None or w <= 0:
            n_sin_pond += 1
            continue
        reg = {"cod": cod23, "w": w,
               "e": str(f[C_EST]).strip(), "u": str(f[C_UPM]).strip(),
               "bpcod": _codigo(f[C_BPCOD])}
        ur.append(reg)
        if (reg["bpcod"] in PERSONALES and _codigo(f[C_BP1_20]) == 2
                and cod23 in U1):
            u1.append(reg)

    out[P + "N-RESPUESTA-01-09"] = n_cod_01_09
    out[P + "N-NSNR"] = n_nsnr
    out[P + "N-BLANCO"] = n_blanco
    out[P + "N-SIN-PONDERADOR"] = n_sin_pond
    out[P + "N-CODIGO-FUERA-DE-CATALOGO"] = n_fuera_cat
    out[P + "N-INCONSISTENTES-BP1-20"] = n_incons
    out[P + "N"] = len(ur)
    out[P + "N-U1"] = len(u1)
    out[P + "N-BPCOD-HOGAR"] = sum(1 for r in ur if r["bpcod"] in HOGAR)
    out[P + "N-BPCOD-PERSONALES"] = sum(1 for r in ur if r["bpcod"] in PERSONALES)
    out[P + "N-SIN-DISENO"] = sum(1 for r in ur if not r["e"] or not r["u"])

    if n_cod_01_09 == 0 and n_nsnr == 0:
        return para("NO-ESTIMABLE-COLUMNA-VACIA:" + C_BP1_23)
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
