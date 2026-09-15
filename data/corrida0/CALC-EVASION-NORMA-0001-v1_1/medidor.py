"""`CALC-EVASION-NORMA-0001-v1_1` -- evasion de norma percibida inutil,
ENVIPE 2025, unidad DELITO. Releva `CORR-0007` `RES-0025`/`RES-0026`.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO EN EL COMMIT-1 DE LA SUCESION v1.1 (`ACTO
GEN2-MEDICION-DEMANDA-2`, CAJA, 15/sep/2026), ANTES DE ABRIR UN SOLO VALOR
DEL MICRODATO EN ESTA SESION. Spec humana sellada que lo gobierna:
`forense/prereg-caja/ENVIPE-EVASION-NORMA-spec-v1_0.md` (sha `69605ea4…`),
via `spec.md`/`spec.yaml` de esta carpeta (contrato verbatim de la v1_0).

Por que existe este archivo: la v1_0 nombra
`script: tools/medidor_evasion_norma_envipe25.py`, que no expone `medir()`.
Este medidor NO reimplementa nada: carga ese script legado por ruta y
REUTILIZA `carga()` (cargador + guardias PARO, normalizacion `dos_digitos` de
BP1_23) y `estima()` (`wprop_ic_conglomerado`, bootstrap de conglomerado
EST_DIS x UPM_DIS, n_boot=10000, seed=42). Lo UNICO que cambia es la ruta del
payload: el `ruta_absoluta` que `preflight` resolvio para `envipe2025_csv`
(P1). El desenlace es el del legado, verbatim: evade_norma = 1 sse
BP1_20 == '2' y BP1_23 (dos digitos) en {04, 05, 06, 08} -- la CONJUNTA, no
la condicional (reserva heredada, spec.md §2).

Lo que decide el CODIGO y no la spec, declarado para que se pueda refutar:
  · `SELLADO_P` = 0.562774 (milpa/tramite.yaml:474, citado en la `unidad` de
    `A-DELTA-VS-SELLADO`); no se lee de `milpa/` en tiempo de corrida.
  · `A-RELEVA-SELLADO = SI` sse |delta| <= 1e-6 (tolerancia.abs de la spec).
  · Guardia estructural: miembro ausente o `carga()` PARA -> conjunto COMPLETO
    de RESULT con `None`/0/`NO-ESTIMABLE-<razon>`. No se adivina nada.
  · seed/replicas del contrato se verifican contra SEED/N_BOOT del estimador
    legado; si difieren, PARA.
"""
from __future__ import annotations

import importlib.util
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
LEGADO = RAIZ / "tools" / "medidor_evasion_norma_envipe25.py"
ZIP_ID = "envipe2025_csv"
P = "RESULT-EVASIONNORMA-"
SELLADO_P = 0.562774          # milpa/tramite.yaml:474, citado en la spec
TOL = 1.0e-6                  # spec.yaml tolerancia.abs (el contrato no la transporta)


def _carga_legado():
    tools = str(RAIZ / "tools")
    if tools not in sys.path:
        sys.path.insert(0, tools)
    spec = importlib.util.spec_from_file_location(
        "medidor_evasion_norma_envipe25_legado", LEGADO)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _no_estimable(razon: str) -> dict:
    return {
        P + "G-N-DELITOS": 0,
        P + "G-NUMERADOR": 0,
        P + "A-P-EVADE": None,
        P + "A-P-CUMPLE": None,
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
    with zipfile.ZipFile(zpath) as z:
        if m.TABLA not in z.namelist():
            return _no_estimable("MIEMBRO-AUSENTE")

    import calibracion_mordida_encig_serie as cal  # noqa: E402  (ya en sys.path)
    if not (seed.get("aplica") and int(seed.get("valor")) == int(cal.SEED)
            and replicas == int(cal.N_BOOT)):
        raise RuntimeError(
            f"contrato seed={seed} replicas={replicas} != estimador legado "
            f"SEED={cal.SEED} N_BOOT={cal.N_BOOT}: no se re-parametriza el script legado")

    m.ZIP = zpath                     # unica desviacion del legado: la ruta (P1)
    try:
        df = m.carga()
    except SystemExit as e:
        return _no_estimable("CARGA-PARO:" + str(e).split("·", 1)[-1].strip()[:60].replace(" ", "_"))

    r = m.estima(df, m.INUTIL, "BP1_20=2 ∧ BP1_23∈{04,05,06,08} · norma inútil o extractiva")
    p = float(r["p"])
    q = 1.0 - p
    residuo = abs(p + q - 1.0)
    delta = p - SELLADO_P
    return {
        P + "G-N-DELITOS": int(r["n"]),
        P + "G-NUMERADOR": int(r["n_num"]),
        P + "A-P-EVADE": p,
        P + "A-P-CUMPLE": q,
        P + "A-SUMA-UNO": f"{'SI' if residuo <= TOL else 'NO'}:{residuo:.3e}",
        P + "A-IC-LO": float(r["lo"]),
        P + "A-IC-HI": float(r["hi"]),
        P + "A-DELTA-VS-SELLADO": delta,
        P + "A-RELEVA-SELLADO": "SI" if abs(delta) <= TOL else "NO",
    }
