#!/usr/bin/env python3
"""CALC-GOB-DIGITAL-EXE-EMISIONES-0002 · piloto 3 · emisiones de candidatos · v1.1.

Sucede a CALC-GOB-DIGITAL-EXE-EMISIONES-0001 (`repite_de`), cuyo `medir()` nunca
corrió (`NotImplementedError`; `ACTO GEN2-CELDA-D-PILOTO-3-EJECUCION`, PR #924).
Congelado por `ACTO GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_1` (20/sep/2026, CAJA) SIN
abrir ENCIG 2025: el punto de entrada corrió sobre un fixture sintético y, con
`ola=2023`, reprodujo los marginales sellados de
CALC-ENCIG2023-CRUCES-HISTORICOS-0002 (tests/test_piloto3_v11.py).

QUÉ ESTIMA (spec v1.1 §1, primera línea): proporción de PAGOS ORDINARIOS DEL
SERVICIO DE LUZ (N_TRA == 01) hechos por canal digital (P7_3 en {4,5}) entre los
de canal válido ({1,2,4,5,6}), por edad × escolaridad. Unidad = TRÁMITE.

QUÉ HACE ESTE ARCHIVO (COMMIT-2): con la ola como PARÁMETRO, carga el payload por
id de manifiesto, une trámites↔personas por `ID_PER` (m:1, validado), aplica el
universo y F1-bis, y agrupa 2025 POR UNA SOLA VARIABLE: marginales de edad, de
escolaridad y total, con bootstrap de diseño (UPM con reposición dentro de
estrato, singleton de certeza; réplicas y semilla del precedente sellado). Con
esos marginales, réplica por réplica, emite por celda C2 (piso), S½ y Sλ; C1a y
C1b salen de los RESULT sellados de 2023 (puntos e IC sellados). El cruce de 2025
NO se agrupa aquí: n(a,b), R(a,b), soporte definitivo y adjudicación viven en
`adjudicacion.py` (COMMIT-3), que se niega a correr sin el sello de este CALC.

GUARDIAS (mecánicas, antes de tocar un archivo de datos):
  S1  el contrato trae `s1_veredicto` en {MISMO-INSTRUMENTO, CAMBIO-MENOR}
      (NC-0355 cerró CAMBIO-MENOR, PR #924). CAMBIO-DE-INSTRUMENTO → PARO.
  S2  FP-399 (firmada 20/sep/2026): el código 97 es edad real censurada y se
      mantiene FUERA del universo del cruce; este medidor CUENTA los trámites con
      97/98/99 (una sola variable de agrupación) y marca RESERVA-S2 si 97 supera
      el 1 % de los trámites de la banda 60+ (60-96 ∪ 97). Exige que la fila
      FP-399 figure FIRMADA en `forense/firmas-pendientes.tsv` (input `origen:
      repo`); si no, PARO. Ya no es un paro por el significado del código.
  RESERVA  ningún insumo cuyo id contenga `encig25`/`2025` entra si la ola del
      contrato no es 2025; y ninguna función de este archivo agrupa por dos
      variables.
"""
from __future__ import annotations

import io
import math
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

# ─── contrato de desenlace, idéntico al de 2021/2023 y al medidor de 2025 ───
ADOPTA = {"4", "5"}            # internet/app · cajero o kiosco inteligente
NO_ADOPTA = {"1", "2", "6"}    # instalaciones · banco o tienda · módulos móviles
TELEFONO = {"3"}               # FUERA del universo: canal remoto atendido
UNIVERSO_PRINCIPAL = {"1"}     # N_TRA normalizado: 01 = pago ordinario del servicio de luz

