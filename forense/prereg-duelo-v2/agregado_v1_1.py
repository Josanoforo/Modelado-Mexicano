#!/usr/bin/env python3
"""Agregado sellado v1_1 sobre las 11 celdas de `marco-M-sorteado-v1_1.tsv`.

ACTO: MAESTRA33-E13 · AGREGA-1 (nube). Aplica, sin editarlo, el procedimiento
SELLADO `procedimiento-scoring-v1_1.md` (unidades z, agregado marginal por
corredor, comparación pareada L-vs-M en unidades z, PASO 2 únicamente,
`B` NO-APLICA, F-DD excluye VERIFICACION-NO-PUNTUA) más la banda/contrato F1
de `procedimiento-scoring-v1_0.md`.

Reutiliza, importadas y SIN editar, `generar_indices_bootstrap` y
`derivar_seed_scope` de `scoring-adv1-m3.py`. Los patrones `bootstrap_marginal`
(líneas ~769-802) y `bootstrap_pareado` (líneas ~826-886) del mismo módulo se
ADAPTAN aquí (no se importan) a `z = (punto-R)/EE(R)` y al indicador
`-0.5<=z<=0.5`, en vez de `celda.skills[corredor]` -- misma mecánica de
remuestreo, cantidad distinta, como el propio procedimiento sellado declara
que corresponde (§2, §3).

Parámetros SELLADOS, no elegidos por este script: delta=0.5 (banda en
unidades z), nivel_ic=0.95, seed=42, replicas=10000 (default técnico de
`scoring-adv1-m3.py` cuando se omite la clave).

Colapso de las 8 réplicas L por (celda, variante) en un punto de corredor:
NO APLICABLE en esta corrida -- ver hallazgo declarado abajo (`punto_l`
queda `None` para las 11 celdas x 2 variantes, mecánicamente, no por regla
inventada: `valor_extraido` es `null` en las 176 capturas reales de
`corridas-L/`, confirmado por censo exhaustivo. El propio `runner_l_cli.py`
(líneas ~124-129, `extraer_fuente_citada`) y `PAQUETE-L-v1_1.md:180`
declaran que el parseo de `valor_extraido` es trabajo de "un extractor
aparte, congelado antes de aplicarse" que ningún acto hasta hoy ha
construido para el marco-M v1_1 -- construirlo aquí, a partir de
`texto_crudo` en prosa libre, sería inventar una regla de extracción que el
procedimiento sellado no pide. Este script declara ese punto NO-DISPONIBLE
y dejar que el universo marginal L y el universo pareado salgan de tamaño 0
como consecuencia mecánica del dato, tal como el propio procedimiento
anticipa en su §6 ("Esa cuenta es consecuencia del dato, no una decisión de
este documento").

Uso:
    python3 forense/prereg-duelo-v2/agregado_v1_1.py
        -- lee corridas-R/, corridas-M/, corridas-L/ para las 11 celdas de
           marco-M-sorteado-v1_1.tsv, calcula el agregado, imprime un JSON
           determinista a stdout y lo escribe también en
           forense/prereg-duelo-v2/agregado-v1_1-resultado.json (A.13:
           declara cuántos archivos examinó).
"""
from __future__ import annotations

import csv
import importlib.util
import json
import math
import statistics
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent

_RUTA_MOTOR = DIR / "scoring-adv1-m3.py"
_SPEC = importlib.util.spec_from_file_location("scoring_adv1_m3", _RUTA_MOTOR)
_MOTOR = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _MOTOR
_SPEC.loader.exec_module(_MOTOR)  # scoring-adv1-m3.py NO se edita -- se importa por ruta

generar_indices_bootstrap = _MOTOR.generar_indices_bootstrap
derivar_seed_scope = _MOTOR.derivar_seed_scope

MARCO_TSV = DIR / "marco-M-sorteado-v1_1.tsv"
CORRIDAS_R = DIR / "corridas-R"
CORRIDAS_M = DIR / "corridas-M"
CORRIDAS_L = DIR / "corridas-L"

DELTA = 0.5
NIVEL_IC = 0.95
SEED = 42
REPLICAS = 10000

UNIVERSO_11 = [
    "CIV-M-01", "CIV-M-06", "CIV-M-08", "CIV-M-09", "CIV-M-11",
    "CIV-M-12", "CIV-M-13", "FAM-M-01", "TRA-M-03", "TRA-M-05", "TRA-M-07",
]
TRA_M_02 = "TRA-M-02"  # informativo, fuera del universo de 11 (FP-213)

