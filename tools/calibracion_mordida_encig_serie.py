#!/usr/bin/env python3
"""ACTO MAESTRA34-L1 · MORDIDA-SERIE — COMMIT-2, piezas P1 y P2.

P1 · calibra `tramite.mordida.discrecional` contra ENCIG 2025 (payload
encig25_base_datos_csv), misma variable/codificacion que TRA-M-07 (2021):
P8_3_1 (1=Si, 2=No, 9 fuera), ponderador FAC_P18, diseno EST_DIS/UPM_DIS.

P2 · serie historica ENCIG 2011/2015/2019/2023, misma variable en las tres
olas CSV (2015/2019/2023: P8_3_1/EST_DIS/UPM_DIS/FAC_P18, identico a
TRA-M-03/05/07). La ola 2011 es DBF y no trae P8_3_1: la tabla
`03_ENCIG2011_tramites.dbf` pregunta por-tramite (P4_11, "las condiciones
lo llevaron a pagar una mordida o soborno?", 1=Si/2=No), con hasta 29
filas por persona. Para hacerla comparable a la pregunta agregada de
2013+, este script COLAPSA a persona: y_persona=1 si CUALQUIER fila valida
(P4_11 en {1,2}) de esa persona es '1'; se excluye a la persona solo si
TODAS sus filas quedan en blanco (nunca se le hizo la pregunta en ningun
tramite). FAC_P18/EST_DIS/UPM_DIS son constantes dentro de persona
(verificado: 0 de 24820 con inconsistencia) -- se toma el primer valor.

Verificacion cruzada de semantica de variable (contra los diccionarios de
datos embebidos en cada ZIP, no supuesta por nombre): 2017/2019/2021/2023
etiquetan `P8_3_1` como "Practica de corrupcion experimentada: intento de
apropiacion de algun beneficio" -- el PRIMER item de una bateria de tres
(P8_3_1/_2/_3: apropiacion / solicitud por tercero-coyote / insinuacion de
condiciones), idem TRA-M-05/07. **2015 rompe el patron**: su diccionario
declara `P8_3` (sin sufijo) como el Si/No de "intento de apropiacion" y
`P8_3_1` como el CONTEO de tramites (numerico, 2 digitos) -- por eso
"P8_3_1" en 2015 trae valores como "01".."44", no "1"/"2", y el script usa
`P8_3` para esa ola (mismo patron que TRA-M-03/2013 en
codificacion-R-v1_0.tsv, que tambien usa `P8_3` pelado). 2025 no trae
diccionario propio en el ZIP (solo CSVs planos): se asume misma semantica
que 2017-2023 por continuidad estructural (mismas 3 columnas P8_3_1/_2/_3,
mismo layout de tabla sec1_A_3_4_5_8_9_10) -- verificado por estructura,
NO por diccionario propio; declarado como tal en el hallazgo de P1.

Formato CSV 2015/2019/2023: las filas usan CR (`\\r`) suelto como
terminador de registro Y ademas cada campo trae un `\\r` embebido antes de
su comilla de cierre (defecto de exportacion de INEGI, ya presente en el
payload de TRA-M-07/2021, que usa el mismo formato). `csv.reader` sobre un
`StringIO` con `newline=''` lo parsea correctamente porque el modulo csv
reconoce cualquier CR/LF fuera de comillas como fin de registro y trata el
CR dentro de comillas como contenido literal; se limpia con `.rstrip("\\r")`
por campo despues.

IC95 por bootstrap por conglomerado estratificado (remuestreo de UPMs con
reemplazo dentro de estrato, 10000 replicas, seed 42) -- mismo estimador
que `tools/tasas_base_ola6_activos.py::wprop_ic_conglomerado` (ACTO
MAESTRA32-E16 / MAESTRA33-E18-P3). "El primer resultado que produzca este
procedimiento es el que se reporta": una sola corrida, sin reintentos.

Este script solo IMPRIME. Quien ejecuta el acto pega el resultado en
milpa/tramite-ola5-propuesta-v0.yaml.

Uso: python3 tools/calibracion_mordida_encig_serie.py
"""
import csv
import hashlib
import io
import os
import tempfile
import zipfile