# ─── rejilla, idéntica a la congelada en las dos olas históricas ───
EDAD_BANDAS = [("18-29", 18, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60-96", 60, 96)]
NIV_AGREGADO = {"HASTA-PRIMARIA": {"0", "1", "2"}, "SECUNDARIA": {"3"},
                "MEDIA-SUPERIOR": {"4", "5", "6", "7"}, "SUPERIOR": {"8", "9"}}
EDADES = [b[0] for b in EDAD_BANDAS]
ESCOLARIDADES = list(NIV_AGREGADO)
CELDAS = [(a, b) for a in EDADES for b in ESCOLARIDADES]

# ─── parámetros congelados (heredados VERBATIM de la spec v1.0 §3.1, FP-400) ───
LAMBDA = 0.8937949410086089           # tau2/(tau2+sigma_bar2) sobre las 15 celdas PUNTUADA
N_MINIMO = 200
OLAS_SOPORTE = ("2021", "2023", "2025")
FUERA_DE_SOPORTE_GLOBAL_SI_FALLAN = 5
FRACCION_PARA_GANAR = 0.75
DELTA_MAE_UMBRAL_PP = 0.5
FUERA_DE_SOPORTE_EX_ANTE = {("18-29", "HASTA-PRIMARIA")}
RESERVA_S2_FRACCION = 0.01            # FP-399: 97 > 1 % de la banda 60+ → RESERVA-S2

PREFIJO_SELLADO = {"2021": "RESULT-ENCIG2021-CRUCES-HISTORICOS-EDAD-ESCOLARIDAD",
                   "2023": "RESULT-ENCIG2023-CRUCES-HISTORICOS-EDAD-ESCOLARIDAD"}
PREFIJO_CONTROL = "RESULT-C2COMP-ADOPTA-ENCIG2025-LUZ-EDADXESCOLARIDAD"


class ParoDeGuardia(RuntimeError):
    """Una condición suspensiva no está satisfecha. El módulo no mide."""


# ══════════════════════════════ guardias ══════════════════════════════

def _fp_estado(tsv_bytes: bytes, fp_id: str) -> str | None:
    """Estado de una fila FP en firmas-pendientes.tsv (columna `estado`)."""
    texto = tsv_bytes.decode("utf-8")
    lineas = texto.split("\n")
    cab = lineas[0].split("\t")
    col = cab.index("estado")
    for linea in lineas[1:]:
        if linea.startswith(fp_id + "\t"):
            partes = linea.split("\t")
            return partes[col].strip() if len(partes) > col else None
    return None


def _guardia_suspensiva(inputs: dict, contrato: dict) -> None:
    p = contrato["parametros"]
    s1 = str(p.get("s1_veredicto", ""))
    if s1 == "CAMBIO-DE-INSTRUMENTO":
        raise ParoDeGuardia("S1: NC-0355 cerró CAMBIO-DE-INSTRUMENTO. La spec se RETIRA SIN CORRER.")
    if s1 not in ("MISMO-INSTRUMENTO", "CAMBIO-MENOR"):
        raise ParoDeGuardia(f"S1: veredicto de NC-0355 no habilitante: {s1!r}.")
    ent = inputs.get("firmas_pendientes_tsv")
    if ent is None:
        raise ParoDeGuardia("S2: falta el input `firmas_pendientes_tsv` (forense/firmas-pendientes.tsv).")
    raw = ent.get("bytes")
    if raw is None:
        raw = Path(ent["ruta_absoluta"]).read_bytes()
    estado = _fp_estado(raw, "FP-399")
    if estado != "FIRMADA":
        raise ParoDeGuardia(f"S2: FP-399 debe figurar FIRMADA en firmas-pendientes.tsv (estado leído: {estado!r}).")


def _guardia_reserva(inputs: dict, contrato: dict) -> None:
    ola = str(contrato["parametros"]["ola"])
    payload_id = str(contrato["parametros"]["payload_id"])
    if payload_id not in inputs:
        raise ParoDeGuardia(f"payload `{payload_id}` declarado en el contrato y ausente de inputs.")
    if ola != "2025":
        for name in inputs:
            low = str(name).lower()
            if any(tok in low for tok in ("encig25", "encig_2025", "2025")):
                raise ParoDeGuardia(f"RESERVA: insumo `{name}` de 2025 con ola={ola}.")


# ══════════════════════════════ carga ══════════════════════════════

def _code(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.replace(r"^0+(?=\d)", "", regex=True)


def _member_csv(archive: str, suffix: str, columns: list[str]) -> pd.DataFrame:
    """Mismo lector que el script sellado (tools/encig_cruces_historicos.py)."""
    with zipfile.ZipFile(archive) as zf:
        wanted = suffix.lower()
        names = [n for n in zf.namelist()
                 if (Path(n).name.lower() in (wanted, "conjunto_de_datos_" + wanted))
                 and "diccionario_de_datos" not in n.lower()]
        if len(names) != 1:
            raise RuntimeError(f"miembro CSV no único: {suffix}: {names}")
        raw = zf.read(names[0])
    for encoding in ("utf-8-sig", "latin-1"):
        try:
            frame = pd.read_csv(io.StringIO(raw.decode(encoding)), dtype=str,
                                keep_default_na=False, na_filter=False)
        except UnicodeDecodeError:
            continue
        frame.columns = [str(c).strip() for c in frame.columns]
        missing = sorted(set(columns) - set(frame.columns))
        if missing:
            raise RuntimeError(f"variables ausentes en {suffix}: {missing}")
        return frame[columns].copy()
    raise RuntimeError(f"codificación no reconocida: {suffix}")


def _banda_edad(series: pd.Series) -> pd.Series:
    v = pd.to_numeric(series, errors="coerce")
    out = pd.Series(pd.NA, index=series.index, dtype="object")
    for nombre, lo, hi in EDAD_BANDAS:
        out[(v >= lo) & (v <= hi)] = nombre
    return out


def _escolaridad(series: pd.Series) -> pd.Series:
    return _code(series).map({c: k for k, cs in NIV_AGREGADO.items() for c in cs})


def cargar_universo(inputs: dict, contrato: dict) -> tuple[pd.DataFrame, dict]:
    """Universo del piloto sobre la ola del contrato. Join por `ID_PER`, m:1,
    validado; nunca por índice de fila. Devuelve el marco de trámites con
    diseño válido y los diagnósticos (incluido el conteo S2 por código)."""
    ola = str(contrato["parametros"]["ola"])
    payload_id = str(contrato["parametros"]["payload_id"])
    archive = inputs[payload_id]["ruta_absoluta"]
    events = _member_csv(archive, f"encig{ola}_04_sec_7.csv",
                         ["N_TRA", "P7_3", "FAC_TRA", "EST_DIS", "UPM_DIS", "ID_PER"])
    people = _member_csv(archive, f"encig{ola}_02_residentes_sec_2.csv", ["ID_PER", "EDAD", "NIV"])
    if people["ID_PER"].duplicated().any():
        raise RuntimeError("ID_PER no es único en residentes")
    joined = events.merge(people, on="ID_PER", how="left", validate="m:1", indicator=True)
    ntra, p73 = _code(joined["N_TRA"]), _code(joined["P7_3"])
    universe = ntra.isin(UNIVERSO_PRINCIPAL) & p73.isin(ADOPTA | NO_ADOPTA)
    frame = joined.loc[universe].copy()
    frame["_w"] = pd.to_numeric(frame["FAC_TRA"], errors="coerce")
    frame["_est"] = frame["EST_DIS"].astype(str).str.strip()
    frame["_upm"] = frame["UPM_DIS"].astype(str).str.strip()
    frame["_y"] = _code(frame["P7_3"]).isin(ADOPTA).astype(float)
    frame["_edad_cod"] = pd.to_numeric(frame["EDAD"], errors="coerce")
    frame["_edad"] = _banda_edad(frame["EDAD"])
    frame["_esc"] = _escolaridad(frame["NIV"])
    design = frame["_w"].notna() & (frame["_w"] > 0) & frame["_est"].ne("") & frame["_upm"].ne("")
    frame = frame.loc[design].copy()
    frame["_key"] = frame["_est"] + "\t" + frame["_upm"]
    if (frame.groupby("ID_PER")["_key"].nunique() > 1).any():
        raise RuntimeError("una persona pertenece a más de una UPM de diseño")

    # S2 (FP-399): conteo por código de edad, UNA variable de agrupación.
    s2 = {}
    for cod in (97, 98, 99):
        sel = frame["_edad_cod"].eq(cod)
        s2[f"S2-EDAD-{cod}-N"] = int(sel.sum())
        s2[f"S2-EDAD-{cod}-MASA"] = float(frame.loc[sel, "_w"].sum())
    n_60mas = int(frame["_edad"].eq("60-96").sum()) + s2["S2-EDAD-97-N"]
    frac = (s2["S2-EDAD-97-N"] / n_60mas) if n_60mas > 0 else 0.0
    s2["S2-BANDA-60MAS-N"] = n_60mas
    s2["S2-FRACCION-97-EN-60MAS"] = float(frac)
    s2["S2-RESERVA"] = "RESERVA-S2" if frac > RESERVA_S2_FRACCION else "SIN-RESERVA"

    completo = frame["_edad"].notna() & frame["_esc"].notna()
    diag = {
        "FILAS-EVENTOS": int(len(events)),
        "JOIN-SIN-DEMOGRAFIA": int(joined["_merge"].ne("both").sum()),
        "N-UNIVERSO": int(universe.sum()),
        "N-DISENO-VALIDO": int(len(frame)),
        "P7-3-EXCLUIDAS": int((ntra.isin(UNIVERSO_PRINCIPAL) & ~p73.isin(ADOPTA | NO_ADOPTA)).sum()),
        "N-COMPLETOS": int(completo.sum()),
        "RESIDUO-EDAD-N": int((frame["_esc"].notna() & frame["_edad"].isna()).sum()),
        "RESIDUO-EDAD-MASA": float(frame.loc[frame["_esc"].notna() & frame["_edad"].isna(), "_w"].sum()),
        "RESIDUO-ESC-N": int((frame["_edad"].notna() & frame["_esc"].isna()).sum()),
        "RESIDUO-ESC-MASA": float(frame.loc[frame["_edad"].notna() & frame["_esc"].isna(), "_w"].sum()),
        **s2,
    }
    # El marco de DISEÑO entero entra al bootstrap (como en el script sellado:
    # las UPM sin casos completos siguen en el sorteo); `completo` va dentro de
    # cada máscara, nunca recortando el marco antes de sortear.
    frame["_completo"] = completo
    return frame, diag


# ══════════════════════════════ bootstrap ══════════════════════════════

def _logit(v):
    v = np.asarray(v, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.log(v / (1.0 - v))


def _expit(x):
    return 1.0 / (1.0 + np.exp(-np.asarray(x, dtype=float)))


def _ratio(num, den):
    return np.divide(num, den, out=np.full_like(num, np.nan, dtype=float), where=den > 0)


def _matrix_by_psu(frame: pd.DataFrame, masks: list[pd.Series]):
    keys = sorted(frame["_key"].unique())
    positions = {k: i for i, k in enumerate(keys)}
    den = np.zeros((len(keys), len(masks)), dtype=float)
    num = np.zeros_like(den)
    for column, mask in enumerate(masks):
        chosen = frame.loc[mask]
        for key, weight, outcome in zip(chosen["_key"], chosen["_w"], chosen["_y"]):
            pos = positions[key]
            den[pos, column] += float(weight)
            num[pos, column] += float(weight) * float(outcome)
    return keys, num, den


def bootstrap(frame: pd.DataFrame, masks: list[pd.Series], repetitions: int, seed: int):
    """Idéntico al del script sellado: UPM con reposición dentro de estrato,
    singleton de certeza, PCG64(seed), bloques de 50. Las multiplicidades no
    dependen de las máscaras, así que dos llamadas con el mismo marco y la
    misma semilla comparten réplicas aunque pidan columnas distintas."""
    keys, num, den = _matrix_by_psu(frame, masks)
    strata: dict[str, list[int]] = {}
    for pos, key in enumerate(keys):
        strata.setdefault(key.split("\t", 1)[0], []).append(pos)
    points = _ratio(num.sum(axis=0), den.sum(axis=0))
    replicas = np.full((repetitions, len(masks)), np.nan, dtype=float)
    rng = np.random.Generator(np.random.PCG64(seed))
    for start in range(0, repetitions, 50):
        size = min(50, repetitions - start)
        multiplicity = np.zeros((size, len(keys)), dtype=np.int16)
        for stratum in sorted(strata):
            indices = np.asarray(strata[stratum], dtype=int)
            if len(indices) == 1:
                multiplicity[:, indices[0]] = 1
                continue
            draws = rng.integers(0, len(indices), size=(size, len(indices)))
            for row in range(size):
                multiplicity[row] += np.bincount(indices[draws[row]], minlength=len(keys)).astype(np.int16)
        replicas[start:start + size] = _ratio(multiplicity @ num, multiplicity @ den)
    return points, replicas, den.sum(axis=0)


def resumen(point: float, replicas: np.ndarray):
    valid = np.isfinite(replicas)
    count = int(valid.sum())
    if not np.isfinite(point) or count != len(replicas):
        return None, None, None, count
    ee = float(np.std(replicas, ddof=1))
    lo, hi = np.percentile(replicas, [2.5, 97.5])
    return ee, float(lo), float(hi), count


# ══════════════════════════════ marginales ══════════════════════════════

def marginales(frame: pd.DataFrame, repetitions: int, seed: int) -> dict:
    """Nueve máscaras de UNA variable: 4 edad, 4 escolaridad, 1 total (casos
    completos). Devuelve puntos, réplicas y n por máscara."""
    masks, nombres = [], []
    comp = frame["_completo"]
    for a in EDADES:
        masks.append(comp & frame["_edad"].eq(a)); nombres.append(("EDAD", a))
    for b in ESCOLARIDADES:
        masks.append(comp & frame["_esc"].eq(b)); nombres.append(("ESC", b))
    masks.append(comp.copy()); nombres.append(("ALL", "ALL"))
    points, boot, den = bootstrap(frame, masks, repetitions, seed)
    return {"nombres": nombres, "puntos": points, "replicas": boot, "den": den,
            "n": [int(m.sum()) for m in masks]}


def c2_desde_marginales(m: dict) -> tuple[dict, dict]:
    """C2 = expit(logit p_a + logit p_b − logit p_all), punto y réplica por
    réplica. NO es independencia multiplicativa (FP-379 D2)."""
    idx = {n: i for i, n in enumerate(m["nombres"])}
    la = {a: (_logit(m["puntos"][idx[("EDAD", a)]]), _logit(m["replicas"][:, idx[("EDAD", a)]])) for a in EDADES}
    lb = {b: (_logit(m["puntos"][idx[("ESC", b)]]), _logit(m["replicas"][:, idx[("ESC", b)]])) for b in ESCOLARIDADES}
    lall = (_logit(m["puntos"][idx[("ALL", "ALL")]]), _logit(m["replicas"][:, idx[("ALL", "ALL")]]))
    punto, rep = {}, {}
    for a, b in CELDAS:
        punto[(a, b)] = float(_expit(la[a][0] + lb[b][0] - lall[0]))
        rep[(a, b)] = _expit(la[a][1] + lb[b][1] - lall[1])
    return punto, rep


# ══════════════════════════════ sellados ══════════════════════════════

def _json_input(inputs: dict, iid: str) -> dict:
    import json
    ent = inputs[iid]
    raw = ent.get("bytes")
    if raw is None:
        raw = Path(ent["ruta_absoluta"]).read_bytes()
    doc = json.loads(raw.decode("utf-8"))
    return doc.get("resultados", doc)


def sellados(inputs: dict) -> dict:
    """p, δ, EE, IC y n por celda de 2021 y 2023 (RESULT sellados), y el punto
    de control C2-compuesto."""
    r21 = _json_input(inputs, "encig2021_cruces_resultados")
    r23 = _json_input(inputs, "encig2023_cruces_resultados")
    ctl = _json_input(inputs, "c2_compuesto_resultados")
    out = {}
    for (a, b) in CELDAS:
        k21 = f"{PREFIJO_SELLADO['2021']}-{a}-{b}"
        k23 = f"{PREFIJO_SELLADO['2023']}-{a}-{b}"
        out[(a, b)] = {
            "n21": int(r21[k21 + "-N"]), "n23": int(r23[k23 + "-N"]),
            "p23": r23[k23 + "-P"], "p23_lo": r23[k23 + "-P-IC-LO"], "p23_hi": r23[k23 + "-P-IC-HI"],
            "d21": r21[k21 + "-DELTA"], "d23": r23[k23 + "-DELTA"],
            "ee21": r21[k21 + "-DELTA-EE"], "ee23": r23[k23 + "-DELTA-EE"],
            "control": ctl.get(f"{PREFIJO_CONTROL}-{a}-X-{b}"),
        }
    return out


def soporte_historico(sel: dict) -> dict:
    """Soporte con las olas ya selladas (2021, 2023). El tercer requisito
    (n ≥ 200 en 2025) se lee en COMMIT-3 (adjudicacion.py), no aquí: leerlo
    exige agrupar 2025 por dos variables, y este archivo no lo hace (E.6)."""
    est = {}
    for c in CELDAS:
        if c in FUERA_DE_SOPORTE_EX_ANTE:
            est[c] = "FUERA-DE-SOPORTE-EX-ANTE"
        elif sel[c]["n21"] >= N_MINIMO and sel[c]["n23"] >= N_MINIMO:
            est[c] = "PUNTUADA-PENDIENTE-2025"
        else:
            est[c] = "FUERA-DE-SOPORTE-HISTORICO"
    return est


# ══════════════════════════════ emisiones ══════════════════════════════

def prefijo(ola: str) -> str:
    return f"RESULT-GOB-EXE15-{ola}"


def emisiones(frame: pd.DataFrame, sel: dict, repetitions: int, seed: int, ola: str) -> dict:
    P = prefijo(ola)
    m = marginales(frame, repetitions, seed)
    out = {}
    for i, (eje, cat) in enumerate(m["nombres"]):
        base = f"{P}-MARGINAL-{eje}-{cat}"
        ee, lo, hi, valid = resumen(float(m["puntos"][i]), m["replicas"][:, i])
        out.update({base + "-N": m["n"][i], base + "-DEN-W": float(m["den"][i]),
                    base + "-P": float(m["puntos"][i]) if np.isfinite(m["puntos"][i]) else None,
                    base + "-P-EE": ee, base + "-P-IC-LO": lo, base + "-P-IC-HI": hi,
                    base + "-B-VALIDAS": valid})
    c2p, c2r = c2_desde_marginales(m)
    sop = soporte_historico(sel)
    for (a, b) in CELDAS:
        s = sel[(a, b)]
        base = f"{P}-{a}-{b}"
        dbar = (s["d21"] + s["d23"]) / 2.0
        cand_rep = {
            "C2": c2r[(a, b)],
            "S-MEDIO": _expit(_logit(c2r[(a, b)]) + 0.5 * s["d23"]),
            "S-LAMBDA": _expit(_logit(c2r[(a, b)]) + LAMBDA * dbar),
        }
        cand_pt = {
            "C2": c2p[(a, b)],
            "S-MEDIO": float(_expit(_logit(c2p[(a, b)]) + 0.5 * s["d23"])),
            "S-LAMBDA": float(_expit(_logit(c2p[(a, b)]) + LAMBDA * dbar)),
        }
        for cid in ("C2", "S-MEDIO", "S-LAMBDA"):
            ee, lo, hi, valid = resumen(cand_pt[cid], cand_rep[cid])
            out.update({f"{base}-{cid}-P": cand_pt[cid] if math.isfinite(cand_pt[cid]) else None,
                        f"{base}-{cid}-P-EE": ee, f"{base}-{cid}-P-IC-LO": lo,
                        f"{base}-{cid}-P-IC-HI": hi, f"{base}-{cid}-B-VALIDAS": valid})
        # C1a: compuesto con marginales de 2023 = expit(logit p23 − δ23). Punto
        # sellado; sin réplicas selladas de 2023 → IC no derivable, declarado.
        c1a = float(_expit(_logit(s["p23"]) - s["d23"]))
        out.update({f"{base}-C1A-P": c1a, f"{base}-C1A-P-IC-LO": None, f"{base}-C1A-P-IC-HI": None,
                    f"{base}-C1A-IC-CAUSA": "SIN-REPLICAS-SELLADAS-2023",
                    f"{base}-C1B-P": s["p23"], f"{base}-C1B-P-IC-LO": s["p23_lo"],
                    f"{base}-C1B-P-IC-HI": s["p23_hi"],
                    f"{base}-DELTA-21": s["d21"], f"{base}-DELTA-23": s["d23"], f"{base}-DELTA-BARRA": dbar,
                    f"{base}-N-2021": s["n21"], f"{base}-N-2023": s["n23"],
                    f"{base}-SOPORTE-HISTORICO": sop[(a, b)],
                    f"{base}-CONTROL-C2COMP-P": s["control"],
                    f"{base}-C2-VS-CONTROL-ABS": (abs(c2p[(a, b)] - s["control"])
                                                  if s["control"] is not None and math.isfinite(c2p[(a, b)]) else None)})
    out[f"{P}-LAMBDA"] = LAMBDA
    out[f"{P}-BOOTSTRAP-REPLICAS"] = int(repetitions)
    out[f"{P}-SEED"] = int(seed)
    return out


def esquema_resultados(ola: str) -> list[dict]:
    """Ids y tipos que `medir()` emite, para la lista `resultados:` de spec.yaml
    (derivada por comando, no tecleada)."""
    P = prefijo(ola)
    rows = []
    def add(i, t, u): rows.append({"id": i, "tipo": t, "unidad": u})
    for k, t in (("FILAS-EVENTOS", "entero"), ("JOIN-SIN-DEMOGRAFIA", "entero"), ("N-UNIVERSO", "entero"),
                 ("N-DISENO-VALIDO", "entero"), ("P7-3-EXCLUIDAS", "entero"), ("N-COMPLETOS", "entero"),
                 ("RESIDUO-EDAD-N", "entero"), ("RESIDUO-EDAD-MASA", "flotante"),
                 ("RESIDUO-ESC-N", "entero"), ("RESIDUO-ESC-MASA", "flotante"),
                 ("S2-EDAD-97-N", "entero"), ("S2-EDAD-97-MASA", "flotante"),
                 ("S2-EDAD-98-N", "entero"), ("S2-EDAD-98-MASA", "flotante"),
                 ("S2-EDAD-99-N", "entero"), ("S2-EDAD-99-MASA", "flotante"),
                 ("S2-BANDA-60MAS-N", "entero"), ("S2-FRACCION-97-EN-60MAS", "flotante"), ("S2-RESERVA", "texto")):
        add(f"{P}-{k}", t, "trámites" if t == "entero" else ("masa FAC_TRA" if "MASA" in k else "estado" if t == "texto" else "fracción"))
    for eje, cats in (("EDAD", EDADES), ("ESC", ESCOLARIDADES), ("ALL", ["ALL"])):
        for cat in cats:
            base = f"{P}-MARGINAL-{eje}-{cat}"
            add(base + "-N", "entero", "trámites"); add(base + "-DEN-W", "flotante", "denominador ponderado")
            add(base + "-P", "proporcion", "proporción [0,1]"); add(base + "-P-EE", "flotante", "error estándar")
            add(base + "-P-IC-LO", "proporcion", "límite inferior IC95"); add(base + "-P-IC-HI", "proporcion", "límite superior IC95")
            add(base + "-B-VALIDAS", "entero", "réplicas definidas")
    for a, b in CELDAS:
        base = f"{P}-{a}-{b}"
        for cid in ("C2", "S-MEDIO", "S-LAMBDA"):
            add(f"{base}-{cid}-P", "proporcion", "proporción [0,1]"); add(f"{base}-{cid}-P-EE", "flotante", "error estándar")
            add(f"{base}-{cid}-P-IC-LO", "proporcion", "límite inferior IC95"); add(f"{base}-{cid}-P-IC-HI", "proporcion", "límite superior IC95")
            add(f"{base}-{cid}-B-VALIDAS", "entero", "réplicas definidas")
        add(f"{base}-C1A-P", "proporcion", "proporción [0,1]"); add(f"{base}-C1A-P-IC-LO", "proporcion", "NO-DERIVABLE (null)")
        add(f"{base}-C1A-P-IC-HI", "proporcion", "NO-DERIVABLE (null)"); add(f"{base}-C1A-IC-CAUSA", "texto", "estado")
        add(f"{base}-C1B-P", "proporcion", "proporción [0,1] sellada 2023"); add(f"{base}-C1B-P-IC-LO", "proporcion", "IC95 sellado 2023")
        add(f"{base}-C1B-P-IC-HI", "proporcion", "IC95 sellado 2023")
        add(f"{base}-DELTA-21", "flotante", "logit sellado 2021"); add(f"{base}-DELTA-23", "flotante", "logit sellado 2023")
        add(f"{base}-DELTA-BARRA", "flotante", "logit"); add(f"{base}-N-2021", "entero", "trámites sellado 2021")
        add(f"{base}-N-2023", "entero", "trámites sellado 2023"); add(f"{base}-SOPORTE-HISTORICO", "texto", "estado")
        add(f"{base}-CONTROL-C2COMP-P", "proporcion", "control, punto sin IC")
        add(f"{base}-C2-VS-CONTROL-ABS", "flotante", "|C2 − control|")
    add(f"{P}-LAMBDA", "flotante", "λ congelada"); add(f"{P}-BOOTSTRAP-REPLICAS", "entero", "réplicas")
    add(f"{P}-SEED", "entero", "semilla PCG64")
    return rows


def medir(inputs: dict, contrato: dict) -> dict:
    """Punto de entrada del COMMIT-2. Corrió en COMMIT-1 sobre fixture sintético
    y sobre ENCIG 2023 (control de oro); nunca sobre 2025 antes del COMMIT-2."""
    _guardia_suspensiva(inputs, contrato)
    _guardia_reserva(inputs, contrato)
    p = contrato["parametros"]
    ola = str(p["ola"])
    repetitions = int(p["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    frame, diag = cargar_universo(inputs, contrato)
    sel = sellados(inputs)
    out = {f"{prefijo(ola)}-{k}": v for k, v in diag.items()}
    out.update(emisiones(frame, sel, repetitions, seed, ola))
    return out
