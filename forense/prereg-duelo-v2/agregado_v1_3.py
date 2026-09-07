#!/usr/bin/env python3
"""Agregado sellado v1_3 sobre las 14 celdas de `marco-M-sorteado-v1_3.tsv`.

ACTO: MAESTRA38-M13 · M-POR-CELDA PASOS 1 Y 2 (nube). Aplica el
procedimiento SELLADO `procedimiento-scoring-v1_2.md` (= `v1_1` verbatim +
la métrica secundaria D4, pre-registrada) sobre el enlace re-sellado
`enlace-M-v1_1.md`. Este script IMPORTA `agregado_v1_2.py` POR RUTA (mismo
patrón que `agregado_v1_2.py` usa para importar `agregado_v1_1.py`, que a
su vez usa para `agregado_v1_1b.py`) y no le toca ni una línea. Solo
sobreescribe, en la instancia importada, dos cosas:

  1. `MARCO_TSV` → `marco-M-sorteado-v1_3.tsv` (mismas 14 celdas, tres con
     la columna `conducta` re-apuntada por `enlace-M-v1_1.md`:
     `TRA-M-02`/`TRA-M-03`/`TRA-M-07` de `paga_mordida` a
     `paga_mordida_encig2025`).
  2. `_leer_m` → resolución POR ARCHIVO en el orden exacto del §16 del
     encargo final `MAESTRA38-M13 · M-POR-CELDA v1.3`:
     `M-<id>__v1_3.json` → `M-<id>.json` → `M-<id>__v1_2.json`, primera
     coincidencia exacta. Las tres celdas re-apuntadas resuelven a
     `__v1_3` (materializadas por `tools.emite_m.emite_celda` en el
     COMMIT 2 de ese acto); las 11 restantes reproducen las fuentes de
     v1.2, porque ninguna tiene `__v1_3`. El resultado incluye
     `fuente_M_por_celda` con los 14 IDs, que es la prueba mecánica del
     control §19-F.

     ANTES (`PR #592`) este script calculaba el `M` de las tres celdas EN
     MEMORIA vía `emitir_binaria`, sin escribir nada bajo `corridas-M/`.
     La `ENMIENDA-1` del encargo corrige esa premisa: el agregado lee
     archivos, así que un `M` que sólo vive en memoria no deja registro
     auditable, ni cita, ni `ola_calibracion`, ni `grado_DD`.

Y AÑADE, sin tocar nada de lo que `agregado_v1_2.py`/`agregado_v1_1.py`
calculan, la métrica secundaria pre-registrada por
`procedimiento-scoring-v1_2.md` §7 (D4): `err_pp = 100·(corredor − R)` por
celda, `MAE_pp` por corredor sobre las 14, y la comparación pareada de
`MAE_pp` (`L-solo vs M`, `L+corpus vs M`) por bootstrap, mismos parámetros
sellados (`seed=42`, `nivel_ic=0.95`, `replicas=10000`) que el resto del
duelo. La banda `z` de v1.1 (heredada de `agregado_v1_2.main()`) sigue
siendo el veredicto primario y **no se toca** — la métrica secundaria no
adjudica "en banda", solo ordena corredores por error absoluto medio en
puntos porcentuales (§7 del procedimiento).

Uso::

    python3 forense/prereg-duelo-v2/agregado_v1_3.py
        -- escribe agregado-v1_3-resultado.json y lo imprime a stdout.
"""
from __future__ import annotations

import importlib.util
import json
import statistics
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
REPO_ROOT = DIR.parents[1]
sys.path.insert(0, str(REPO_ROOT))

_RUTA_AGREGADO = DIR / "agregado_v1_2.py"
_SPEC = importlib.util.spec_from_file_location("agregado_v1_2_base_para_v1_3", _RUTA_AGREGADO)
_BASE = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _BASE
_SPEC.loader.exec_module(_BASE)  # agregado_v1_2.py NO se edita -- se importa por ruta