VARIANTES_L = ("L-solo", "L+corpus")
K_REPLICAS_L = 8


def _leer_marco() -> dict[str, dict]:
    with MARCO_TSV.open(encoding="utf-8") as fh:
        filas = list(csv.DictReader(fh, delimiter="\t"))
    return {fila["id"]: fila for fila in filas}


def _leer_r(id_celda: str) -> dict | None:
    ruta = CORRIDAS_R / f"{id_celda}.json"
    if not ruta.exists():
        return None
    with ruta.open(encoding="utf-8") as fh:
        return json.load(fh)


def _leer_m(id_celda: str) -> dict | None:
    ruta = CORRIDAS_M / f"M-{id_celda}.json"
    if not ruta.exists():
        return None
    with ruta.open(encoding="utf-8") as fh:
        return json.load(fh)


def _leer_l_variante(id_celda: str, variante: str) -> tuple[float | None, int, int]:
    """Colapso mecánico de las 8 réplicas de (id_celda, variante) en un punto.

    Regla declarada: media de `valor_extraido` sobre las réplicas donde
    `valor_extraido` no es `null` (mismo verbo que `procedimiento-scoring
    -v1_1.md` usa para M: "un punto de corredor disponible"). Si CERO de las
    8 réplicas trae `valor_extraido` no-nulo, el punto de esa (celda,
    variante) es NO-DISPONIBLE -- no se sustituye por 0 ni por ningún otro
    valor.

    Retorna (punto_o_None, n_replicas_examinadas, n_replicas_con_valor).
    """
    valores: list[float] = []
    n_examinadas = 0
    variante_archivo = variante  # "L-solo" | "L+corpus", coincide con el nombre de archivo
    for k in range(1, K_REPLICAS_L + 1):
        ruta = CORRIDAS_L / f"L-{id_celda}-M__{variante_archivo}__{k:02d}.json"
        if not ruta.exists():
            continue
        n_examinadas += 1
        with ruta.open(encoding="utf-8") as fh:
            datos = json.load(fh)
        if datos.get("variante") != variante:
            raise ValueError(f"{ruta}: variante inesperada {datos.get('variante')!r}")
        v = datos.get("valor_extraido")
        if v is not None:
            valores.append(float(v))
    if not valores:
        return None, n_examinadas, 0
    return statistics.fmean(valores), n_examinadas, len(valores)


def _cuantil_7(ordenados: list[float], probabilidad: float) -> float:
    if len(ordenados) == 1:
        return float(ordenados[0])
    posicion = (len(ordenados) - 1) * probabilidad
    inferior = math.floor(posicion)
    superior = math.ceil(posicion)
    if inferior == superior:
        return float(ordenados[inferior])
    peso = posicion - inferior
    return float(ordenados[inferior] * (1 - peso) + ordenados[superior] * peso)


def _resumen_bootstrap(punto: float, replicas: list[float]) -> dict:
    ordenadas = sorted(replicas)
    cola = (1.0 - NIVEL_IC) / 2.0
    return {
        "punto": punto,
        "ic_lo": _cuantil_7(ordenadas, cola),
        "ic_hi": _cuantil_7(ordenadas, 1.0 - cola),
        "n_celdas": len(replicas) and len(ordenadas) or 0,
    }


def _bootstrap_proporcion_y_mediana(scope_id: str, zs: list[float]) -> dict:
    """Adapta `bootstrap_marginal` (scoring-adv1-m3.py:769-802) de
    `celda.skills[corredor]` a `z` y al indicador `dentro_de_banda(z)`."""
    n = len(zs)
    if n == 0:
        return {
            "n_celdas": 0,
            "proporcion_en_banda": None,
            "mediana_abs_z": None,
        }
    seed_scope = derivar_seed_scope(SEED, scope_id)
    indices = generar_indices_bootstrap(n, REPLICAS, seed_scope)
    indicador = [1.0 if -DELTA <= z <= DELTA else 0.0 for z in zs]
    abs_z = [abs(z) for z in zs]

    replicas_prop = [sum(indicador[i] for i in rep) / n for rep in indices]
    replicas_mediana = [statistics.median(abs_z[i] for i in rep) for rep in indices]

    prop_punto = sum(indicador) / n
    mediana_punto = statistics.median(abs_z)

    return {
        "n_celdas": n,
        "proporcion_en_banda": _resumen_bootstrap(prop_punto, replicas_prop),
        "mediana_abs_z": _resumen_bootstrap(mediana_punto, replicas_mediana),
    }


