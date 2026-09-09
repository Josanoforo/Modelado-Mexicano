"""`CALC-B-0001` — ENSAYO de la linea base temporal `B` sobre remesas ENIGH 2016-2022.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO EN EL COMMIT-1 DE `ACTO GEN2-C0-B`, ANTES DE LEER UN
SOLO BYTE DE MICRODATO DE ENIGH. Spec sellada que lo gobierna:
`forense/prereg-caja/B-REMESAS-spec-v1_0.md` (`prereg-caja-B-REMESAS`).

NO mide ninguna regla y ninguna cifra suya entra a un veredicto (`T9`).
`R5.1` / `familia.seguro.volatilidad_ausencia_estado` NO se mueve.

El selector `tools/baseline_temporal.py` se ejecuta desde los BYTES que el
snapshot de `preflight` ya verifico por sha256 (`origen: repo`), no
reabriendo el archivo: el medidor consume exactamente lo que el SHA
identifica.
"""
from __future__ import annotations

import io
import sys
import types
import zipfile

import numpy as np
import pandas as pd


# ── utilidades ────────────────────────────────────────────────────────────

def _num(v):
    """`NO-ESTIMABLE` viaja como `null`, nunca como NaN ni como cadena."""
    if v is None:
        return None
    f = float(v)
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _norm(col: str) -> str:
    """Los CSV de ENIGH vienen UTF-8 con BOM. Se leen en latin-1 (nunca
    falla, y todos los campos que esta spec usa son ASCII) y se le quita al
    primer nombre de columna el BOM ya decodificado."""
    return col.lstrip("﻿").lstrip("ï»¿").strip()


def _selector(inputs):
    """Modulo del selector, ejecutado desde los bytes verificados.

    El modulo se registra en `sys.modules` ANTES del `exec`: `@dataclass`
    resuelve las anotaciones via `sys.modules[cls.__module__].__dict__`, y sin
    el registro eso es `None.__dict__`. Mismo patron que `_carga_medidor` de
    `tools/corrida0.py`."""
    crudo = inputs["IN-B-SELECTOR"]["bytes"]
    nombre = "baseline_temporal_calc_b_0001"
    mod = types.ModuleType(nombre)
    sys.modules[nombre] = mod
    exec(compile(crudo, "tools/baseline_temporal.py", "exec"), mod.__dict__)
    return mod


def _csv_de_la_ola(ruta_zip: str, directorio: str) -> pd.DataFrame:
    """Un solo CSV de datos por ola. Si no hay exactamente uno, la corrida
    PARA: adivinar cual es seria elegir el dato."""
    with zipfile.ZipFile(ruta_zip) as z:
        cand = [n for n in z.namelist()
                if n.startswith(directorio + "/conjunto_de_datos/")
                and n.endswith(".csv") and "bitacora" not in n]
        if len(cand) != 1:
            raise RuntimeError(
                f"{ruta_zip}: se esperaba UN csv de datos bajo "
                f"{directorio}/conjunto_de_datos/, hay {len(cand)}: {cand}")
        crudo = z.read(cand[0])
    texto = crudo.decode("latin-1")
    cabecera = [_norm(c) for c in texto.split("\n", 1)[0].strip().split(",")]
    quiero = {"folioviv", "foliohog", "factor", "upm", "est_dis", "remesas"}
    faltan = quiero - set(cabecera)
    if faltan:
        raise RuntimeError(f"{ruta_zip}/{directorio}: faltan columnas {sorted(faltan)}")
    df = pd.read_csv(io.StringIO(texto), dtype=str, low_memory=False,
                     usecols=lambda c: _norm(c) in quiero)
    df.columns = [_norm(c) for c in df.columns]
    return df[sorted(quiero)]


