#!/usr/bin/env python3
"""El primer resultado que produzca este procedimiento es el que se reporta.

CALC-ARBITRO-PERSISTENCIA-ERROR-0001 · ACTO GEN2-ARBITRO-MARGINALES-1 (pieza 3).

ADJUDICACIÓN DE LA PERSISTENCIA, como aritmética entre sellados. CERO
MICRODATO: los dos lados de cada resta ya están sellados —
  · el PISO (persistencia t-1): `CALC-PISOS-ENIF2021-EJES-0003`,
    `…-ENIF2021-FORMALIDAD-0001`, `…-ENVIPE2024-EJES-0002`, `…-ENCIG2023-EJES-0002`;
  · la REALIDAD R (ola nueva, GEN2): `CALC-ARBITRO-MARGINALES-ENIF2024-0001`,
    `…-ENVIPE2025-0001`, `…-ENCIG2025-0001`;
enlazados 1:1 por `forense/prereg-caja/ARBITRO-MARGINALES-metadatos-v1_0.tsv`
(57 celdas: las `SOLO-PISO` del marcador en `55c8d57c`). Rotulada PROSPECTIVA:
cada piso se selló antes de que GEN2 midiera su R.

POR CELDA: d = (R − piso)·100 en pp; IC95 de d por simetría normal desde los
dos IC95 sellados (olas tratadas como muestras independientes; misma receta
que `CALC-PISO-PERSISTENCIA-ERROR-0001`); CLASE = PERSISTE si el IC de d
incluye 0, CAMBIA si lo excluye; COBERTURA = DENTRO si R (punto) cae en el
IC95 del piso, FUERA si no. Además, para el hallazgo sobre GEN1: p del
árbitro GEN1 (`milpa/tramite-ola5-propuesta-v0.yaml`, misma celda) y
R − p_GEN1, con cotejo COINCIDE (|Δ| ≤ 5e-7, el redondeo a 6 decimales del
yaml) / DISCREPA. Y donde un piloto ya selló el marginal de la ola nueva
(`CALC-C2-COMPUESTO-IC-ENIF2024-0001`, 28 celdas; `CALC-GOB-DIGITAL-EXE-EMISIONES-0002`,
8 celdas) se CITA y se coteja: COINCIDE (|Δp| ≤ 1e-6) / COINCIDE-1E-3 /
DISCREPA, sin gatear nada.

POR ENCUESTA (y por encuesta×desenlace y encuesta×eje; NUNCA entre
encuestas: unidades persona/delito/trámite y brechas 3/1/2 años distintas):
N, error medio (media de d), MAE, N-DENTRO, cobertura = N-DENTRO/N con IC95
binomial de Wilson, N-PERSISTE, N-CAMBIA.

Sólo stdlib + yaml. No adopta nada. No corrige el yaml GEN1.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import yaml

Z95 = 1.959964
TOL_GEN1 = 5e-7          # redondeo a 6 decimales del yaml
TOL_SELLADO = 1e-6       # mismo método y misma semilla reproducen a esto
TOL_SELLADO_LAXA = 1e-3  # método distinto (otro bootstrap, otro universo por NA)
PREF = "RESULT-ARBERR"

INPUT_TABLA = "ARBITRO-MARGINALES-METADATOS"
INPUT_YAML = "ARBITRO-OLA5-YAML"
INPUTS_R = {"ENIF": "R-ENIF2024", "ENVIPE": "R-ENVIPE2025", "ENCIG": "R-ENCIG2025"}
INPUTS_PISO = {"CALC-PISOS-ENIF2021-EJES-0003": "PISO-ENIF2021-EJES",
               "CALC-PISOS-ENIF2021-FORMALIDAD-0001": "PISO-ENIF2021-FORMALIDAD",
               "CALC-PISOS-ENVIPE2024-EJES-0002": "PISO-ENVIPE2024-EJES",
               "CALC-PISOS-ENCIG2023-EJES-0002": "PISO-ENCIG2023-EJES"}
INPUTS_SELLADO = {"ENIF": "SELLADO-C2IC-ENIF2024", "ENCIG": "SELLADO-GOB-EXE-2025"}

# ── mapa explícito R -> marginal sellado por un piloto (cita, no re-medición) ──
# lado izquierdo: sufijo del id de R sin `RESULT-ARBITRO-<INST><ola>-` ni `-P`.
# lado derecho: id sellado del punto (el IC se deriva por sufijo declarado).
MAPA_C2IC_EJE = {"SEXO-1": "SEXO-1-HOMBRE", "SEXO-2": "SEXO-2-MUJER",
                 "EDAD-18-29": "EDAD-18-29", "EDAD-30-44": "EDAD-30-44", "EDAD-45-59": "EDAD-45-59",
                 "EDAD-60-MAS": "EDAD-60",
                 "ESCOLARIDAD-HASTA-PRIMARIA": "ESCOLARIDAD-HASTA-PRIMARIA",
                 "ESCOLARIDAD-SECUNDARIA": "ESCOLARIDAD-SECUNDARIA",
                 "ESCOLARIDAD-MEDIA-SUPERIOR": "ESCOLARIDAD-MEDIA-SUPERIOR",
                 "ESCOLARIDAD-SUPERIOR": "ESCOLARIDAD-SUPERIOR",
                 "LOCALIDAD-MENOR-DE-15-000": "LOCALIDAD-MENOR-DE-15-000",
                 "LOCALIDAD-15-000-Y-MAS": "LOCALIDAD-15-000-Y-MAS",
                 "CUENTA-SIN-CUENTA": "CUENTA-FORMAL-SIN-CUENTA",
                 "CUENTA-CON-CUENTA": "CUENTA-FORMAL-CON-CUENTA"}
MAPA_C2IC_DES = {"D9": "AHORRA-SOLO-INFORMAL", "INFORMAL-CUALQUIERA": "INFORMAL-CUALQUIERA"}
MAPA_GOB_EJE = {"EDAD-18-29": "EDAD-18-29", "EDAD-30-44": "EDAD-30-44", "EDAD-45-59": "EDAD-45-59",
                "EDAD-60-MAS": "EDAD-60-96",
                "ESCOLARIDAD-HASTA-PRIMARIA": "ESC-HASTA-PRIMARIA", "ESCOLARIDAD-SECUNDARIA": "ESC-SECUNDARIA",
                "ESCOLARIDAD-MEDIA-SUPERIOR": "ESC-MEDIA-SUPERIOR", "ESCOLARIDAD-SUPERIOR": "ESC-SUPERIOR"}


def _bytes(inputs: dict, iid: str) -> bytes:
    ent = inputs[iid]
    b = ent.get("bytes")
    return b if b is not None else Path(ent["ruta_absoluta"]).read_bytes()


def _resultados(inputs: dict, iid: str) -> dict:
    return json.loads(_bytes(inputs, iid).decode("utf-8"))["resultados"]


def _tabla(inputs: dict) -> list[dict]:
    texto = _bytes(inputs, INPUT_TABLA).decode("utf-8")
    return list(csv.DictReader(texto.splitlines(), delimiter="\t"))


def _celdas_yaml(inputs: dict) -> dict:
    """`MARG::<regla>::<desenlace>::<eje>::<categoria>` -> celda del yaml
    (misma identidad que construye `tools/marcador_segmento.py`)."""
    d = yaml.safe_load(_bytes(inputs, INPUT_YAML).decode("utf-8"))
    out = {}

    def camina(nodo, desenlace=""):
        if isinstance(nodo, dict):
            if "eje" in nodo and "celdas" in nodo:
                yield desenlace, nodo
            hijo = nodo.get("nombre") if ("nombre" in nodo and "ejes" in nodo) else None
            for k, v in nodo.items():
                if k != "nombre":
                    yield from camina(v, hijo or desenlace)
        elif isinstance(nodo, list):
            for e in nodo:
                yield from camina(e, desenlace)
    for r in d["reglas_propuestas"]:
        if "_ejes_" not in r.get("id", ""):
            continue
        for des, bloque in camina(r):
            for c in bloque.get("celdas") or []:
                suf = f"{des}::" if des else ""
                out[f"MARG::{r['id']}::{suf}{bloque['eje']}::{c['celda']}"] = c
    return out


def _ee(inf, sup) -> float:
    return (float(sup) - float(inf)) / (2.0 * Z95)


def _wilson(k: int, n: int) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    z2 = Z95 * Z95
    den = 1 + z2 / n
    centro = (p + z2 / (2 * n)) / den
    semi = Z95 * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n)) / den
    return (max(0.0, centro - semi), min(1.0, centro + semi))


def _clave(cell_id_R: str) -> tuple[str, str, str]:
    """('ENIF2024', 'D9', 'SEXO-1') desde `RESULT-ARBITRO-ENIF2024-D9-SEXO-1-P`."""
    s = cell_id_R[len("RESULT-ARBITRO-"):-2]
    inst, resto = s.split("-", 1)
    for des in ("INFORMAL-CUALQUIERA", "D9", "EVASION", "DENUNCIA", "DIGITAL"):
        if resto.startswith(des + "-"):
            return inst, des, resto[len(des) + 1:]
    raise KeyError(cell_id_R)


def _sellado(fila: dict, res_sell: dict) -> tuple[str, str, str] | None:
    inst, des, eje = _clave(fila["cell_id_R"])
    if fila["instrumento"] == "ENIF" and eje in MAPA_C2IC_EJE:
        b = f"RESULT-C2IC-ENIF2024-G-MARG-{MAPA_C2IC_DES[des]}-{MAPA_C2IC_EJE[eje]}"
        return (f"{b}-P", f"{b}-IC95INF", f"{b}-IC95SUP")
    if fila["instrumento"] == "ENCIG" and eje in MAPA_GOB_EJE:
        b = f"RESULT-GOB-EXE15-2025-MARGINAL-{MAPA_GOB_EJE[eje]}"
        return (f"{b}-P", f"{b}-P-IC-LO", f"{b}-P-IC-HI")
    return None


def _slug(v) -> str:
    return "".join(c if c.isalnum() else "-" for c in str(v)).strip("-").upper()


def celdas(inputs: dict) -> list[dict]:
    tabla = _tabla(inputs)
    R = {k: _resultados(inputs, v) for k, v in INPUTS_R.items()}
    P = {k: _resultados(inputs, v) for k, v in INPUTS_PISO.items()}
    S = {k: _resultados(inputs, v) for k, v in INPUTS_SELLADO.items()}
    Y = _celdas_yaml(inputs)
    out = []
    for f in tabla:
        r = R[f["instrumento"]]; p = P[f["calc_piso"]]
        rid, pid = f["cell_id_R"], f["cell_id_piso"]
        base_r, base_p = rid[:-2], pid[:-2]
        y = Y[f["marcador_celda_id"]]
        sel = _sellado(f, S)
        out.append({
            "fila": f, "inst": f["instrumento"], "des": _clave(rid)[1], "eje": f["axis"],
            "R": r[rid], "R_lo": r[base_r + "-IC-LO"], "R_hi": r[base_r + "-IC-HI"],
            "piso": p[pid], "piso_lo": p[base_p + "-IC-LO"], "piso_hi": p[base_p + "-IC-HI"],
            "gen1": y["p"],
            "sellado": (S[f["instrumento"]][sel[0]], S[f["instrumento"]][sel[1]], S[f["instrumento"]][sel[2]], sel[0]) if sel else None,
        })
    return out


def medir(inputs: dict, contrato: dict) -> dict:
    cs = celdas(inputs)
    out: dict = {}
    grupos: dict[str, list] = {}
    for c in cs:
        inst, des, eje = _clave(c["fila"]["cell_id_R"])
        b = f"{PREF}-{inst}-{des}-{eje}"
        R, piso = float(c["R"]), float(c["piso"])
        d = (R - piso) * 100.0
        ee = math.sqrt(_ee(c["R_lo"], c["R_hi"]) ** 2 + _ee(c["piso_lo"], c["piso_hi"]) ** 2) * 100.0
        lo, hi = d - Z95 * ee, d + Z95 * ee
        clase = "PERSISTE" if lo <= 0.0 <= hi else "CAMBIA"
        dentro = "DENTRO" if float(c["piso_lo"]) <= R <= float(c["piso_hi"]) else "FUERA"
        dg = R - float(c["gen1"])
        out[f"{b}-D-PP"] = d
        out[f"{b}-D-IC-LO-PP"] = lo
        out[f"{b}-D-IC-HI-PP"] = hi
        out[f"{b}-CLASE"] = clase
        out[f"{b}-R-EN-IC-PISO"] = dentro
        out[f"{b}-GEN1-P"] = float(c["gen1"])
        out[f"{b}-R-MENOS-GEN1"] = dg
        out[f"{b}-GEN1-COTEJO"] = "COINCIDE" if abs(dg) <= TOL_GEN1 else "DISCREPA"
        if c["sellado"] is not None:
            sp, slo, shi, sid = c["sellado"]
            ds = R - float(sp)
            dic = max(abs(float(c["R_lo"]) - float(slo)), abs(float(c["R_hi"]) - float(shi)))
            out[f"{b}-SELLADO-P"] = float(sp)
            out[f"{b}-R-MENOS-SELLADO"] = ds
            out[f"{b}-SELLADO-DELTA-IC-MAX"] = dic
            out[f"{b}-SELLADO-COTEJO"] = ("COINCIDE" if abs(ds) <= TOL_SELLADO else
                                          "COINCIDE-1E-3" if abs(ds) <= TOL_SELLADO_LAXA else "DISCREPA")
            out[f"{b}-SELLADO-FUENTE"] = sid
        rec = {"d": d, "abs": abs(d), "dentro": dentro == "DENTRO", "clase": clase,
               "gen1_coincide": abs(dg) <= TOL_GEN1, "abs_gen1": abs(dg)}
        for g in (f"{inst}", f"{inst}-DESENLACE-{des}", f"{inst}-EJE-{_slug(c['eje'])}"):
            grupos.setdefault(g, []).append(rec)

    for g, recs in grupos.items():
        n = len(recs); k = sum(1 for r in recs if r["dentro"])
        wlo, whi = _wilson(k, n)
        b = f"{PREF}-AGG-{g}"
        out[f"{b}-N"] = n
        out[f"{b}-D-MEDIO-PP"] = sum(r["d"] for r in recs) / n
        out[f"{b}-MAE-PP"] = sum(r["abs"] for r in recs) / n
        out[f"{b}-MAX-ABS-PP"] = max(r["abs"] for r in recs)
        out[f"{b}-N-DENTRO"] = k
        out[f"{b}-COBERTURA"] = k / n
        out[f"{b}-COBERTURA-IC-LO"] = wlo
        out[f"{b}-COBERTURA-IC-HI"] = whi
        out[f"{b}-N-PERSISTE"] = sum(1 for r in recs if r["clase"] == "PERSISTE")
        out[f"{b}-N-CAMBIA"] = sum(1 for r in recs if r["clase"] == "CAMBIA")
        out[f"{b}-GEN1-N-COINCIDE"] = sum(1 for r in recs if r["gen1_coincide"])
        out[f"{b}-GEN1-MAX-ABS"] = max(r["abs_gen1"] for r in recs)
    out[f"{PREF}-G-N-CELDAS"] = len(cs)
    out[f"{PREF}-G-N-CON-SELLADO-PILOTO"] = sum(1 for c in cs if c["sellado"] is not None)
    out[f"{PREF}-G-ROTULO"] = "PROSPECTIVA: piso sellado antes de que GEN2 midiera R"
    return out


def esquema_resultados(inputs: dict) -> list[dict]:
    """Los ids que `medir()` emite, derivados de la tabla de identidad (no
    del dato): sale el bloque `resultados:` de `spec.yaml`."""
    rows = []
    tabla = _tabla(inputs)
    grupos: list[str] = []
    for f in tabla:
        inst, des, eje = _clave(f["cell_id_R"])
        b = f"{PREF}-{inst}-{des}-{eje}"
        rows += [{"id": f"{b}-D-PP", "tipo": "flotante", "unidad": "puntos porcentuales (R menos piso)"},
                 {"id": f"{b}-D-IC-LO-PP", "tipo": "flotante", "unidad": "límite inferior IC95 de d, pp"},
                 {"id": f"{b}-D-IC-HI-PP", "tipo": "flotante", "unidad": "límite superior IC95 de d, pp"},
                 {"id": f"{b}-CLASE", "tipo": "texto", "unidad": "PERSISTE | CAMBIA"},
                 {"id": f"{b}-R-EN-IC-PISO", "tipo": "texto", "unidad": "DENTRO | FUERA (punto R en IC95 del piso)"},
                 {"id": f"{b}-GEN1-P", "tipo": "proporcion", "unidad": "p del árbitro GEN1 (yaml), misma celda"},
                 {"id": f"{b}-R-MENOS-GEN1", "tipo": "flotante", "unidad": "R menos p GEN1, en proporción"},
                 {"id": f"{b}-GEN1-COTEJO", "tipo": "texto", "unidad": "COINCIDE (|Δ| ≤ 5e-7) | DISCREPA"}]
        if _sellado(f, {}) is not None:
            rows += [{"id": f"{b}-SELLADO-P", "tipo": "proporcion", "unidad": "marginal de la ola nueva ya sellado por un piloto"},
                     {"id": f"{b}-R-MENOS-SELLADO", "tipo": "flotante", "unidad": "R menos el sellado del piloto, en proporción"},
                     {"id": f"{b}-SELLADO-DELTA-IC-MAX", "tipo": "flotante", "unidad": "máx |Δ| en los límites del IC95, en proporción"},
                     {"id": f"{b}-SELLADO-COTEJO", "tipo": "texto", "unidad": "COINCIDE (≤1e-6) | COINCIDE-1E-3 (≤1e-3) | DISCREPA"},
                     {"id": f"{b}-SELLADO-FUENTE", "tipo": "texto", "unidad": "id del RESULT sellado citado"}]
        for g in (f"{inst}", f"{inst}-DESENLACE-{des}", f"{inst}-EJE-{_slug(f['axis'])}"):
            if g not in grupos:
                grupos.append(g)
    for g in grupos:
        b = f"{PREF}-AGG-{g}"
        rows += [{"id": f"{b}-N", "tipo": "entero", "unidad": "celdas"},
                 {"id": f"{b}-D-MEDIO-PP", "tipo": "flotante", "unidad": "media de d, pp (error medio con signo)"},
                 {"id": f"{b}-MAE-PP", "tipo": "flotante", "unidad": "media de |d|, pp"},
                 {"id": f"{b}-MAX-ABS-PP", "tipo": "flotante", "unidad": "máx |d|, pp"},
                 {"id": f"{b}-N-DENTRO", "tipo": "entero", "unidad": "celdas con R dentro del IC95 del piso"},
                 {"id": f"{b}-COBERTURA", "tipo": "proporcion", "unidad": "N-DENTRO / N"},
                 {"id": f"{b}-COBERTURA-IC-LO", "tipo": "proporcion", "unidad": "IC95 binomial de Wilson, inferior"},
                 {"id": f"{b}-COBERTURA-IC-HI", "tipo": "proporcion", "unidad": "IC95 binomial de Wilson, superior"},
                 {"id": f"{b}-N-PERSISTE", "tipo": "entero", "unidad": "celdas PERSISTE (IC de d incluye 0)"},
                 {"id": f"{b}-N-CAMBIA", "tipo": "entero", "unidad": "celdas CAMBIA (IC de d excluye 0)"},
                 {"id": f"{b}-GEN1-N-COINCIDE", "tipo": "entero", "unidad": "celdas cuyo R coincide con el p GEN1 del yaml a 5e-7"},
                 {"id": f"{b}-GEN1-MAX-ABS", "tipo": "flotante", "unidad": "máx |R − p GEN1|, en proporción"}]
    rows += [{"id": f"{PREF}-G-N-CELDAS", "tipo": "entero", "unidad": "celdas enlazadas (SOLO-PISO en 55c8d57c)"},
             {"id": f"{PREF}-G-N-CON-SELLADO-PILOTO", "tipo": "entero", "unidad": "celdas con marginal de la ola nueva ya sellado por un piloto"},
             {"id": f"{PREF}-G-ROTULO", "tipo": "texto", "unidad": "rótulo de la adjudicación"}]
    return rows