def _bootstrap_pareado_z(scope_id: str, pares: list[tuple[float, float]]) -> dict:
    """Adapta `bootstrap_pareado` (scoring-adv1-m3.py:826-886) a
    `dif_pareada_z = z_L - z_M`."""
    n = len(pares)
    if n == 0:
        return {"n_celdas": 0, "punto": None, "ic_lo": None, "ic_hi": None}
    seed_scope = derivar_seed_scope(SEED, scope_id)
    indices = generar_indices_bootstrap(n, REPLICAS, seed_scope)
    difs = [zl - zm for zl, zm in pares]
    replicas_dif = [sum(difs[i] for i in rep) / n for rep in indices]
    punto = statistics.fmean(difs)
    resumen = _resumen_bootstrap(punto, replicas_dif)
    return {"n_celdas": n, **resumen}


def _adjudicar(ic_lo: float | None, ic_hi: float | None) -> str:
    if ic_lo is None or ic_hi is None:
        return "SIN_CELDAS_PAREADAS"
    if ic_lo >= -DELTA and ic_hi <= DELTA:
        return "EQUIVALENTES-EN-BANDA"
    if ic_lo > DELTA:
        return "L-MAS-ALTO-QUE-M"
    if ic_hi < -DELTA:
        return "M-MAS-ALTO-QUE-L"
    if ic_lo <= 0 <= ic_hi:
        return "INDETERMINADO"
    return "POSICION_NO_DEFINIDA"