# NOTA: este modulo ya NO importa milpa.src.emisor. El M de las tres celdas
# re-apuntadas se lee de corridas-M/M-<id>__v1_3.json, emitido por
# tools/emite_m.py -- que es el unico que habla con el motor. Ver §16.

MARCO_TSV_V1_3 = DIR / "marco-M-sorteado-v1_3.tsv"

CONDUCTA_NUEVA = "paga_mordida_encig2025"
IDS_REAPUNTADOS = ("TRA-M-02", "TRA-M-03", "TRA-M-07")

# --- 1) marco: sobreescribe el VALOR de la constante en el modulo v1_2
#     importado (que a su vez sobreescribio el modulo v1_1), sin tocar
#     ningun archivo .py existente -----------------------------------------
_BASE.MARCO_TSV = MARCO_TSV_V1_3
_BASE._BASE.MARCO_TSV = MARCO_TSV_V1_3  # el modulo base (agregado_v1_1) tambien lee esta constante

# --- 2) M: resolucion POR ARCHIVO, en el orden exacto del §16 -----------
#
# ACTO MAESTRA38-M13 · M-POR-CELDA v1.3 (encargo final, §2/§15/§16).
# Antes este script calculaba el M de las tres celdas re-apuntadas EN
# MEMORIA (`emitir_binaria`), sin escribir nada bajo `corridas-M/`. La
# ENMIENDA-1 corrige la premisa: la cadena real del duelo es
#
#   marco -> tools/emite_m.py::emite_celda -> milpa.src.emisor.emitir_binaria
#         -> corridas-M/M-<id>*.json -> agregado::_leer_m
#
# es decir, el agregado lee ARCHIVOS, y un M que solo vive en memoria no
# deja registro auditable ni cita, ni `ola_calibracion`, ni `grado_DD`.
# El COMMIT 2 de este acto materializo los tres `M-<id>__v1_3.json` con
# `tools.emite_m.emite_celda`; aqui se consumen desde disco.
#
# §16, literal: "Para cada celda, buscar en este orden: 1. M-<id>__v1_3.json
# 2. M-<id>.json 3. M-<id>__v1_2.json. Primera coincidencia exacta. No otra
# heuristica." Para las 11 no afectadas el resultado es identico al de
# `agregado_v1_2._leer_m_v1_2` (que prueba `M-<id>.json` y luego
# `M-<id>__v1_2.json`), porque ninguna de ellas tiene `__v1_3`.
ORDEN_RESOLUCION_M = ("M-{id}__v1_3.json", "M-{id}.json", "M-{id}__v1_2.json")


def _ruta_m(id_celda: str) -> Path | None:
    """Primera coincidencia EXACTA del orden de §16, o None."""
    for patron in ORDEN_RESOLUCION_M:
        ruta = _BASE._BASE.CORRIDAS_M / patron.format(id=id_celda)
        if ruta.exists():
            return ruta
    return None


def _fuente_m(id_celda: str) -> str | None:
    ruta = _ruta_m(id_celda)
    return None if ruta is None else str(ruta.relative_to(DIR.parents[1]))


def _leer_m_v1_3(id_celda: str):
    ruta = _ruta_m(id_celda)
    if ruta is None:
        return None
    with ruta.open(encoding="utf-8") as fh:
        return json.load(fh)


_BASE._BASE._leer_m = _leer_m_v1_3


# ── Métrica secundaria D4 (procedimiento-scoring-v1_2.md §7) ───────────────

DELTA = _BASE._BASE.DELTA
NIVEL_IC = _BASE._BASE.NIVEL_IC
SEED = _BASE._BASE.SEED
REPLICAS = _BASE._BASE.REPLICAS
generar_indices_bootstrap = _BASE._BASE.generar_indices_bootstrap
derivar_seed_scope = _BASE._BASE.derivar_seed_scope
_resumen_bootstrap = _BASE._BASE._resumen_bootstrap


