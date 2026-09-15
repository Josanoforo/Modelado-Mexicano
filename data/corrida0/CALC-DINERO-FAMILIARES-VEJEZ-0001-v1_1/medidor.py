"""`CALC-DINERO-FAMILIARES-VEJEZ-0001-v1_1` -- recibe dinero de familiares
para la vejez, ENIF 2024, unidad PERSONA. Releva `CORR-0010` `RES-0033`/`RES-0034`.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO EN EL COMMIT-1 DE LA SUCESION v1.1 (`ACTO
GEN2-MEDICION-DEMANDA-2`, CAJA, 15/sep/2026), ANTES DE ABRIR UN SOLO VALOR
DEL MICRODATO EN ESTA SESION. Spec humana sellada que lo gobierna:
`forense/prereg-caja/ENIF-DINERO-FAMILIARES-VEJEZ-spec-v1_0.md` (sha
`e46cac7a…`), via `spec.md`/`spec.yaml` de esta carpeta (contrato verbatim
de la v1_0).

Por que existe este archivo: la v1_0 nombra `script: tools/tasas_base_fase1.py`,
un script de CINCO reglas que no expone `medir()` y cuya funcion de esta regla
(`regla_familia_apoyo()`) trae la ruta del payload fija. Este medidor:
  · IMPORTA `wprop_ic_bootstrap` de ese mismo script (bootstrap ponderado
    SIMPLE por remuestreo de filas, `random.Random(42)`, 10000 replicas,
    percentiles por indice entero -- verbatim, no se reimplementa: es lo que
    hace reproducible el IC95 sellado);
  · REPLICA linea a linea el universo y los filtros de `regla_familia_apoyo()`
    (lectura `pd.read_csv(..., encoding="latin-1", low_memory=False)` sin
    `dtype=str`; `FILTRO_S9_1 == 2` y `EDAD_V < 71` a numerico; `P9_9_4` en
    {1, 2}; `FAC_PER` numerico no nulo), cambiando SOLO la ruta del payload por
    el `ruta_absoluta` que `preflight` resolvio para `enif_2024_enif_2024_bd_csv`
    (P1).

Lo que decide el CODIGO y no la spec, declarado para que se pueda refutar:
  · `G-N-PERSONAS` es el `n` que el legado devolvio y milpa sello (11895):
    personas del universo FILTRO_S9_1=2 y EDAD_V<71 CON reactivo P9_9_4 en
    {1,2} y FAC_PER valido. El legado tambien contaba el universo antes de
    esos dos filtros (`n_universo_filtro_edad`); ese conteo no tiene RESULT
    en la spec y no se inventa uno -- queda en `ejecucion.json` solo si el
    runner lo registra, y en la nota del acto.
  · `SELLADO_P` = 0.457707 (milpa/tramite.yaml:833, citado en la `unidad` de
    `A-DELTA-VS-SELLADO`); `A-RELEVA-SELLADO = SI` sse |delta| <= 1e-6.
  · Guardia estructural: miembro `TMODULO.csv` ausente o columnas ausentes ->
    conjunto COMPLETO de RESULT con `None`/0/`NO-ESTIMABLE-<razon>`.
  · seed/replicas del contrato se verifican contra SEED/N_BOOT del legado.
"""
from __future__ import annotations

import importlib.util
import sys
import zipfile
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
LEGADO = RAIZ / "tools" / "tasas_base_fase1.py"
ZIP_ID = "enif_2024_enif_2024_bd_csv"
P = "RESULT-DFVEJEZ-"
TABLA = "TMODULO.csv"
COLS = ["FILTRO_S9_1", "EDAD_V", "P9_9_4", "FAC_PER"]
SELLADO_P = 0.457707          # milpa/tramite.yaml:833, citado en la spec
TOL = 1.0e-6                  # spec.yaml tolerancia.abs (el contrato no la transporta)


def _carga_legado():
    tools = str(RAIZ / "tools")
    if tools not in sys.path:
        sys.path.insert(0, tools)
    spec = importlib.util.spec_from_file_location("tasas_base_fase1_legado", LEGADO)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _no_estimable(razon: str) -> dict:
    return {
        P + "G-N-PERSONAS": 0,
        P + "A-P-RECIBE": None,
        P + "A-P-NO-RECIBE": None,
        P + "A-SUMA-UNO": f"NO-ESTIMABLE-{razon}",
        P + "A-IC-LO": None,
        P + "A-IC-HI": None,
        P + "A-DELTA-VS-SELLADO": None,
        P + "A-RELEVA-SELLADO": f"NO-ESTIMABLE-{razon}",
    }


def medir(inputs: dict, contrato: dict) -> dict:
    zpath = inputs[ZIP_ID]["ruta_absoluta"]
    seed = contrato["seed"]
    replicas = int((contrato.get("parametros") or {}).get("bootstrap_replicas", 10000))

    m = _carga_legado()
    if not (seed.get("aplica") and int(seed.get("valor")) == int(m.SEED)
            and replicas == int(m.N_BOOT)):
        raise RuntimeError(
            f"contrato seed={seed} replicas={replicas} != estimador legado "
            f"SEED={m.SEED} N_BOOT={m.N_BOOT}: no se re-parametriza el script legado")

    # ── replica de tools/tasas_base_fase1.py::regla_familia_apoyo(), salvo la ruta ──
    with zipfile.ZipFile(zpath) as z:
        if TABLA not in z.namelist():
            return _no_estimable("MIEMBRO-AUSENTE")
        with z.open(TABLA) as f:
            df = pd.read_csv(f, encoding="latin-1", low_memory=False)
    faltan = [c for c in COLS if c not in df.columns]
    if faltan:
        return _no_estimable("COLUMNAS-AUSENTES:" + "+".join(faltan))

    df["FILTRO_S9_1"] = pd.to_numeric(df["FILTRO_S9_1"], errors="coerce")
    df["EDAD_V"] = pd.to_numeric(df["EDAD_V"], errors="coerce")
    universo = df[(df["FILTRO_S9_1"] == 2) & (df["EDAD_V"] < 71)].copy()

    universo["P9_9_4"] = pd.to_numeric(universo["P9_9_4"], errors="coerce")
    universo = universo[universo["P9_9_4"].isin([1, 2])]
    universo["_desenlace"] = (universo["P9_9_4"] == 1).astype(int)
    universo["FAC_PER"] = pd.to_numeric(universo["FAC_PER"], errors="coerce")
    universo = universo.dropna(subset=["FAC_PER"])
    if len(universo) == 0:
        return _no_estimable("UNIVERSO-VACIO")

    p, lo, hi, n = m.wprop_ic_bootstrap(
        universo["_desenlace"].tolist(), universo["FAC_PER"].tolist()
    )
    # ── fin de la replica ──
    p = float(p)
    q = 1.0 - p
    residuo = abs(p + q - 1.0)
    delta = p - SELLADO_P
    return {
        P + "G-N-PERSONAS": int(n),
        P + "A-P-RECIBE": p,
        P + "A-P-NO-RECIBE": q,
        P + "A-SUMA-UNO": f"{'SI' if residuo <= TOL else 'NO'}:{residuo:.3e}",
        P + "A-IC-LO": float(lo),
        P + "A-IC-HI": float(hi),
        P + "A-DELTA-VS-SELLADO": delta,
        P + "A-RELEVA-SELLADO": "SI" if abs(delta) <= TOL else "NO",
    }
