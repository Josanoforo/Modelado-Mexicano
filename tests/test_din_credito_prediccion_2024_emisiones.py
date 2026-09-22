#!/usr/bin/env python3
"""Falsadores de CALC-DIN-CREDITO-PREDICCION-2024-EMISIONES-0001
(ACTO GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1, piezas P1/P2/P3).

Dos bloques, ninguno abre microdato real ni ENIF 2024:

1. **Sintético (D-22).** Fabrica cuatro "pisos" con series de proporciones
   inventadas (no reales) para varias conductas de prueba, cubriendo cada
   rama terminal declarada en la spec (§2-3): sin ninguna ola (todo
   `None`), 1 ola (sólo persistencia posible), 2 olas (bajo el umbral de
   3: sigue siendo sólo persistencia), 4 olas (los cuatro contendientes),
   y una celda rara deliberada (`IC-LO=0.0` exacto) que el medidor debe
   excluir de la serie sin reventar.
2. **Sellado.** Si `resultados.json` existe: `spec_md_sha256` coincide;
   PERSISTENCIA es el mejor contendiente de backtest en al menos la
   mayoría de las conductas que entran (evidencia de que el backtest
   corrió sobre dato real, no está vacío).

Corre standalone (`python3 tests/test_din_credito_prediccion_2024_emisiones.py`)
y expone `corre()`.
"""
from __future__ import annotations

import hashlib
import json
import math
import types
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CALC = ROOT / "data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-EMISIONES-0001"
SPEC_MD = ROOT / "forense/prereg-caja/DIN-CREDITO-PREDICCION-2024-EMISIONES-spec-v1_0.md"


def _modulo(ruta: Path, nombre: str):
    src = ruta.read_bytes()
    mod = types.ModuleType(nombre)
    exec(compile(src, str(ruta), "exec"), mod.__dict__)
    return mod


def _resultado_ola(prefijo: str, cid: str, cell: str, p, lo, hi, n=1000):
    b = f"RESULT-{prefijo}-{cid}-{cell}"
    return {f"{b}-P": p, f"{b}-IC-LO": lo, f"{b}-IC-HI": hi, f"{b}-N": n}


def _piso_sintetico(prefijo: str, casos: dict) -> bytes:
    """casos: {(cid, cell): (p, lo, hi) | None} -- None omite la celda."""
    r = {}
    for (cid, cell), val in casos.items():
        if val is None:
            continue
        p, lo, hi = val
        r.update(_resultado_ola(prefijo, cid, cell, p, lo, hi))
    return json.dumps({"resultados": r}).encode("utf-8")