def main() -> dict:
    marco = _leer_marco()
    n_archivos_examinados = 0

    # F-DD: excluir VERIFICACION-NO-PUNTUA (§5 del procedimiento sellado)
    excluidas_dd = [
        cid for cid in UNIVERSO_11 if marco[cid]["grado_DD"] == "VERIFICACION-NO-PUNTUA"
    ]
    universo = [cid for cid in UNIVERSO_11 if cid not in excluidas_dd]

    celdas: dict[str, dict] = {}
    n_archivos_l_examinados = 0
    n_archivos_l_con_valor = 0

    for cid in universo:
        r = _leer_r(cid)
        n_archivos_examinados += 1
        m = _leer_m(cid)
        n_archivos_examinados += 1

        registro: dict = {"id_celda": cid, "R": None, "EE_R": None, "M": None, "z_M": None}

        if r is not None and r.get("estado") == "COMPUTADO":
            registro["R"] = r["R"]
            registro["EE_R"] = r["EE_R"]
        if m is not None:
            registro["M"] = m.get("valor_punto")
        if registro["R"] is not None and registro["EE_R"] and registro["M"] is not None:
            registro["z_M"] = (registro["M"] - registro["R"]) / registro["EE_R"]

        for variante in VARIANTES_L:
            punto, n_ex, n_con_valor = _leer_l_variante(cid, variante)
            n_archivos_l_examinados += n_ex
            n_archivos_l_con_valor += n_con_valor
            clave_punto = "L_solo" if variante == "L-solo" else "L_corpus"
            clave_z = "z_L_solo" if variante == "L-solo" else "z_L_corpus"
            registro[clave_punto] = punto
            registro["n_replicas_l_examinadas_" + clave_punto] = n_ex
            registro["n_replicas_l_con_valor_" + clave_punto] = n_con_valor
            if punto is not None and registro["R"] is not None and registro["EE_R"]:
                registro[clave_z] = (punto - registro["R"]) / registro["EE_R"]
            else:
                registro[clave_z] = None

        celdas[cid] = registro

    n_archivos_examinados += n_archivos_l_examinados

    # --- agregado marginal por corredor (§2) ---
    zs_m = [c["z_M"] for c in celdas.values() if c["z_M"] is not None]
    zs_l_solo = [c["z_L_solo"] for c in celdas.values() if c["z_L_solo"] is not None]
    zs_l_corpus = [c["z_L_corpus"] for c in celdas.values() if c["z_L_corpus"] is not None]

    marginal = {
        "M": _bootstrap_proporcion_y_mediana("marginal::M::v1_1", zs_m),
        "L_SOLO": _bootstrap_proporcion_y_mediana("marginal::L_SOLO::v1_1", zs_l_solo),
        "L_CORPUS": _bootstrap_proporcion_y_mediana("marginal::L_CORPUS::v1_1", zs_l_corpus),
    }

    # --- comparación principal pareada L_SOLO vs M (§3), unidades z ---
    pares_l_solo_m = [
        (c["z_L_solo"], c["z_M"])
        for c in celdas.values()
        if c["z_L_solo"] is not None and c["z_M"] is not None
    ]
    pareado = _bootstrap_pareado_z("pareado::L_SOLO_vs_M::v1_1", pares_l_solo_m)
    veredicto = _adjudicar(pareado.get("ic_lo"), pareado.get("ic_hi"))

    # --- TRA-M-02, informativo (FP-213), fuera del universo y del pareado ---
    r_tra02 = _leer_r(TRA_M_02)
    n_archivos_examinados += 1
    m_tra02 = _leer_m(TRA_M_02)
    n_archivos_examinados += 1
    tra_m_02 = {
        "id_celda": TRA_M_02,
        "R": r_tra02.get("R") if r_tra02 else None,
        "EE_R": r_tra02.get("EE_R") if r_tra02 else None,
        "M": m_tra02.get("valor_punto") if m_tra02 else None,
        "R_estado": "NO-ENCONTRADO" if r_tra02 is None else r_tra02.get("estado"),
        "nota": "Informativa (FP-213): no sorteada en marco-M-sorteado-v1_1 "
        "de 11 celdas, viene de esquema v1_0. No entra a ningún agregado ni "
        "al universo pareado de las 11.",
    }

    # --- conteo L∩M para FP-221: celdas de las 11 con punto real L (cualquier
    # variante) Y punto real M simultáneo ---
    interseccion_l_m = [
        cid
        for cid, c in celdas.items()
        if c["M"] is not None and (c["L_solo"] is not None or c["L_corpus"] is not None)
    ]

    resultado = {
        "parametros_sellados": {
            "delta": DELTA, "nivel_ic": NIVEL_IC, "seed": SEED, "replicas": REPLICAS,
        },
        "universo_11": universo,
        "excluidas_verificacion_no_puntua": excluidas_dd,
        "celdas": celdas,
        "agregado_marginal_por_corredor": marginal,
        "comparacion_principal_pareada": {
            "id": "L_SOLO_vs_M",
            "universo_pareado_ids": [
                cid for cid, c in celdas.items()
                if c["z_L_solo"] is not None and c["z_M"] is not None
            ],
            **pareado,
            "veredicto": veredicto,
        },
        "tra_m_02_informativo": tra_m_02,
        "conteo_l_interseccion_m_fp221": {
            "ids": interseccion_l_m,
            "n": len(interseccion_l_m),
            "umbral_activacion_corredor_e": 8,
            "cumple_umbral": len(interseccion_l_m) >= 8,
        },
        "hallazgo_declarado": {
            "valor_extraido_null_en_las_176_capturas_l": True,
            "n_archivos_l_examinados": n_archivos_l_examinados,
            "n_archivos_l_con_valor_extraido_no_nulo": n_archivos_l_con_valor,
            "razon": (
                "runner_l_cli.py declara valor_extraido=None por diseño "
                "(parseo delegado a 'un extractor aparte, congelado antes de "
                "aplicarse', PAQUETE-L-v1_1.md:180) -- ese extractor no existe "
                "en el repo para marco-M v1_1. Este acto no lo construye "
                "(inventaría una regla de extracción sobre prosa libre que el "
                "procedimiento sellado no pide). Consecuencia mecánica: "
                "universo marginal L = 0 celdas, universo pareado = 0 celdas, "
                "anticipado por procedimiento-scoring-v1_1.md §6."
            ),
        },
        "a13_conteo_archivos_examinados": {
            "corridas_R_y_M_11_celdas": 22,
            "corridas_R_y_M_TRA_M_02": 2,
            "corridas_L_examinadas": n_archivos_l_examinados,
            "total": n_archivos_examinados,
        },
    }
    return resultado


if __name__ == "__main__":
    resultado = main()
    salida = DIR / "agregado-v1_1-resultado.json"
    with salida.open("w", encoding="utf-8") as fh:
        json.dump(resultado, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps(resultado, ensure_ascii=False, indent=1, sort_keys=True))