import numpy as np
import pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RAIZ, "data", "raw")
SEED = 42
N_BOOT = 10000
CHUNK = 500


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def wprop_ic_conglomerado(d, w, estrato, upm, n_boot=N_BOOT, seed=SEED):
    """Idéntica a tools/tasas_base_ola6_activos.py (verbatim, mismo estimador)."""
    d = np.asarray(d, dtype=float)
    w = np.asarray(w, dtype=float)
    p_hat = float((w * d).sum() / w.sum())

    llave = pd.Series(
        [f"{e}\x1f{u}" for e, u in zip(estrato, upm)], dtype="object")
    cl_id, _ = pd.factorize(llave)
    n_cl = cl_id.max() + 1
    sw = np.bincount(cl_id, weights=w, minlength=n_cl)
    swd = np.bincount(cl_id, weights=w * d, minlength=n_cl)
    est_de_cl = pd.Series(list(estrato)).groupby(cl_id).first().to_numpy()
    orden = np.argsort(pd.factorize(pd.Series(est_de_cl))[0], kind="stable")
    sw, swd = sw[orden], swd[orden]
    est_ord = pd.factorize(pd.Series(est_de_cl[orden]))[0]

    tam_est = np.bincount(est_ord)
    inicio_est = np.concatenate([[0], np.cumsum(tam_est)[:-1]])
    inicio = inicio_est[est_ord].astype(np.int64)
    tam = tam_est[est_ord].astype(np.int64)

    rng = np.random.default_rng(seed)
    boots = np.empty(n_boot, dtype=float)
    hecho = 0
    while hecho < n_boot:
        b = min(CHUNK, n_boot - hecho)
        idx = inicio + (rng.random((b, len(sw))) * tam).astype(np.int64)
        boots[hecho:hecho + b] = swd[idx].sum(axis=1) / sw[idx].sum(axis=1)
        hecho += b
    boots.sort()
    lo = float(boots[int(0.025 * n_boot)])
    hi = float(boots[int(0.975 * n_boot) - 1])
    return p_hat, lo, hi, len(d), int(tam_est.size), int(n_cl)


def leer_csv_cr(zpath, member, encoding="latin-1"):
    """Lector tolerante al formato CR-suelto + CR-embebido de INEGI (ver
    docstring del modulo). Devuelve DataFrame de columnas str, sin CR."""
    with zipfile.ZipFile(zpath) as z:
        raw = z.read(member)
    text = raw.decode(encoding, errors="replace")
    rows = list(csv.reader(io.StringIO(text, newline=""), delimiter=","))
    header = [h.strip().rstrip("\r").lstrip("﻿") for h in rows[0]]
    body = [[c.rstrip("\r") for c in r] for r in rows[1:] if r]
    df = pd.DataFrame(body, columns=header)
    return df


def medir_ola_p8_3_1(zpath, member, ola, payload_id, var_col="P8_3_1",
                      estrato_col="EST_DIS", upm_col="UPM_DIS",
                      pond_col="FAC_P18"):
    sha = sha256(zpath)
    df = leer_csv_cr(zpath, member)
    for col in (var_col, estrato_col, upm_col, pond_col):
        assert col in df.columns, f"{ola}: falta columna {col}"
    n_filas = len(df)
    v = df[var_col].astype(str).str.strip()
    m = v.isin(["1", "2"])
    n_fuera = int((~m).sum())
    d = (v[m] == "1").astype(float).to_numpy()
    w = pd.to_numeric(df.loc[m, pond_col], errors="coerce").to_numpy()
    n_sin_pond = int(pd.isna(w).sum())
    assert n_sin_pond == 0, f"{ola}: {n_sin_pond} filas sin ponderador valido"
    est = df.loc[m, estrato_col].astype(str).to_numpy()
    upm = df.loc[m, upm_col].astype(str).to_numpy()
    p, lo, hi, n, ne, nu = wprop_ic_conglomerado(d, w, est, upm)
    print(f"  ENCIG {ola}: p={p:.6f}  IC95=[{lo:.6f}, {hi:.6f}]  n={n}  "
          f"estratos={ne}  UPM={nu}  n_filas_leidas={n_filas}  "
          f"n_fuera_de_universo(no 1/2)={n_fuera}")
    print(f"             ponderador={pond_col}  sha256={sha}")
    return dict(ola=ola, p=p, ic95=[lo, hi], n=n, n_efectivo=n, estratos=ne,
                upm=nu, ponderador=pond_col, sha256_payload=sha,
                payload_manifiesto_id=payload_id, n_filas_leidas=n_filas,
                n_fuera_de_universo=n_fuera)