def _mae_pp_bootstrap(scope_id: str, errores_pp: list[float]) -> dict:
    n = len(errores_pp)
    if n == 0:
        return {"n_celdas": 0, "mae_pp": None}
    seed_scope = derivar_seed_scope(SEED, scope_id)
    indices = generar_indices_bootstrap(n, REPLICAS, seed_scope)
    abs_err = [abs(e) for e in errores_pp]
    replicas_mae = [statistics.fmean(abs_err[i] for i in rep) for rep in indices]
    punto = statistics.fmean(abs_err)
    return {"n_celdas": n, "mae_pp": _resumen_bootstrap(punto, replicas_mae)}


def _dif_mae_pp_pareada_bootstrap(scope_id: str, pares_abs_err: list[tuple[float, float]]) -> dict:
    """dif = |err_pp_corredor| - |err_pp_M|, bootstrapeada -- mismo patron
    que _bootstrap_pareado_z del modulo base, cantidad distinta (D4)."""
    n = len(pares_abs_err)
    if n == 0:
        return {"n_celdas": 0, "punto": None, "ic_lo": None, "ic_hi": None}
    seed_scope = derivar_seed_scope(SEED, scope_id)
    indices = generar_indices_bootstrap(n, REPLICAS, seed_scope)
    difs = [a - b for a, b in pares_abs_err]
    replicas_dif = [statistics.fmean(difs[i] for i in rep) for rep in indices]
    punto = statistics.fmean(difs)
    return {"n_celdas": n, **_resumen_bootstrap(punto, replicas_dif)}


def _metrica_secundaria_pp(resultado: dict) -> dict:
    celdas = resultado["celdas"]
    err_pp: dict[str, dict[str, float | None]] = {}
    for cid, c in celdas.items():
        R = c.get("R")
        fila = {"R": R}
        for clave_punto, clave_err in (
            ("M", "err_pp_M"),
            ("L_solo", "err_pp_L_solo"),
            ("L_corpus", "err_pp_L_corpus"),
        ):
            punto = c.get(clave_punto)
            fila[clave_err] = 100.0 * (punto - R) if (punto is not None and R is not None) else None
        err_pp[cid] = fila

    mae_por_corredor = {
        "M": _mae_pp_bootstrap(
            "mae_pp::M::v1_3", [f["err_pp_M"] for f in err_pp.values() if f["err_pp_M"] is not None]
        ),
        "L_SOLO": _mae_pp_bootstrap(
            "mae_pp::L_SOLO::v1_3",
            [f["err_pp_L_solo"] for f in err_pp.values() if f["err_pp_L_solo"] is not None],
        ),
        "L_CORPUS": _mae_pp_bootstrap(
            "mae_pp::L_CORPUS::v1_3",
            [f["err_pp_L_corpus"] for f in err_pp.values() if f["err_pp_L_corpus"] is not None],
        ),
    }

    pares_l_solo_m = [
        (abs(f["err_pp_L_solo"]), abs(f["err_pp_M"]))
        for f in err_pp.values()
        if f["err_pp_L_solo"] is not None and f["err_pp_M"] is not None
    ]
    pares_l_corpus_m = [
        (abs(f["err_pp_L_corpus"]), abs(f["err_pp_M"]))
        for f in err_pp.values()
        if f["err_pp_L_corpus"] is not None and f["err_pp_M"] is not None
    ]

    comparacion_l_solo = _dif_mae_pp_pareada_bootstrap(
        "mae_pp::pareado::L_SOLO_vs_M::v1_3", pares_l_solo_m
    )
    comparacion_l_corpus = _dif_mae_pp_pareada_bootstrap(
        "mae_pp::pareado::L_CORPUS_vs_M::v1_3", pares_l_corpus_m
    )

    def _ordena(dif: dict) -> str:
        ic_lo, ic_hi = dif.get("ic_lo"), dif.get("ic_hi")
        if ic_lo is None or ic_hi is None:
            return "SIN_CELDAS_PAREADAS"
        if ic_lo <= 0 <= ic_hi:
            return "INDETERMINADO"
        if ic_hi < 0:
            return "L-MENOR-ERROR-PP-QUE-M"
        return "M-MENOR-ERROR-PP-QUE-L"

    return {
        "definicion": "err_pp = 100*(corredor - R) por celda, con signo; MAE_pp = media de |err_pp| "
        "sobre el universo de 14 (o el subconjunto con punto de corredor disponible); comparacion "
        "pareada = bootstrap de la diferencia |err_pp_corredor| - |err_pp_M| sobre celdas con ambos "
        "puntos disponibles, mismos parametros sellados (seed=42, nivel_ic=0.95, replicas=10000). "
        "Diagnostico, NO gating -- el veredicto primario sigue siendo la banda z de "
        "comparacion_principal_pareada, sin tocar.",
        "err_pp_por_celda": err_pp,
        "mae_pp_por_corredor": mae_por_corredor,
        "comparacion_pareada_mae_pp": {
            "L_SOLO_vs_M": {"universo_pareado_n": len(pares_l_solo_m), **comparacion_l_solo,
                             "orden": _ordena(comparacion_l_solo)},
            "L_CORPUS_vs_M": {"universo_pareado_n": len(pares_l_corpus_m), **comparacion_l_corpus,
                               "orden": _ordena(comparacion_l_corpus)},
        },
    }