def _boot_ic(y, w, est, upm, replicas, semilla, n_min):
    """Bootstrap de UPM CON REEMPLAZO DENTRO DE CADA ESTRATO, conservando el
    numero de UPM por estrato; percentiles 2.5/97.5. Vectorizado por
    replica: se re-suman conglomerados ya agregados, no filas."""
    if y.size < n_min:
        return None, None
    clave = np.char.add(np.char.add(est, "|"), upm)
    u_cl, inv = np.unique(clave, return_inverse=True)
    sy = np.bincount(inv, weights=y * w, minlength=u_cl.size)
    sw = np.bincount(inv, weights=w, minlength=u_cl.size)
    est_cl = np.array([c.rsplit("|", 1)[0] for c in u_cl])
    _u_est, inv_est = np.unique(est_cl, return_inverse=True)
    orden = np.argsort(inv_est, kind="stable")
    cuenta = np.bincount(inv_est)
    inicio = np.concatenate(([0], np.cumsum(cuenta)[:-1]))
    ini_slot = inicio[inv_est]
    cnt_slot = cuenta[inv_est]
    rng = np.random.Generator(np.random.PCG64(semilla))
    reps = np.empty(replicas, dtype="float64")
    for i in range(replicas):
        sel = orden[ini_slot + rng.integers(0, cnt_slot)]
        d = sw[sel].sum()
        reps[i] = sy[sel].sum() / d if d > 0 else np.nan
    reps = reps[np.isfinite(reps)]
    if reps.size < replicas // 2:
        return None, None
    return float(np.percentile(reps, 2.5)), float(np.percentile(reps, 97.5))


# ── medicion ──────────────────────────────────────────────────────────────

