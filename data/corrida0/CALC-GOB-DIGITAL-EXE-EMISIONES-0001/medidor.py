#!/usr/bin/env python3
"""CALC-GOB-DIGITAL-EXE-EMISIONES-0001 · piloto 3 · emisiones de candidatos.

CONGELADO SIN MICRODATO por `ACTO GEN2-CELDA-D-PILOTO-3-P0` (20/sep/2026).
`medidor_ejecutado_al_congelar: NO` — este archivo no se corrió al escribirse y no
produjo un solo resultado.

DOS CONDICIONES SUSPENSIVAS (adenda de mesa, 20/sep/2026). `_guardia_suspensiva()`
las hace mecánicas: el módulo REHÚSA correr mientras no se le pasen firmadas.

  S1  COMMIT-2 no corre hasta que NC-0355 cierre con MISMO-INSTRUMENTO o CAMBIO-MENOR.
      Si cierra CAMBIO-DE-INSTRUMENTO, esta spec se retira SIN CORRER
      (SUPERADO, n_resultados=0): no se enmienda, no se adapta, no se reusa.
  S2  Primera lectura de caja, ANTES que P0: qué significan 97/98/99 por ola. Si alguno
      es edad real censurada, F1-bis está sacando población del universo y eso se
      reporta a mesa ANTES de emitir. La rejilla sellada del árbitro (60-96) no se toca.

F3: quien congeló este COMMIT-1 no ejecuta COMMIT-2 ni COMMIT-3.

Unidad de análisis = TRÁMITE. Quien hizo doce trámites contribuye doce veces.
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

# ─── contrato de desenlace, idéntico al de 2021/2023 y al medidor de 2025 ───
ADOPTA = {"4", "5"}            # internet/app · cajero o kiosco inteligente
NO_ADOPTA = {"1", "2", "6"}    # instalaciones · banco o tienda · módulos móviles
TELEFONO = {"3"}               # FUERA del universo: canal remoto atendido
UNIVERSO_PRINCIPAL = {"01"}    # N_TRA: pago ordinario del servicio de luz

# ─── rejilla, idéntica a la congelada en las dos olas históricas ───
EDAD_BANDAS = [("18-29", 18, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60-96", 60, 96)]
NIV_AGREGADO = {"HASTA-PRIMARIA": {"0", "1", "2"}, "SECUNDARIA": {"3"},
                "MEDIA-SUPERIOR": {"4", "5", "6", "7"}, "SUPERIOR": {"8", "9"}}
EDADES = [b[0] for b in EDAD_BANDAS]
ESCOLARIDADES = list(NIV_AGREGADO)

# ─── parámetros congelados (no se teclean: derivados en la spec §3.1) ───
LAMBDA = 0.8937949410086089           # tau2/(tau2+sigma_bar2) sobre las 15 celdas PUNTUADA
N_MINIMO = 200
OLAS_SOPORTE = ("2021", "2023", "2025")
FUERA_DE_SOPORTE_GLOBAL_SI_FALLAN = 5
FRACCION_PARA_GANAR = 0.75
DELTA_MAE_UMBRAL_PP = 0.5
FUERA_DE_SOPORTE_EX_ANTE = {("18-29", "HASTA-PRIMARIA")}
BOOTSTRAP_REPLICAS = 10000


class ParoDeGuardia(RuntimeError):
    """Se levanta cuando una condición suspensiva no está satisfecha."""


def _guardia_suspensiva(s1_veredicto: str, s2_codigos_leidos: dict) -> None:
    """Hace mecánicas S1 y S2. Sin esto, el módulo no mide.

    s1_veredicto: veredicto de NC-0355 (P0), leído del texto de los cuestionarios.
    s2_codigos_leidos: {"2021": {...}, "2023": {...}, "2025": {...}}, cada uno con
        el significado por texto de 97, 98 y 99 y la clave `edad_real_censurada`
        (bool) que dice si ALGUNO de los tres es edad real.
    """
    if s1_veredicto == "CAMBIO-DE-INSTRUMENTO":
        raise ParoDeGuardia(
            "S1: NC-0355 cerró CAMBIO-DE-INSTRUMENTO. Esta spec se RETIRA SIN CORRER "
            "(SUPERADO, n_resultados=0). No se enmienda ni se reusa."
        )
    if s1_veredicto not in ("MISMO-INSTRUMENTO", "CAMBIO-MENOR"):
        raise ParoDeGuardia(
            f"S1: NC-0355 no ha cerrado con un veredicto habilitante "
            f"(recibido: {s1_veredicto!r}). COMMIT-2 no corre."
        )
    faltan = [o for o in ("2021", "2023", "2025") if o not in s2_codigos_leidos]
    if faltan:
        raise ParoDeGuardia(
            f"S2: falta la lectura por texto de 97/98/99 en {faltan}. "
            "Es la PRIMERA lectura de caja, antes que P0."
        )
    censura = [o for o, v in s2_codigos_leidos.items() if v.get("edad_real_censurada")]
    if censura:
        raise ParoDeGuardia(
            f"S2: en {censura} al menos uno de 97/98/99 es EDAD REAL CENSURADA, así que "
            "F1-bis está sacando población del universo. Se REPORTA A MESA ANTES DE "
            "EMITIR. La rejilla sellada del árbitro (60-96) no se toca aquí."
        )


def _logit(p):
    return np.log(np.asarray(p, dtype=float) / (1.0 - np.asarray(p, dtype=float)))


def _expit(x):
    return 1.0 / (1.0 + np.exp(-np.asarray(x, dtype=float)))


def _banda_edad(edad):
    for nombre, lo, hi in EDAD_BANDAS:
        if lo <= edad <= hi:
            return nombre
    return None   # F1-bis: fuera de las cuatro bandas -> FUERA DEL UNIVERSO


def _prepara(sec7: pd.DataFrame, residentes: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Aplica universo, desenlace y rejilla. Devuelve el marco y el residuo declarado."""
    df = sec7[sec7["N_TRA"].astype(str).str.zfill(2).isin(UNIVERSO_PRINCIPAL)].copy()
    canal = df["P7_3"].astype(str).str.strip()
    df = df[canal.isin(ADOPTA | NO_ADOPTA)].copy()       # {3} y {7,8,9,blanco} fuera
    df["_y"] = canal[canal.isin(ADOPTA | NO_ADOPTA)].isin(ADOPTA).astype(float)
    df["_w"] = df["FAC_TRA"].astype(float)

    df = df.merge(residentes[["EDAD", "NIV"]], left_index=True, right_index=True, how="left")
    df["_edad"] = pd.to_numeric(df["EDAD"], errors="coerce").map(
        lambda e: _banda_edad(e) if pd.notna(e) else None)
    niv = df["NIV"].astype(str).str.strip()
    df["_esc"] = niv.map({c: k for k, cs in NIV_AGREGADO.items() for c in cs})

    completo = df["_edad"].notna() & df["_esc"].notna()
    residuo = {
        "residuo_edad_n": int((df["_esc"].notna() & df["_edad"].isna()).sum()),
        "residuo_edad_masa": float(df.loc[df["_esc"].notna() & df["_edad"].isna(), "_w"].sum()),
        "residuo_esc_n": int((df["_edad"].notna() & df["_esc"].isna()).sum()),
        "residuo_esc_masa": float(df.loc[df["_edad"].notna() & df["_esc"].isna(), "_w"].sum()),
        "n_completos": int(completo.sum()),
    }
    return df[completo].copy(), residuo


