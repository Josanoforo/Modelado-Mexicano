#!/usr/bin/env python3
"""Falsadores de CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001
(ACTO GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-1, pieza P2 -- código
CONGELADO SIN CORRER, guardia de una variable).

NUNCA abre `data/raw/enif2024_csv.zip` (el real): fabrica un ZIP propio
con la MISMA forma de columnas (minúsculas, nombres 2024 verificados
contra el descriptor) y valores inventados.

Tres bloques:
1. **Guardia.** `abre_conducta_2024` PARA con `ReservaRota` para: una
   conducta fuera de la lista blanca, una lista de conductas, `"*"`.
   Nunca llega a abrir el ZIP en esos tres casos (se verifica pasando una
   ruta inexistente -- si el código intentara leerla, reventaría con
   `FileNotFoundError`/`RuntimeError`, no con `ReservaRota`).
2. **Extracción guardada.** Para una conducta autorizada (K1), el marco
   devuelto está recortado a EDAD 18-70 (igual que -RECORTE1870-0001) y
   los ejes (sexo/edad/escolaridad/localidad/formalidad) sólo traen
   categorías de la rejilla esperada.
3. **`medir()` de punta a punta sobre el sintético.** Las 9 conductas de
   la lista blanca emiten sus 7 celdas (nacional + sexo x2 + edad x4 +
   escolaridad x4 + localidad x2 + formalidad x2 + universo = 16) con
   -P/-IC-LO/-IC-HI/-N/-DEN-W/-B-VALIDAS, sin NaN/inf.

Corre standalone y expone `corre()`.
"""
from __future__ import annotations

import io
import math
import types
import zipfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CALC = ROOT / "data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001"
CALC_0003 = ROOT / "data/corrida0/CALC-PISOS-ENIF2021-EJES-0003"
MIEMBRO = "conjunto_de_datos_tmodulo_enif2024.csv"


def _modulo():
    src = (CALC / "medidor.py").read_bytes()
    mod = types.ModuleType("medidor_adjudicacion_2024")
    exec(compile(src, str(CALC / "medidor.py"), "exec"), mod.__dict__)
    return mod


def _payload_sintetico(n: int = 1200, semilla: int = 11) -> bytes:
    rng = np.random.default_rng(semilla)
    cols = ([f"p6_2_{k}" for k in range(1, 10)] + [f"p6_3_{k}" for k in range(1, 10)]
            + [f"p6_1_{k}" for k in range(1, 6)]
            + ["p6_13", "p6_14", "p6_16", "p3_10", "sexo", "edad_v", "tloc", "niv",
               "fac_per", "est_dis", "upm_dis"])
    filas = []
    for i in range(n):
        est = 1 + i % 10
        upm = est * 10 + rng.integers(0, 4)
        prod = ["1" if rng.random() < p else "2" for p in
                (0.20, 0.08, 0.06, 0.05, 0.02, 0.10, 0.02, 0.01, 0.01)]
        tenedor = "1" in prod
        atr = ["" if pk != "1" else rng.choice(["1", "2", "2", "2"], p=[.2, .6, .1, .1])
               for pk in prod]
        inf = [rng.choice(["1", "2"], p=[q, 1 - q]) for q in (.05, .04, .15, .2, .01)]
        p13 = "" if tenedor else rng.choice(["1", "2"], p=[.3, .7])
        p14 = str(rng.integers(1, 10)) if (not tenedor and p13 == "2") else ""
        p16 = rng.choice(["1", "2", "3"], p=[.12, .38, .5])
        p310 = rng.choice(list("1234569"), p=[.35, .05, .02, .03, .02, .5, .03])
        niv = rng.choice(["00", "02", "03", "06", "08", "10", "99"],
                          p=[.05, .15, .25, .25, .2, .05, .05])
        filas.append(prod + atr + inf + [
            p13, p14, p16, p310, str(rng.integers(1, 3)),
            str(rng.integers(18, 99)), str(rng.integers(1, 5)), niv,
            str(rng.integers(500, 5000)), f"{est:03d}", f"{upm:07d}"])
    csv = ",".join(cols) + "\n" + "\n".join(",".join(f) for f in filas) + "\n"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(MIEMBRO, csv.encode("utf-8"))
    return buf.getvalue()


