#!/usr/bin/env python3
"""Cargador PROPUESTA: qué produciría la entrada `v1_1` de
`tools/score_marco_m.py` si mesa firma `procedimiento-scoring-v1_1
-PROPUESTA.md` -- mismo patrón que `carga_l_v1_1.py` con `pipeline-L
-adv1-m2.py` (importa el módulo sellado por ruta de archivo,
`importlib.util.spec_from_file_location`, SIN editar una sola línea de
`tools/score_marco_m.py`).

ACTO: MAESTRA33-E10 · PROCEDIMIENTO-SCORING-v1_1-PROPUESTA (nube, Opus).
Escrito 1/sep/2026, SHA de redacción `b3c6a1d`.

*** ESTE SCRIPT NO SE EJECUTA EN ESTE ACTO. *** Perímetro del encargo: "el
cargador (sin ejecutar)". No hay smoke-test, no hay `--dry-run`, no hay
salida verificada contra el árbol -- a diferencia de `carga_l_v1_1.py`
(que sí corrió su propio `--dry-run`), este cargador se entrega puramente
como especificación ejecutable de lo que P2 pide, sin invocarlo ni una vez.

Qué produciría, si mesa firma y alguien lo corriera después:

  El único campo que cambia respecto a la `entrada_scoring` que
  `tools/score_marco_m.py` ya arma (`construir_entrada_scoring`,
  `score_marco_m.py:124-158`, sin editar) es `configuracion["delta"]`,
  ausente ahí a propósito (`score_marco_m.py:145-146`: "`delta`:
  deliberadamente ausente -- sigue sin escalar único citado por mesa"). Este
  cargador le añade `delta = 0.5` -- el escalar que
  `procedimiento-scoring-v1_1-PROPUESTA.md` §1 deriva (no elige) de la
  banda ya sellada `Δ_material = 0.5·EE(R)` (`FP-163`/`ADR-199`) expresada
  en unidades `z = dif/EE(R)`.

  `celdas` NO se toca: `mediciones` sigue `{}` en toda celda puntuable --
  sin corredor `B` (declarado NO-APLICA,
  `procedimiento-scoring-v1_1-PROPUESTA.md` §4) no hay `skill` normalizada
  legítima que poblar, y este cargador no la inventa tampoco. Con
  `mediciones: {}`, invocar `ejecutar_scoring` sobre esta entrada seguiría
  fallando en `SIN_CELDAS_PAREADAS` (`scoring-adv1-m3.py:1044-1048`) --
  `delta` sellado no resuelve la ausencia de `B`; son dos huecos
  independientes (§4 del procedimiento v1.0 y v1.1 lo declaran así). Este
  cargador no pretende lo contrario.

Uso (documentado, NO corrido en este acto):
    python3 forense/prereg-duelo-v2/carga_scoring_v1_1_propuesta.py \
        [--marco v1_1] [--json salida.json]
        -- censaría `marco-M-sorteado-<sufijo>.tsv` vía
           `tools/score_marco_m.py` (sin editarlo), le añadiría
           `delta=0.5`, e imprimiría/escribiría el documento resultante.
           No llama a `ejecutar_scoring`. No escribe en `corridas-*`.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT = DIR.parents[1]

_RUTA_SCORE_MARCO_M = ROOT / "tools" / "score_marco_m.py"
_SPEC = importlib.util.spec_from_file_location("score_marco_m", _RUTA_SCORE_MARCO_M)
_SCORE_MARCO_M = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _SCORE_MARCO_M
_SPEC.loader.exec_module(_SCORE_MARCO_M)  # tools/score_marco_m.py NO se edita -- se importa por ruta

_leer_tsv = _SCORE_MARCO_M._leer_tsv
censar_universo = _SCORE_MARCO_M.censar_universo
construir_entrada_scoring = _SCORE_MARCO_M.construir_entrada_scoring
PREREG = _SCORE_MARCO_M.PREREG

# Escalar derivado, no elegido -- procedimiento-scoring-v1_1-PROPUESTA.md
# §1, de la banda ya sellada Δ_material = 0.5·EE(R) (FP-163/ADR-199,
# procedimiento-scoring-v1_0.md:20-24) expresada en unidades z = dif/EE(R).
# PENDIENTE-DE-MESA: no entra a ninguna entrada real hasta que mesa firme
# la fila del tablero (mesa-pendientes.md §5, P3 de MAESTRA33-E10).
DELTA_PROPUESTA_V1_1 = 0.5


def construir_entrada_v1_1_propuesta(censo: list[dict]) -> dict:
    """`entrada_scoring` de `tools/score_marco_m.py` (sin editar) + `delta` PROPUESTA.

    No toca `celdas` -- `mediciones` sigue `{}` en toda celda puntuable
    (baseline `B` NO-APLICA, `procedimiento-scoring-v1_1-PROPUESTA.md` §4).
    Único cambio: `configuracion["delta"]`, ausente en la entrada sellada
    de `tools/score_marco_m.py` (`score_marco_m.py:145-146`).
    """
    entrada = construir_entrada_scoring(censo)
    entrada["configuracion"] = dict(entrada["configuracion"])
    entrada["configuracion"]["delta"] = DELTA_PROPUESTA_V1_1
    return entrada


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
    entrada_v1_1 = construir_entrada_v1_1_propuesta(censo)

    documento = {
        "acto": "MAESTRA33-E10 · PROCEDIMIENTO-SCORING-v1_1-PROPUESTA",
        "estado": "PROPUESTA -- PENDIENTE-DE-MESA -- este script no se ejecutó en MAESTRA33-E10",
        "marco_censado": ruta_marco.name,
        "entrada_scoring_v1_1_propuesta": entrada_v1_1,
    }
    salida = json.dumps(documento, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if argumentos.salida_json:
        Path(argumentos.salida_json).write_text(salida, encoding="utf-8")
    else:
        sys.stdout.write(salida)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