def _marginales(frame: pd.DataFrame) -> dict:
    """Marginales RECALCULADOS sobre el universo del cruce (F1-bis), no los sellados."""
    out = {}
    for eje, cats in (("_edad", EDADES), ("_esc", ESCOLARIDADES)):
        for cat in cats:
            sel = frame[frame[eje].eq(cat)]
            den = float(sel["_w"].sum())
            out[(eje, cat)] = (float((sel["_w"] * sel["_y"]).sum()) / den) if den > 0 else math.nan
    den = float(frame["_w"].sum())
    out["_all"] = (float((frame["_w"] * frame["_y"]).sum()) / den) if den > 0 else math.nan
    return out


def c2_replica(frame: pd.DataFrame) -> dict:
    """C2 = piso a vencer. Ausencia de interacción en logit, réplica por réplica.

    p(a,b) = expit(logit p_a + logit p_b - logit p_all). NO es independencia
    multiplicativa: esa forma no preserva el rango (FP-379 D2).
    """
    m = _marginales(frame)
    out = {}
    for a in EDADES:
        for b in ESCOLARIDADES:
            out[(a, b)] = float(_expit(_logit(m[("_edad", a)]) + _logit(m[("_esc", b)])
                                       - _logit(m["_all"])))
    return out


def retadores(c2: dict, delta_23: dict, delta_barra: dict) -> dict:
    """S½ y Sλ, sobre el C2 de la misma réplica. λ congelada, no se teclea."""
    s_medio, s_lambda = {}, {}
    for k, base in c2.items():
        s_medio[k] = float(_expit(_logit(base) + 0.5 * delta_23[k]))
        s_lambda[k] = float(_expit(_logit(base) + LAMBDA * delta_barra[k]))
    return {"S-MEDIO": s_medio, "S-LAMBDA": s_lambda}


def clasifica_soporte(n_por_ola: dict) -> dict:
    """PUNTUADA si n >= 200 en 2021, 2023 y 2025. El tercero solo se sabe aquí."""
    estado = {}
    for celda in ((a, b) for a in EDADES for b in ESCOLARIDADES):
        if celda in FUERA_DE_SOPORTE_EX_ANTE:
            estado[celda] = "FUERA-DE-SOPORTE-EX-ANTE"
            continue
        if all(n_por_ola.get(ola, {}).get(celda, 0) >= N_MINIMO for ola in OLAS_SOPORTE):
            estado[celda] = "PUNTUADA"
        else:
            estado[celda] = "FUERA-DE-SOPORTE"
    fallan = sum(1 for c, e in estado.items()
                 if e == "FUERA-DE-SOPORTE" and c not in FUERA_DE_SOPORTE_EX_ANTE)
    estado["_GLOBAL"] = ("FUERA-DE-SOPORTE-GLOBAL"
                         if fallan >= FUERA_DE_SOPORTE_GLOBAL_SI_FALLAN else "CON-SOPORTE")
    return estado


def medir(inputs: dict, contrato: dict) -> dict:
    """Punto de entrada del COMMIT-2. NO SE EJECUTÓ en el COMMIT-1."""
    _guardia_suspensiva(contrato["s1_veredicto"], contrato["s2_codigos_leidos"])
    raise NotImplementedError(
        "COMMIT-2: el cuerpo de medición se completa en la sesión de caja que abra el "
        "microdato, con el contrato de arriba congelado. F3: no la de este acto."
    )