def _corre_sintetico(errores: list[str]) -> dict | None:
    mod = _modulo(CALC / "medidor.py", "medidor_prediccion_2024")
    om_path = ROOT / "tools/encig_origen_movil.py"

    # Cuatro conductas de prueba, cada una ejerciendo una rama distinta.
    casos_2012 = {("CERO-OLAS", "NACIONAL-TODOS"): None,
                  ("UNA-OLA", "NACIONAL-TODOS"): (0.20, 0.15, 0.25),
                  ("DOS-OLAS", "NACIONAL-TODOS"): (0.18, 0.13, 0.23),
                  ("CUATRO-OLAS", "NACIONAL-TODOS"): (0.10, 0.08, 0.12),
                  ("CELDA-RARA", "NACIONAL-TODOS"): (0.001, 0.0, 0.003)}
    casos_2015 = {("CERO-OLAS", "NACIONAL-TODOS"): None,
                  ("UNA-OLA", "NACIONAL-TODOS"): None,
                  ("DOS-OLAS", "NACIONAL-TODOS"): (0.20, 0.15, 0.25),
                  ("CUATRO-OLAS", "NACIONAL-TODOS"): (0.13, 0.10, 0.16),
                  ("CELDA-RARA", "NACIONAL-TODOS"): (0.002, 0.0005, 0.004)}
    casos_2018 = {("CERO-OLAS", "NACIONAL-TODOS"): None,
                  ("UNA-OLA", "NACIONAL-TODOS"): None,
                  ("DOS-OLAS", "NACIONAL-TODOS"): None,
                  ("CUATRO-OLAS", "NACIONAL-TODOS"): (0.16, 0.13, 0.19),
                  ("CELDA-RARA", "NACIONAL-TODOS"): (0.0015, 0.0004, 0.0035)}
    casos_2021 = {("CERO-OLAS", "NACIONAL-TODOS"): None,
                  ("UNA-OLA", "NACIONAL-TODOS"): None,
                  ("DOS-OLAS", "NACIONAL-TODOS"): None,
                  ("CUATRO-OLAS", "NACIONAL-TODOS"): (0.19, 0.16, 0.22),
                  ("CELDA-RARA", "NACIONAL-TODOS"): (0.0018, 0.0006, 0.0038)}

    inputs = {
        "PISO-2012": {"ruta_absoluta": "", "bytes": _piso_sintetico("SINT-PISOS-2012", casos_2012)},
        "PISO-2015": {"ruta_absoluta": "", "bytes": _piso_sintetico("SINT-PISOS-2015", casos_2015)},
        "PISO-2018": {"ruta_absoluta": "", "bytes": _piso_sintetico("SINT-PISOS-2018", casos_2018)},
        "PISO-2021": {"ruta_absoluta": "", "bytes": _piso_sintetico("SINT-PISOS-2021", casos_2021)},
        "MEDIDOR-TENDENCIA-ORIGEN-MOVIL": {"ruta_absoluta": str(om_path), "bytes": om_path.read_bytes()},
    }

    mod.WAVE_PREFIJO = {"2012": "SINT-PISOS-2012", "2015": "SINT-PISOS-2015",
                        "2018": "SINT-PISOS-2018", "2021": "SINT-PISOS-2021"}
    mod.ENTERING = ["CERO-OLAS", "UNA-OLA", "DOS-OLAS", "CUATRO-OLAS", "CELDA-RARA"]
    mod.CELLS = ["NACIONAL-TODOS"]

    try:
        out = mod.medir(inputs, {})
    except Exception as exc:  # noqa: BLE001
        errores.append(f"medir() sobre el sintético reventó: {exc!r}")
        return None
    return out


def _falsa_sintetico(out: dict, errores: list[str]) -> None:
    pref = "RESULT-DIN-CREDITO-PREDICCION-2024"

    # CERO-OLAS: ninguna predicción definida para ningún año/contendiente.
    for anio in (2015, 2018, 2021, 2024):
        if out.get(f"{pref}-CERO-OLAS-NACIONAL-TODOS-{anio}-N-OLAS-PREVIAS") != 0:
            errores.append(f"CERO-OLAS-{anio}: N-OLAS-PREVIAS debería ser 0")
        if out.get(f"{pref}-CERO-OLAS-NACIONAL-TODOS-{anio}-PERSISTENCIA-P") is not None:
            errores.append(f"CERO-OLAS-{anio}: PERSISTENCIA-P debería ser None")

    # UNA-OLA (sólo 2012): persistencia entra para 2015+, tendencia nunca.
    if out.get(f"{pref}-UNA-OLA-NACIONAL-TODOS-2015-PERSISTENCIA-P") is None:
        errores.append("UNA-OLA-2015: PERSISTENCIA-P debería estar definida (1 ola previa)")
    for piso in ("TENDENCIA-2", "TENDENCIA-3", "TENDENCIA-SERIE"):
        if out.get(f"{pref}-UNA-OLA-NACIONAL-TODOS-2015-{piso}-P") is not None:
            errores.append(f"UNA-OLA-2015: {piso}-P debería ser None (sólo 1 ola previa)")

    # DOS-OLAS (2012,2015): para el objetivo 2018 hay 2 previas -- bajo el
    # umbral de 3 de esta spec, sigue siendo sólo persistencia.
    if out.get(f"{pref}-DOS-OLAS-NACIONAL-TODOS-2018-PERSISTENCIA-P") is None:
        errores.append("DOS-OLAS-2018: PERSISTENCIA-P debería estar definida")
    for piso in ("TENDENCIA-2", "TENDENCIA-3", "TENDENCIA-SERIE"):
        if out.get(f"{pref}-DOS-OLAS-NACIONAL-TODOS-2018-{piso}-P") is not None:
            errores.append(f"DOS-OLAS-2018: {piso}-P debería ser None bajo el umbral de 3 (spec.md §2)")

    # CUATRO-OLAS: los cuatro contendientes definidos para 2024, con backtest
    # en 2015/2018/2021.
    for piso in ("PERSISTENCIA", "TENDENCIA-2", "TENDENCIA-3", "TENDENCIA-SERIE"):
        if out.get(f"{pref}-CUATRO-OLAS-NACIONAL-TODOS-2024-{piso}-P") is None:
            errores.append(f"CUATRO-OLAS-2024: {piso}-P debería estar definida (4 olas previas)")
    if out.get(f"{pref}-CUATRO-OLAS-PERSISTENCIA-N-BACKTEST") != 3:
        errores.append("CUATRO-OLAS: N-BACKTEST de PERSISTENCIA debería ser 3 (2015,2018,2021)")
    err_2021 = out.get(f"{pref}-CUATRO-OLAS-NACIONAL-TODOS-2021-PERSISTENCIA-ERROR-PP")
    if err_2021 is None:
        errores.append("CUATRO-OLAS-2021: ERROR-PP debería estar definido (hay valor real sellado)")

    # CELDA-RARA: la ola con lo=0.0 se excluye; con 4 olas fabricadas y 1
    # excluida quedan 3 -- justo en el umbral, entran los cuatro contendientes
    # para 2024 (3 previas: 2015,2018,2021 sin la de 2012).
    raras = out.get(f"{pref}-CELDA-RARA-NACIONAL-TODOS-CELDAS-RARAS-EXCLUIDAS")
    if raras != "2012":
        errores.append(f"CELDA-RARA: CELDAS-RARAS-EXCLUIDAS debería ser '2012', es {raras!r}")
    if out.get(f"{pref}-CELDA-RARA-NACIONAL-TODOS-N-CELDAS-RARAS-EXCLUIDAS") != 1:
        errores.append("CELDA-RARA: N-CELDAS-RARAS-EXCLUIDAS debería ser 1")

    # Ningún NaN/inf en todo el sintético.
    no_finitos = [k for k, v in out.items() if isinstance(v, float) and not math.isfinite(v)]
    if no_finitos:
        errores.append(f"valores no finitos: {no_finitos[:5]}")


