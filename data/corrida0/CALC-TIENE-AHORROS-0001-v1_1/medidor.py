"""`CALC-TIENE-AHORROS-0001-v1_1` -- tenencia de ahorro (formal ∪ informal),
ENIF 2024, unidad PERSONA elegida 18+. Releva `CORR-0009` `RES-0031`/`RES-0032`.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO EN EL COMMIT-1 DE LA SUCESION v1.1 (`ACTO
GEN2-MEDICION-DEMANDA-2`, CAJA, 15/sep/2026), ANTES DE ABRIR UN SOLO VALOR
DEL MICRODATO EN ESTA SESION. Spec humana sellada que lo gobierna:
`forense/prereg-caja/ENIF-TIENE-AHORROS-spec-v1_0.md` (sha `b2add081…`),
via `spec.md`/`spec.yaml` de esta carpeta (contrato verbatim de la v1_0).

Por que existe este archivo: la v1_0 nombra `script: tools/medidor_ahorro_enif24.py`,
que no expone `medir()` -- el runner lo declara NO-EJECUTABLE por doctrina.
Este medidor NO reimplementa nada: carga ese mismo script legado por ruta y
REUTILIZA `carga()` (cargador + guardias PARO) y `estima()` (que llama a
`wprop_ic_conglomerado`, bootstrap de conglomerado EST_DIS x UPM_DIS,
n_boot=10000, seed=42, `numpy.random.default_rng`). Lo UNICO que cambia es la
ruta del payload: en vez de `data/raw/enif_2024_bd_csv.zip` fijo, el
`ruta_absoluta` que `preflight` resolvio para `enif_2024_enif_2024_bd_csv`
(P1: el medidor no vuelve a resolver identidad).

Lo que decide el CODIGO y no la spec, declarado para que se pueda refutar:
  · `SELLADO_P` = 0.642080 es la constante que la propia spec escribe en la
    `unidad` de `A-DELTA-VS-SELLADO` (milpa/tramite.yaml:641); no se lee de
    `milpa/` en tiempo de corrida (no es input declarado).
  · `A-RELEVA-SELLADO = SI` sse |delta| <= tolerancia.abs de la spec (1e-6).
    El valor sellado esta redondeado a 6 decimales, asi que una reproduccion
    exacta da |delta| <= 5e-7.
  · Guardia estructural: si el ZIP no trae `TMODULO.csv`, o `carga()` PARA
    (columnas ausentes, EDAD_V < 18, FAC_PER no positivo, seccion 5 en
    blanco), se devuelve el conjunto COMPLETO de RESULT con `None` donde la
    spec lo permite, 0 en los enteros y `NO-ESTIMABLE-<razon>` en los textos.
    No se adivina nada.
  · Los defaults del estimador legado (seed 42, 10000 replicas) se verifican
    contra el contrato; si difieren, la corrida PARA (no se re-parametriza el
    script legado).
"""
from __future__ import annotations

import importlib.util
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
LEGADO = RAIZ / "tools" / "medidor_ahorro_enif24.py"
ZIP_ID = "enif_2024_enif_2024_bd_csv"
P = "RESULT-TIENEAHORROS-"
SELLADO_P = 0.642080          # milpa/tramite.yaml:641, citado en la spec
TOL = 1.0e-6                  # spec.yaml tolerancia.abs (el contrato no la transporta)
TABLA = "TMODULO.csv"


def _carga_legado():
    """Importa `tools/medidor_ahorro_enif24.py` por ruta, sin ejecutar su
    `main()`. `tools/` entra en `sys.path` solo porque el propio script legado
    lo hace al importarse (necesita `calibracion_mordida_encig_serie` y
    `ejes_maestra35_l1`)."""
    tools = str(RAIZ / "tools")
    if tools not in sys.path:
        sys.path.insert(0, tools)
    spec = importlib.util.spec_from_file_location("medidor_ahorro_enif24_legado", LEGADO)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _no_estimable(razon: str) -> dict:
    return {
        P + "G-N-PERSONAS": 0,
        P + "G-NUMERADOR": 0,
        P + "A-P-TIENE": None,
        P + "A-P-NO-TIENE": None,
        P + "A-SUMA-UNO": f"NO-ESTIMABLE-{razon}",
        P + "A-IC-LO": None,
        P + "A-IC-HI": None,
        P + "A-DELTA-VS-SELLADO": None,
        P + "A-RELEVA-SELLADO": f"NO-ESTIMABLE-{razon}",
    }


def medir(inputs: dict, contrato: dict) -> dict:
    zpath = inputs[ZIP_ID]["ruta_absoluta"]
    tol = TOL
    seed = contrato["seed"]
    replicas = int((contrato.get("parametros") or {}).get("bootstrap_replicas", 10000))

    with zipfile.ZipFile(zpath) as z:
        if TABLA not in z.namelist():
            return _no_estimable("MIEMBRO-AUSENTE")

    m = _carga_legado()
    # el estimador legado fija seed y replicas por defecto en
    # calibracion_mordida_encig_serie (SEED, N_BOOT): se verifica, no se re-parametriza
    import calibracion_mordida_encig_serie as cal  # noqa: E402  (ya en sys.path)
    if not (seed.get("aplica") and int(seed.get("valor")) == int(cal.SEED)
            and replicas == int(cal.N_BOOT)):
        raise RuntimeError(
            f"contrato seed={seed} replicas={replicas} != estimador legado "
            f"SEED={cal.SEED} N_BOOT={cal.N_BOOT}: no se re-parametriza el script legado")

    m.ZIP = zpath                     # unica desviacion del legado: la ruta (P1)
    try:
        df = m.carga()
    except SystemExit as e:           # las guardias PARO del legado
        return _no_estimable("CARGA-PARO:" + str(e).split("·", 1)[-1].strip()[:60].replace(" ", "_"))

    r = m.estima(df, m.TODAS, "formal ∪ informal (P5_1_1..6 ∪ P5_6_1..9)")
    p = float(r["p"])
    q = 1.0 - p
    residuo = abs(p + q - 1.0)
    delta = p - SELLADO_P
    return {
        P + "G-N-PERSONAS": int(r["n"]),
        P + "G-NUMERADOR": int(r["n_num"]),
        P + "A-P-TIENE": p,
        P + "A-P-NO-TIENE": q,
        P + "A-SUMA-UNO": f"{'SI' if residuo <= tol else 'NO'}:{residuo:.3e}",
        P + "A-IC-LO": float(r["lo"]),
        P + "A-IC-HI": float(r["hi"]),
        P + "A-DELTA-VS-SELLADO": delta,
        P + "A-RELEVA-SELLADO": "SI" if abs(delta) <= tol else "NO",
    }