def main() -> dict:
    resultado = _BASE.main()
    resultado["version_marco"] = "v1_3"
    resultado["version_enlace"] = "v1_1 (enlace-M-v1_1.md -- TRA-M-02/03/07 re-apuntadas a "
    resultado["version_enlace"] += "paga_mordida_encig2025)"
    resultado["version_scoring"] = "v1_2 (procedimiento-scoring-v1_2.md -- z primaria sin cambio, "
    resultado["version_scoring"] += "metrica secundaria pp anadida, D4)"
    resultado["reapuntadas"] = list(IDS_REAPUNTADOS)

    # §16: "Anadir al resultado fuente_M_por_celda ... Debe contener
    # exactamente los 14 IDs del universo." Se deriva del UNIVERSO, no del
    # orden en que `_leer_m` fue llamado, para que sea exactamente 14 y
    # deterministico. Es la prueba mecanica del control §19-F.
    universo = list(_BASE.UNIVERSO_V1_2)
    resultado["fuente_M_por_celda"] = {cid: _fuente_m(cid) for cid in universo}
    resultado["orden_resolucion_M"] = {
        "orden": list(ORDEN_RESOLUCION_M),
        "regla": ("primera coincidencia exacta, sin otra heuristica (encargo "
                   "MAESTRA38-M13 §16). Para las 11 celdas no afectadas reproduce "
                   "las fuentes de v1.2, porque ninguna tiene __v1_3."),
        "reapuntadas_usan_v1_3": sorted(
            cid for cid in universo
            if (resultado["fuente_M_por_celda"].get(cid) or "").endswith("__v1_3.json")),
    }
    faltan = [cid for cid, f in resultado["fuente_M_por_celda"].items() if f is None]
    if faltan:
        raise LookupError(f"sin archivo M para {faltan} -- §16 exige los 14 IDs resueltos")
    if len(resultado["fuente_M_por_celda"]) != 14:
        raise AssertionError("fuente_M_por_celda debe traer exactamente los 14 IDs del universo")

    resultado["metrica_secundaria_pp_d4"] = _metrica_secundaria_pp(resultado)
    return resultado


if __name__ == "__main__":
    resultado = main()
    salida = DIR / "agregado-v1_3-resultado.json"
    with salida.open("w", encoding="utf-8") as fh:
        json.dump(resultado, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps(resultado, ensure_ascii=False, indent=1, sort_keys=True))