def _falsa_sellado(errores: list[str]) -> None:
    rj = CALC / "resultados.json"
    if not rj.exists():
        return
    res = json.loads(rj.read_text(encoding="utf-8")).get("resultados", {})
    spec = yaml.safe_load((CALC / "spec.yaml").read_text(encoding="utf-8"))
    with SPEC_MD.open("rb") as fh:
        sha_md = hashlib.sha256(fh.read()).hexdigest()
    if spec.get("spec_md_sha256") != sha_md:
        errores.append("spec_md_sha256 del yaml no coincide con la spec humana")

    entering = ["K1", "K2-DEPARTAMENTAL", "K2-NOMINA", "K2-AUTOMOTRIZ", "K3",
                "K4A-AUTOEXCLUSION", "K4B-OFERTA", "K5", "K6-P-TENEDORES"]
    mejores = [res.get(f"RESULT-DIN-CREDITO-PREDICCION-2024-{cid}-MEJOR-CONTENDIENTE-BACKTEST")
               for cid in entering]
    faltan = [cid for cid, m in zip(entering, mejores) if m is None]
    if faltan:
        errores.append(f"sellado: sin MEJOR-CONTENDIENTE-BACKTEST para {faltan}")
    n_persistencia = sum(1 for m in mejores if m == "PERSISTENCIA")
    if n_persistencia < len(entering) // 2:
        errores.append(
            f"sellado: PERSISTENCIA sólo es mejor en {n_persistencia}/{len(entering)} -- "
            "revisar si el backtest realmente corrió sobre dato real"
        )


def corre() -> list[str]:
    errores: list[str] = []
    for p in (CALC / "medidor.py", CALC / "spec.yaml", SPEC_MD,
              Path(str(SPEC_MD).rsplit(".md", 1)[0] + ".sha256")):
        if not p.exists():
            errores.append(f"falta {p.relative_to(ROOT)}")
    if errores:
        return errores

    out = _corre_sintetico(errores)
    if out is not None:
        _falsa_sintetico(out, errores)
    _falsa_sellado(errores)
    return errores


def main() -> int:
    errores = corre()
    for e in errores:
        print("FALLA --", e)
    if not errores:
        print(
            "PASA -- tests/test_din_credito_prediccion_2024_emisiones.py "
            "(sintético: 0/1/2/4 olas, celda rara excluida sin reventar; "
            "sellado si existe)"
        )
    return 1 if errores else 0


if __name__ == "__main__":
    raise SystemExit(main())