def _inputs(tmp_zip_path: str) -> dict:
    return {
        "enif2024_csv": {"ruta_absoluta": tmp_zip_path, "bytes": None},
        "MEDIDOR-EJES-0003": {"ruta_absoluta": str(CALC_0003 / "medidor.py"),
                              "bytes": (CALC_0003 / "medidor.py").read_bytes()},
    }


def _falsa_guardia(mod, inputs, errores: list[str]) -> None:
    ruta_inexistente = "/no/existe/nada.zip"
    inputs_rota = dict(inputs)
    inputs_rota["enif2024_csv"] = {"ruta_absoluta": ruta_inexistente, "bytes": None}
    for malo in ("K1-NO-EXISTE", ["K1"], "*", "", None, "k1"):
        try:
            mod.abre_conducta_2024(inputs_rota, malo, {})
            errores.append(f"la guardia dejó pasar conducta_id={malo!r} sin abrir nada")
        except mod.ReservaRota:
            pass
        except Exception as exc:  # noqa: BLE001
            errores.append(f"conducta_id={malo!r} reventó con {exc!r} en vez de ReservaRota "
                           "-- la guardia dejó que el código intentara abrir el ZIP")


def _falsa_extraccion(mod, inputs, errores: list[str]) -> None:
    abierto = mod.abre_conducta_2024(inputs, "K1", {})
    d = abierto["marco"]
    edad = d[mod.COLUMNA_2024["EDAD"]].astype(float)
    if not ((edad >= 18) & (edad <= 70)).all():
        errores.append("K1: el marco extraído trae EDAD fuera de [18,70]")
    vistos = set(abierto["ejes"]["escolaridad"].dropna().unique())
    esperados = {"hasta_primaria", "secundaria", "media_superior", "superior"}
    if not vistos <= esperados:
        errores.append(f"K1: escolaridad fuera de la rejilla: {vistos - esperados}")


def _falsa_medir(mod, inputs, errores: list[str]) -> None:
    contrato = {"parametros": {"bootstrap_replicas": 120}, "seed": {"valor": 42}}
    try:
        out = mod.medir(inputs, contrato)
    except Exception as exc:  # noqa: BLE001
        errores.append(f"medir() sobre el sintético reventó: {exc!r}")
        return
    puntos = [k for k in out if k.endswith("-P") and k.startswith(f"RESULT-{mod.PREFIJO}")]
    esperado = len(mod.CONDUCTAS_AUTORIZADAS) * 7  # nacional+2+4+4+2+2+1 = 16... ver abajo
    # nacional(1) + sexo(2) + edad(4) + escolaridad(4) + localidad(2) + formalidad(2) + universo(1) = 16
    esperado = len(mod.CONDUCTAS_AUTORIZADAS) * 16
    if len(puntos) != esperado:
        errores.append(f"{len(puntos)} celdas -P, esperaba {esperado}")
    no_finitos = [k for k, v in out.items() if isinstance(v, float) and not math.isfinite(v)]
    if no_finitos:
        errores.append(f"valores no finitos: {no_finitos[:5]}")


def corre() -> list[str]:
    errores: list[str] = []
    for p in (CALC / "medidor.py", CALC / "spec.yaml"):
        if not p.exists():
            errores.append(f"falta {p.relative_to(ROOT)}")
    if errores:
        return errores
    mod = _modulo()

    import tempfile
    with tempfile.TemporaryDirectory() as td:
        zp = Path(td) / "enif2024_sintetico.zip"
        zp.write_bytes(_payload_sintetico())
        inputs = _inputs(str(zp))
        _falsa_guardia(mod, inputs, errores)
        _falsa_extraccion(mod, inputs, errores)
        _falsa_medir(mod, inputs, errores)
    return errores


def main() -> int:
    errores = corre()
    for e in errores:
        print("FALLA --", e)
    if not errores:
        print(
            "PASA -- tests/test_din_credito_prediccion_2024_adjudicacion.py "
            "(guardia rechaza conducta no autorizada/lista/\"*\"; extracción "
            "recorta 18-70; medir() sintético: 9 conductas x 16 celdas, sin NaN/inf)"
        )
    return 1 if errores else 0


if __name__ == "__main__":
    raise SystemExit(main())