def medir(inputs, contrato):
    p = contrato["parametros"]
    B = _selector(inputs)
    replicas = int(p["bootstrap_replicas"])
    n_min = int(p["n_minimo_celda"])
    semilla = int(contrato["seed"]["valor"])
    col = p["columnas"]
    out: dict[str, object] = {}
    obs: dict[str, dict] = {}

    # ── 1 · una ola a la vez, jamas agrupadas ─────────────────────────────
    for ficha in p["olas"]:
        ola = str(ficha["ola"])
        pre = f"RESULT-B-ENIGH-{ola}"
        df = _csv_de_la_ola(inputs[ficha["payload_id"]]["ruta_absoluta"],
                            ficha["directorio"])
        out[f"{pre}-METADATO-TEMPORAL"] = ficha["temporal_verbatim"]

        rem = pd.to_numeric(df[col["desenlace"]], errors="coerce").to_numpy("float64")
        w = pd.to_numeric(df[col["ponderador"]], errors="coerce").to_numpy("float64")
        n_nulos = int(np.sum(~np.isfinite(rem)))
        out[f"{pre}-N-NULOS-REMESAS"] = n_nulos

        est = df[col["estrato"]].fillna("").astype(str).to_numpy()
        upm = df[col["upm"]].fillna("").astype(str).to_numpy()
        sin_diseno = (est == "") | (upm == "") | (est == "nan") | (upm == "nan")
        out[f"{pre}-N-SIN-DISENO"] = int(np.sum(sin_diseno))

        valido = np.isfinite(w) & (w > 0) & np.isfinite(rem)
        out[f"{pre}-N"] = int(np.sum(valido))
        out[f"{pre}-HOGARES-EXPANDIDOS"] = _num(np.sum(w[valido])) if valido.any() else None

        # §1.1: la rama NA no existe. Si aparece un nulo, la ola PARA.
        if n_nulos > 0:
            out[f"{pre}-P"] = out[f"{pre}-IC-LO"] = out[f"{pre}-IC-HI"] = None
            out[f"{pre}-VEREDICTO"] = "NO-ESTIMABLE-NULOS-INESPERADOS"
            obs[ola] = {"p": None}
            continue

        y = (rem[valido] > 0).astype("float64")
        wv = w[valido]
        punto = float(np.sum(y * wv) / np.sum(wv)) if wv.size else None
        out[f"{pre}-P"] = _num(punto)

        if int(np.sum(sin_diseno & valido)) > 0:
            lo = hi = None
            veredicto = "NO-ESTIMABLE-DISENO-INCOMPLETO"
        else:
            lo, hi = _boot_ic(y, wv, est[valido], upm[valido],
                              replicas, semilla, n_min)
            veredicto = ("SERIE-REPORTADA" if punto is not None and wv.size >= n_min
                         else "NO-ESTIMABLE")
        out[f"{pre}-IC-LO"] = _num(lo)
        out[f"{pre}-IC-HI"] = _num(hi)
        out[f"{pre}-VEREDICTO"] = veredicto
        obs[ola] = {"p": _num(punto), "lo": _num(lo), "hi": _num(hi),
                    "disponible_desde": ficha["modified"]}

    # ── 2 · el selector B, dos brazos, sin tocarlo ────────────────────────
    serie = dict(p["serie"])
    n_pred = {}
    dentro = {}
    for brazo in p["brazos"]:
        n_pred[brazo] = 0
        dentro[brazo] = []
        for objetivo in p["objetivos"]:
            obj = str(objetivo)
            pre = f"RESULT-B-{brazo}-{obj}"
            historial = []
            for ficha in p["olas"]:
                ola = str(ficha["ola"])
                if ola == obj:
                    continue
                disp = (ficha["modified"] if brazo == "OPERATIVO"
                        else f"{ola}-12-31")
                historial.append({
                    "serie": serie,
                    "periodo_inicio": f"{ola}-01-01",
                    "periodo_fin": f"{ola}-12-31",
                    "disponible_desde": disp,
                    "publicada": True,
                    "p": obs.get(ola, {}).get("p"),
                    "resultado_id": f"RESULT-B-ENIGH-{ola}-P",
                    "fuente": ficha["payload_id"],
                })
            doc = {
                "objetivo": {
                    "serie": serie,
                    "periodo_inicio": f"{obj}-01-01",
                    "periodo_fin": f"{obj}-12-31",
                    "fecha_corte": f"{int(obj) - 1}-12-31",
                },
                "historial": historial,
            }
            r = B.desde_documento(doc)
            out[f"{pre}-ESTADO"] = r["estado"]
            out[f"{pre}-METODO"] = r["metodo"]
            out[f"{pre}-FUENTE"] = r.get("resultado_id") or "SIN-BASELINE"
            pb = _num(r.get("p"))
            out[f"{pre}-P"] = pb
            o = obs.get(obj, {})
            po, lo, hi = o.get("p"), o.get("lo"), o.get("hi")
            if pb is None or po is None:
                out[f"{pre}-ERROR"] = None
                out[f"{pre}-ERROR-ABS"] = None
                out[f"{pre}-DENTRO-IC"] = "SIN-BASELINE" if pb is None else "SIN-OBSERVADA"
                out[f"{pre}-MARGEN-AL-BORDE"] = None
                continue
            n_pred[brazo] += 1
            out[f"{pre}-ERROR"] = _num(pb - po)
            out[f"{pre}-ERROR-ABS"] = _num(abs(pb - po))
            if lo is None or hi is None:
                out[f"{pre}-DENTRO-IC"] = "SIN-IC"
                out[f"{pre}-MARGEN-AL-BORDE"] = None
            else:
                adentro = lo <= pb <= hi
                out[f"{pre}-DENTRO-IC"] = "SI" if adentro else "NO"
                # positivo = dentro; magnitud = distancia al borde mas cercano
                margen = min(pb - lo, hi - pb)
                out[f"{pre}-MARGEN-AL-BORDE"] = _num(margen)
                dentro[brazo].append(bool(adentro))

    for brazo in p["brazos"]:
        out[f"RESULT-B-N-PREDICCIONES-{brazo}"] = int(n_pred[brazo])
        d = dentro[brazo]
        if not d:
            lectura = "SIN-PREDICCIONES"
        elif all(d):
            lectura = "PISO-ALTO"
        elif not any(d):
            lectura = "PISO-BAJO"
        else:
            lectura = "MIXTO"
        out[f"RESULT-B-BIS-LECTURA-{brazo}"] = lectura

    # ── 3 · pre-declaracion de adopcion, TRES ramas (§6 de la sellada) ────
    # `umbral_replay` DEBE ser identico a `tolerancia.abs` de esta spec: es la
    # tolerancia con que `T35 (c)` compara el valor materializado por el
    # consumidor contra el RESULT. `contrato_ejecutable()` no pasa
    # `tolerancia`, asi que se declara aqui espejada y la spec lo dice.
    a = p["adopcion_p3"]
    medido = out.get(a["result_id"])
    if medido is None:
        out["RESULT-B-ADOPCION-P3-DELTA"] = None
        out["RESULT-B-ADOPCION-P3"] = "NO-ADOPTABLE-POR-DISCREPANCIA"
    else:
        delta = float(medido) - float(a["valor_materializado"])
        out["RESULT-B-ADOPCION-P3-DELTA"] = _num(delta)
        if abs(delta) <= float(a["umbral_replay"]):
            rama = "ADOPTABLE"
        elif abs(delta) < float(a["umbral_grano_milpa"]):
            rama = "NO-ADOPTABLE-POR-GRANO"
        else:
            rama = "NO-ADOPTABLE-POR-DISCREPANCIA"
        out["RESULT-B-ADOPCION-P3"] = rama
    return out
