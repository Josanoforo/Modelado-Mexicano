#!/usr/bin/env python3
"""Adaptador marco-M -> entrada de `forense/prereg-duelo-v2/scoring-adv1-m3.py`.

`ACTO MAESTRA33-E8 · SCORE-M-1`. Este script NO edita `scoring-adv1-m3.py`
(sellado, `ADR-209`/`ADR-225`/`ADR-226`) y no emite `M`, `R` ni `L` -- solo
lee lo que ya existe en el árbol y arma:

  1. Un censo por celda del universo `marco-M-sorteado-v1_1.tsv` (más
     `marco-M-sorteado-v1_0.tsv`, declarado aparte por venir de un esquema
     anterior a F-DD, sin columna `grado_DD`/`elegible_v1_1`): qué
     corredores tiene disponibles (`M`/`R`/`L`, banderas booleanas), si
     está marcada `VERIFICACION-NO-PUNTUA` bajo F-DD (`ADR-237`, columna
     `grado_DD`) y si es "puntuable" bajo la regla de este acto: **R
     presente, más al menos uno de M o L**. Ninguna celda VERIFICACION-
     NO-PUNTUA entra al cómputo de puntuables aunque tenga R+M/L.
  2. La `entrada.json` que `scoring-adv1-m3.py` espera (dos claves,
     `configuracion` y `celdas`), con `nivel_ic=0.95`/`seed=42`
     (`FP-168`, FIRMADA 30/ago/2026) ya poblados y `delta` deliberadamente
     ausente -- sigue sin tener cita como escalar único de corrida
     (`procedimiento-scoring-v1_0.md` §3); no se inventa aquí tampoco.
     Las celdas puntuables llevan `mediciones: {}` por la misma razón que
     `intento_scoring_e9.py`: sin corredor `B` (baseline) no hay una
     `skill` normalizada legítima que poblar (§4 del procedimiento).

Uso::

    python3 tools/score_marco_m.py [--marco v1_1] [--json salida.json]

Sin argumentos, censa `marco-M-sorteado-v1_1.tsv` y escribe el censo + la
entrada de scoring a stdout (JSON). Determinista: mismo árbol -> misma
salida (orden de celdas por `id_celda`, sin timestamps).
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

RAIZ = Path(__file__).resolve().parents[1]
PREREG = RAIZ / "forense" / "prereg-duelo-v2"
CORRIDAS_M = PREREG / "corridas-M"
CORRIDAS_R = PREREG / "corridas-R"
CORRIDAS_L = PREREG / "corridas-L"

NIVEL_IC_FP168 = 0.95
SEED_FP168 = 42


def _leer_tsv(ruta: Path) -> list[dict[str, str]]:
    if not ruta.exists():
        return []
    with ruta.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def _es_no_puntua_dd(fila: dict[str, str]) -> bool:
    grado_dd = (fila.get("grado_DD") or "").upper()
    return "NO-PUNTUA" in grado_dd or "NO_PUNTUA" in grado_dd


def _m_disponible(id_celda: str) -> dict[str, Any]:
    ruta = CORRIDAS_M / f"M-{id_celda}.json"
    if not ruta.exists():
        return {"disponible": False, "estado_M": None, "valor_punto": None}
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    estado = datos.get("estado_M")
    return {
        "disponible": estado == "EMITE",
        "estado_M": estado,
        "valor_punto": datos.get("valor_punto") if estado == "EMITE" else None,
    }


def _r_disponible(id_celda: str) -> dict[str, Any]:
    ruta = CORRIDAS_R / f"{id_celda}.json"
    if not ruta.exists():
        return {"disponible": False, "estado": None, "R": None, "EE_R": None}
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    estado = datos.get("estado")
    return {
        "disponible": estado == "COMPUTADO",
        "estado": estado,
        "R": datos.get("R") if estado == "COMPUTADO" else None,
        "EE_R": datos.get("EE_R") if estado == "COMPUTADO" else None,
    }


def _l_disponible(id_celda: str) -> dict[str, Any]:
    if not CORRIDAS_L.exists():
        return {"disponible": False, "n_corridas": 0, "archivos": []}
    archivos = sorted(CORRIDAS_L.glob(f"{id_celda}__L-*__*.json"))
    return {
        "disponible": len(archivos) > 0,
        "n_corridas": len(archivos),
        "archivos": [archivo.name for archivo in archivos],
    }


def censar_universo(filas_marco: list[dict[str, str]], schema_dd: bool) -> list[dict[str, Any]]:
    censo: list[dict[str, Any]] = []
    for fila in sorted(filas_marco, key=lambda f: f["id"]):
        id_celda = fila["id"]
        no_puntua_dd = _es_no_puntua_dd(fila) if schema_dd else False
        m = _m_disponible(id_celda)
        r = _r_disponible(id_celda)
        l = _l_disponible(id_celda)
        puntuable = (not no_puntua_dd) and r["disponible"] and (m["disponible"] or l["disponible"])
        censo.append(
            {
                "id_celda": id_celda,
                "schema_con_grado_dd": schema_dd,
                "grado_DD": fila.get("grado_DD") if schema_dd else "SIN-COLUMNA (esquema pre-F-DD)",
                "verificacion_no_puntua": no_puntua_dd,
                "corredores": {"M": m, "R": r, "L": l},
                "puntuable": puntuable,
            }
        )
    return censo


def construir_entrada_scoring(censo: list[dict[str, Any]]) -> dict[str, Any]:
    """Arma `entrada.json` para `scoring-adv1-m3.py` -- `delta` deliberadamente ausente.

    Los corredores obligatorios del contrato F1 (`{(L,solo):1,(M,principal):1}`)
    se declaran activos siempre, sea cual sea la disponibilidad real de datos
    por celda -- eso lo decide `construir_matriz_mediciones` celda por celda,
    no la declaración de corredores (misma lectura que `intento_scoring_e9.py`).
    Ninguna celda `VERIFICACION-NO-PUNTUA` entra a `celdas`.
    """
    configuracion = {
        "corredores_activos": [
            {"id": "L_SOLO", "familia": "L", "variante": "solo"},
            {"id": "M", "familia": "M", "variante": "principal"},
        ],
        "comparaciones_l_m": [
            {"id": "L_SOLO_vs_M", "l_id": "L_SOLO", "m_id": "M"},
        ],
        "comparacion_principal_id": "L_SOLO_vs_M",
        "e_id": None,
        "nivel_ic": NIVEL_IC_FP168,
        "seed": SEED_FP168,
        # "delta": deliberadamente ausente -- sigue sin escalar único
        # citado por mesa (procedimiento-scoring-v1_0.md §3). No se inventa.
    }
    celdas = []
    for entrada in censo:
        if entrada["verificacion_no_puntua"]:
            continue
        # Sin baseline B (mismo hallazgo estructural de E9, §4 del
        # procedimiento): no hay skill normalizada legítima que poblar.
        # mediciones vacío es la representación honesta de ese hueco.
        celdas.append(
            {"id_celda": entrada["id_celda"], "estado": "EVALUABLE", "mediciones": {}}
        )
    return {"configuracion": configuracion, "celdas": celdas}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--marco",
        default="v1_1",
        help="sufijo de marco-M-sorteado-<sufijo>.tsv a censar (default v1_1)",
    )
    parser.add_argument("--json", dest="salida_json", help="ruta de salida del documento combinado")
    argumentos = parser.parse_args(argv)

    ruta_marco = PREREG / f"marco-M-sorteado-{argumentos.marco}.tsv"
    filas = _leer_tsv(ruta_marco)
    schema_dd = "grado_DD" in (filas[0].keys() if filas else [])
    censo = censar_universo(filas, schema_dd)
    entrada = construir_entrada_scoring(censo)

    documento = {
        "marco_censado": ruta_marco.name,
        "n_celdas_universo": len(censo),
        "n_verificacion_no_puntua": sum(1 for c in censo if c["verificacion_no_puntua"]),
        "n_puntuables": sum(1 for c in censo if c["puntuable"]),
        "censo": censo,
        "entrada_scoring": entrada,
    }
    salida = json.dumps(documento, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if argumentos.salida_json:
        Path(argumentos.salida_json).write_text(salida, encoding="utf-8")
    else:
        sys.stdout.write(salida)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
