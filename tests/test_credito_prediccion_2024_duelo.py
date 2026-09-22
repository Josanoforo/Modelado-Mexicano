#!/usr/bin/env python3
"""Falsadores de `tools/duelo/credito_prediccion_2024.py` (commit_3,
ACTO GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-2-3).

No abre microdato ni RESULT reales: fabrica dos diccionarios RESULT
sintéticos (forma de ADJUDICACION-0001 y de EMISIONES-0001) y verifica:

1. **Determinismo.** Dos corridas de `adjudica_conducta` con la misma
   semilla dan el mismo ΔMAE/IC bit a bit.
2. **Escolaridad nunca elegible.** `n_celdas_elegibles` no incluye ninguna
   de las 4 celdas `ESCOLARIDAD-*`, aunque el sintético les dé P/IC no
   nulos (para que la exclusión sea por eje declarado, no por casualidad
   de datos ausentes).
3. **Caso conocido: candidato == R exacto en todas las celdas.** ΔMAE debe
   salir 0.0 exacto contra PERSISTENCIA cuando el retador se fabrica
   IDÉNTICO a R (mismo P/IC en cada celda elegible) -- MAE(retador)=0.
4. **Retador ausente.** Si ninguna TENDENCIA-X tiene P (sólo PERSISTENCIA),
   `retador_primario` es `None` y no revienta.

Corre standalone y expone `corre()`.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "duelo"))
import credito_prediccion_2024 as dp  # noqa: E402


def _celda_r(p, ee=0.05):
    lo, hi = dp._expit(dp._logit(p) - dp.Z95 * ee), dp._expit(dp._logit(p) + dp.Z95 * ee)
    return p, lo, hi


def _fabrica(persistencia_p: dict, r_p: dict, tendencia_p: dict | None = None):
    """Construye R_all/E_all sintéticos para UNA conducta ('K1'), con P/IC
    fabricados por `_celda_r` en las 16 celdas de dp.CELLS_ADJ."""
    R_all, E_all = {}, {}
    for cell in dp.CELLS_ADJ:
        p, lo, hi = _celda_r(r_p[cell])
        base = f"RESULT-DIN-CREDITO-PREDICCION-2024-ADJ-K1-{cell}"
        R_all[base + "-P"], R_all[base + "-IC-LO"], R_all[base + "-IC-HI"] = p, lo, hi
        for piso, fuente in (("PERSISTENCIA", persistencia_p), ("TENDENCIA-2", tendencia_p),
                             ("TENDENCIA-3", tendencia_p), ("TENDENCIA-SERIE", tendencia_p)):
            basec = f"RESULT-DIN-CREDITO-PREDICCION-2024-K1-{cell}-2024-{piso}"
            if fuente is None:
                E_all[basec + "-P"] = E_all[basec + "-IC-LO"] = E_all[basec + "-IC-HI"] = None
            else:
                pc, loc, hic = _celda_r(fuente[cell])
                E_all[basec + "-P"], E_all[basec + "-IC-LO"], E_all[basec + "-IC-HI"] = pc, loc, hic
    return R_all, E_all


def _valores(base_p: float):
    return {cell: base_p for cell in dp.CELLS_ADJ}


def _test_determinismo(errores: list[str]):
    R_all, E_all = _fabrica(_valores(0.30), _valores(0.30), _valores(0.35))
    r1 = dp.adjudica_conducta("K1", R_all, E_all, np.random.Generator(np.random.PCG64(dp.SEED)))
    r2 = dp.adjudica_conducta("K1", R_all, E_all, np.random.Generator(np.random.PCG64(dp.SEED)))
    d1 = r1["adjudicacion_por_retador"][r1["retador_primario"]]["delta_mae_pp"]
    d2 = r2["adjudicacion_por_retador"][r2["retador_primario"]]["delta_mae_pp"]
    if d1 != d2:
        errores.append(f"no determinista: {d1} vs {d2}")


def _test_escolaridad_nunca_elegible(errores: list[str]):
    R_all, E_all = _fabrica(_valores(0.30), _valores(0.30), _valores(0.35))
    res = dp.adjudica_conducta("K1", R_all, E_all, np.random.Generator(np.random.PCG64(dp.SEED)))
    tocadas = set(res["celdas_elegibles"]) & dp.ESCOLARIDAD_EXCLUIDA
    if tocadas:
        errores.append(f"escolaridad entró a celdas_elegibles: {tocadas}")
    if res["n_celdas_elegibles"] != len(dp.CELLS_ADJ) - len(dp.ESCOLARIDAD_EXCLUIDA):
        errores.append(f"n_celdas_elegibles={res['n_celdas_elegibles']}, esperaba "
                        f"{len(dp.CELLS_ADJ) - len(dp.ESCOLARIDAD_EXCLUIDA)}")


def _test_retador_identico_a_r(errores: list[str]):
    R_all, E_all = _fabrica(_valores(0.40), _valores(0.30), _valores(0.30))
    res = dp.adjudica_conducta("K1", R_all, E_all, np.random.Generator(np.random.PCG64(dp.SEED)))
    for piso in ("TENDENCIA-2", "TENDENCIA-3", "TENDENCIA-SERIE"):
        mae = res["mae_por_contendiente"][piso]["mae_pp"]
        if mae is None or abs(mae) > 1e-9:
            errores.append(f"MAE({piso}) debía ser ~0.0 (candidato==R), salió {mae}")


def _test_sin_retador(errores: list[str]):
    R_all, E_all = _fabrica(_valores(0.30), _valores(0.30), None)
    res = dp.adjudica_conducta("K1", R_all, E_all, np.random.Generator(np.random.PCG64(dp.SEED)))
    if res["retador_primario"] is not None:
        errores.append(f"esperaba retador_primario=None, salió {res['retador_primario']}")
    if res["habilitados"]:
        errores.append(f"esperaba habilitados=[], salió {res['habilitados']}")
    if res["mae_por_contendiente"]["PERSISTENCIA"]["mae_pp"] is None:
        errores.append("MAE(PERSISTENCIA) no debía ser None con retador ausente")


def corre() -> list[str]:
    errores: list[str] = []
    _test_determinismo(errores)
    _test_escolaridad_nunca_elegible(errores)
    _test_retador_identico_a_r(errores)
    _test_sin_retador(errores)
    return errores


def main() -> int:
    errores = corre()
    for e in errores:
        print("FALLA --", e)
    if not errores:
        print(
            "PASA -- tests/test_credito_prediccion_2024_duelo.py "
            "(determinista; escolaridad nunca elegible; MAE=0 si candidato==R; "
            "sin retador habilitado no revienta)"
        )
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