def medir_2011_tramites():
    """Colapso a persona sobre 03_ENCIG2011_tramites.dbf::P4_11 (ver docstring)."""
    from dbfread import DBF
    zpath = os.path.join(RAW, "encig2011", "Base_datos_encig2011_dbf.zip")
    sha = sha256(zpath)
    with zipfile.ZipFile(zpath) as z:
        data = z.read("Base de datos/03_ENCIG2011_tramites.dbf")
    tmp = tempfile.NamedTemporaryFile(suffix=".dbf", delete=False)
    try:
        tmp.write(data)
        tmp.close()
        recs = list(DBF(tmp.name, encoding="latin-1",
                         ignore_missing_memofile=True))
    finally:
        os.unlink(tmp.name)

    from collections import defaultdict
    byperson = defaultdict(list)
    for r in recs:
        k = (r["ENT"], r["CON"], r["V_SEL"], r["N_HOG"], r["R_ELE"])
        byperson[k].append(r)

    for k, rows in byperson.items():
        assert len({r["FAC_P18"] for r in rows}) == 1, f"FAC_P18 inconsistente en persona {k}"
        assert len({r["EST_DIS"] for r in rows}) == 1, f"EST_DIS inconsistente en persona {k}"
        assert len({r["UPM_DIS"] for r in rows}) == 1, f"UPM_DIS inconsistente en persona {k}"

    ys, ws, ests, upms = [], [], [], []
    n_excluidas_todo_blanco = 0
    for k, rows in byperson.items():
        vals = [r["P4_11"] for r in rows if r["P4_11"] in ("1", "2")]
        if not vals:
            n_excluidas_todo_blanco += 1
            continue
        ys.append(1.0 if "1" in vals else 0.0)
        ws.append(float(rows[0]["FAC_P18"]))
        ests.append(rows[0]["EST_DIS"])
        upms.append(rows[0]["UPM_DIS"])

    d = np.array(ys)
    w = np.array(ws)
    p, lo, hi, n, ne, nu = wprop_ic_conglomerado(d, w, ests, upms)
    print(f"  ENCIG 2011: p={p:.6f}  IC95=[{lo:.6f}, {hi:.6f}]  n={n}  "
          f"estratos={ne}  UPM={nu}  n_filas_dbf={len(recs)}  "
          f"n_personas_total={len(byperson)}  "
          f"n_excluidas(todo P4_11 en blanco)={n_excluidas_todo_blanco}")
    print(f"             ponderador=FAC_P18  sha256={sha}")
    return dict(ola=2011, p=p, ic95=[lo, hi], n=n, n_efectivo=n, estratos=ne,
                upm=nu, ponderador="FAC_P18", sha256_payload=sha,
                payload_manifiesto_id="encig_2011_base_datos_encig2011_dbf",
                n_filas_leidas=len(recs),
                n_personas_total=len(byperson),
                n_excluidas_todo_blanco=n_excluidas_todo_blanco)


def p1_calibracion_2025():
    print("=" * 72)
    print("P1 · CALIBRACION ENCIG 2025 (tramite.mordida.discrecional)")
    print("=" * 72)
    zpath = os.path.join(RAW, "encig25_base_datos_csv.zip")
    r = medir_ola_p8_3_1(zpath, "encig2025_01_sec1_A_3_4_5_8_9_10.csv",
                         2025, "encig25_base_datos_csv")
    return r


def p2_serie_historica():
    print("=" * 72)
    print("P2 · SERIE HISTORICA ENCIG 2011/2015/2019/2023")
    print("=" * 72)
    out = {}
    out[2011] = medir_2011_tramites()
    out[2015] = medir_ola_p8_3_1(
        os.path.join(RAW, "encig2015_csv.zip"),
        "01_sec1_3_4_5_8_9_10_encig2015/conjunto_de_datos/encig2015_01_sec1_3_4_5_8_9_10.csv",
        2015, "encig2015_csv", var_col="P8_3")
    out[2019] = medir_ola_p8_3_1(
        os.path.join(RAW, "encig2019_csv.zip"),
        "conjunto_de_datos_encig2019_01_sec1_3_4_5_8_9_10/conjunto_de_datos/"
        "conjunto_de_datos_encig2019_01_sec1_3_4_5_8_9_10.csv",
        2019, "encig2019_csv")
    out[2023] = medir_ola_p8_3_1(
        os.path.join(RAW, "encig2023_datosabiertos_csv.zip"),
        "conjunto_de_datos_encig2023_01_sec1_a_3_4_5_8_9_10/conjunto_de_datos/"
        "conjunto_de_datos_encig2023_01_sec1_a_3_4_5_8_9_10.csv",
        2023, "encig2023_datosabiertos_csv")
    return out


if __name__ == "__main__":
    r1 = p1_calibracion_2025()
    print()
    r2 = p2_serie_historica()
