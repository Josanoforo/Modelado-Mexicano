#!/usr/bin/env python3
"""Piezas comunes de los expedientes de apertura — ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (28/sep/2026).

Un expediente vive en `forense/prereg-aperturas/<X>/` (X = PROGRAMA-OLA) y trae:
  APERTURA-<X>-spec-v1_0.md (+ .sha256)   spec humana (D-15)
  APERTURA-<X>-spec.yaml                  contrato `corrida0` completo (lo escribe `escribe_contrato`)
  medidor_apertura_<x>.py                 `medir(inputs, contrato)` + `esquema_resultados()` + `CONTRATO`
  RECETA-APERTURA-<X>.md                  receta de un commit (la escribe `escribe_receta`)

La apertura es un commit: copiar `APERTURA-<X>-spec.yaml` a `data/corrida0/CALC-APERTURA-<X>-0001/spec.yaml`
(el `spec_md` ya es relativo a esa carpeta y el `script` apunta al medidor del expediente), `preflight`,
`run`. Nada se reescribe al abrir.

Contrato del medidor (lo verifica `tests/test_prereg_aperturas.py` sobre TODO expediente):
  · `CONTRATO` = dict con `x`, `programa`, `ola`, `contendientes` (CALC sellados), `payloads` [(id, nota)],
    `repo` [(clave, ruta, nota)], y los textos `universo`, `filtros`, `ponderador`, `transformacion`,
    `estimando`, `variables` (lista de dicts `nombre`, `definicion`).
  · `medir()` corre `guardia_apertura.exige_auditoria` sobre su propio archivo como PRIMERA sentencia.
  · única lectura de la ola reservada: una función llamada `lee_payload_reservado`.
  · `esquema_resultados()` = `esquema(P, celdas)`; `medir()` devuelve exactamente esos ids.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import types

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
EXP = "forense/prereg-aperturas"
ACTO = "GEN2-APERTURAS-PREREGISTRADAS-1"


def carga(ruta_abs: str, nombre: str):
    spec = importlib.util.spec_from_file_location(nombre, ruta_abs)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


G = carga(os.path.join(AQUI, "guardia_apertura.py"), "guardia_apertura")


def sha256_de(rel: str) -> str:
    return hashlib.sha256(open(os.path.join(RAIZ, rel), "rb").read()).hexdigest()


def bytes_repo(inputs: dict | None, clave: str, rel: str, sha: str) -> bytes:
    """Bytes de un input `origen: repo`: de `inputs[clave]["bytes"]` si corrida0 los dio, si no del árbol;
    el sha se exige igual en los dos casos."""
    b = (inputs or {}).get(clave, {}).get("bytes")
    if b is None:
        b = open(os.path.join(RAIZ, rel), "rb").read()
    if isinstance(b, str):
        b = b.encode("utf-8")
    if hashlib.sha256(b).hexdigest() != sha:
        raise G.ParoDeGuardia(f"sha discordante: {rel}")
    return b


def modulo(nombre: str, b: bytes):
    m = types.ModuleType(nombre)
    m.__file__ = f"<{nombre}>"
    exec(compile(b, m.__file__, "exec"), m.__dict__)
    return m


def json_repo(inputs, clave, rel, sha):
    return json.loads(bytes_repo(inputs, clave, rel, sha))


# ── resultados ───────────────────────────────────────────────────────────────
GLOBALES = (
    ("DICTAMEN", "texto", "vocabulario cerrado CALIBRADO/SUBCUBRE/SOBRECUBRE/NO-ESTIMABLE", False),
    ("K", "entero", "celdas con R dentro del IC del contendiente", False),
    ("N", "entero", "celdas puntuadas", False),
    ("WILSON-LO", "proporcion", "IC de Wilson 95% de k/n, inferior", True),
    ("WILSON-HI", "proporcion", "IC de Wilson 95% de k/n, superior", True),
    ("MAE-PUNTO", "flotante", "error absoluto medio punto del contendiente vs R (descriptivo)", True),
    ("MARCA", "texto", "PROSPECTIVA (contendiente sellado antes de R)", False),
)


def esquema(P: str, celdas: list[str], unidad_r: str = "proporción ponderada en la ola reservada",
            tipo_r: str = "proporcion") -> list[dict]:
    """`tipo_r` = "flotante" cuando R no es una proporción (media, gasto): la cobertura no cambia."""
    out = [{"id": f"{P}-{c}-R", "tipo": tipo_r, "unidad": unidad_r, "permite_no_estimable": True}
           for c in celdas]
    for k, tipo, unidad, ne in GLOBALES:
        f = {"id": f"{P}-{k}", "tipo": tipo, "unidad": unidad}
        if ne:
            f["permite_no_estimable"] = True
        out.append(f)
    return out


def _fin(x):
    return float(x) if isinstance(x, (int, float)) and x == x and abs(x) != float("inf") else None


def salida(P: str, filas: list[dict]) -> dict:
    """`filas`: dicts con `id` (celda), `lo`, `hi`, `punto`, `r`, `conglomerado`. Devuelve el dict de
    resultados con exactamente los ids de `esquema(P, [f["id"] for f in filas])`."""
    adj = G.adjudica_cobertura(filas)
    out = {f"{P}-{f['id']}-R": _fin(f.get("r")) for f in filas}
    out.update({f"{P}-DICTAMEN": adj["dictamen"], f"{P}-K": int(adj["k"]), f"{P}-N": int(adj["n"]),
                f"{P}-WILSON-LO": _fin(adj["wilson_lo"]), f"{P}-WILSON-HI": _fin(adj["wilson_hi"]),
                f"{P}-MAE-PUNTO": _fin(adj["mae_punto"]), f"{P}-MARCA": "PROSPECTIVA"})
    return out


# ── manifiesto (solo sha y raíz; nunca el payload) ──────────────────────────
_MANIF = None


def entrada_manifiesto(pid: str) -> dict:
    global _MANIF
    if _MANIF is None:
        with open(os.path.join(RAIZ, "data", "manifiesto.yaml"), encoding="utf-8") as f:
            _MANIF = {e["id"]: e for e in yaml.load(f, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))}
    return _MANIF.get(pid, {})


# ── contrato corrida0 ───────────────────────────────────────────────────────
def ruta_contrato(x: str) -> str:
    return f"{EXP}/{x}/APERTURA-{x}-spec.yaml"


def contrato_dict(med_rel: str, M) -> dict:
    C = M.CONTRATO
    x = C["x"]
    md_rel = f"{EXP}/{x}/APERTURA-{x}-spec-v1_0.md"
    inputs = []
    for pid, nota in C["payloads"]:
        e = entrada_manifiesto(pid)
        inputs.append({"id": pid, "origen": "manifiesto", "sha256": e.get("sha256", "AUSENTE-DEL-MANIFIESTO"),
                       "funcion": "DATO", "nota": nota})
    for clave, rel, nota in C["repo"]:
        inputs.append({"id": clave, "origen": "repo", "ruta": rel, "sha256": sha256_de(rel),
                       "funcion": "CODIGO" if rel.endswith(".py") else "DATO", "nota": nota})
    return {
        "calc_id": f"CALC-APERTURA-{x}-0001",
        "spec_md": f"../../../{md_rel}",
        "spec_md_sha256": sha256_de(md_rel),
        "script": med_rel,
        "dependencias_materiales": list(C.get("dependencias", ["numpy", "pandas"])),
        "etiquetas": {"generacion": "GEN2", "uso_motor": "NO-ADOPTA-NADA", "cuenta_gen2": "NO",
                      "fuente_acto": ACTO, "tipo": "APERTURA-PRE-REGISTRADA (COMMIT-3 de la ola reservada)",
                      "agrupacion": "UNA-SOLA-VARIABLE", "marca": "PROSPECTIVA",
                      "unidad_transferencia": C.get("unidad", "PERSONA"),
                      "contendientes": list(C["contendientes"]),
                      "ola_reservada": f"{C['programa']} {C['ola']} (se abre sólo al correr este CALC)",
                      "congelado": "NO -- expediente; se congela cuando mesa firme su apertura"},
        "inputs": inputs,
        "variables": list(C["variables"]),
        "universo": C["universo"], "filtros": C["filtros"], "ponderador": C["ponderador"],
        "transformacion": C["transformacion"], "estimando": C["estimando"],
        "seed": {"aplica": False, "razon": "R es un punto; la cobertura usa el IC ya sellado del contendiente"},
        "parametros": {"nominal": 0.95, "z": 1.959964,
                       "regla": "cobertura R en [lo, hi] del contendiente; Wilson 95%; "
                                "NO-ESTIMABLE > SUBCUBRE > SOBRECUBRE > CALIBRADO",
                       "columna_ausente_en_catalogo": "NO-ESTIMABLE (sin recodificación ad hoc)"},
        "tolerancia": {"tipo": "flotante", "abs": 1e-10, "razon": "determinista: sumas float64 sin remuestreo"},
        "resultados": M.esquema_resultados(),
    }


def texto_contrato(med_rel: str, M) -> str:
    x = M.CONTRATO["x"]
    d = contrato_dict(med_rel, M)
    cab = (f"# CALC-APERTURA-{x}-0001 -- contrato ejecutable del expediente de apertura (D-15), {ACTO}.\n"
           f"# NO CORRIDO. La apertura es copiar este archivo a data/corrida0/CALC-APERTURA-{x}-0001/spec.yaml;\n"
           f"# el primer resultado que produzca es el que se reporta. Derivado por expediente_apertura.escribe_contrato.\n")
    return cab + yaml.safe_dump(d, allow_unicode=True, sort_keys=False, width=110)


def escribe_contrato(med_rel: str, M) -> str:
    rel = ruta_contrato(M.CONTRATO["x"])
    with open(os.path.join(RAIZ, rel), "w", encoding="utf-8") as f:
        f.write(texto_contrato(med_rel, M))
    return rel


def ruta_receta(x: str) -> str:
    return f"{EXP}/{x}/RECETA-APERTURA-{x}.md"


def texto_receta(M) -> str:
    C = M.CONTRATO
    x, prog, ola = C["x"], C["programa"], C["ola"]
    return f"""# Receta de apertura de un commit · {prog} {ola}

Derivada por `expediente_apertura.escribe_receta` ({ACTO}). El acto de apertura no diseña nada; si un paso
no se sostiene, PARA.

1. **Firma**: la fila de mesa que autorice abrir (`firma_que_faltaria` en `data/corrida0/aperturas-pendientes-v1_0.tsv`).
2. **Caja** (A.2, E.6): `python3 tools/entorno.py --arranque` debe decir CAJA.
3. **Preflight documental** (no es abrir; E.6 permite cuestionario, FD y catálogo): para cada variable de
   `APERTURA-{x}-spec.yaml::variables`, el cuestionario/catálogo de {ola} trae el mismo texto de pregunta y
   códigos; la que no, sale NO-ESTIMABLE (spec §5). Salida cruda a la nota del acto.
4. **Un commit (apertura)**:
   a. Levantar custodia de cada payload de `inputs` con `raiz: reserva_respondentes` (`corrida0` no lee esa
      raíz por construcción: `input_manifiesto_FUERA_DE_PERIMETRO`): mover el archivo a `data_raw` con la misma
      ruta relativa y, en `data/manifiesto.yaml`, quitar `estado_reserva` y poner `raiz: data_raw` (pareja que
      exige `tests/manifiesto.py`); `sha256` no cambia. Payload con `raiz` `data_raw`/`descargas_mx`: nada que mover.
   b. `mkdir data/corrida0/CALC-APERTURA-{x}-0001 && cp {EXP}/{x}/APERTURA-{x}-spec.yaml
      data/corrida0/CALC-APERTURA-{x}-0001/spec.yaml`.
   c. `python3 tools/corrida0.py preflight CALC-APERTURA-{x}-0001` → VERDE (el expediente lo simuló sin payload:
      ver la nota del acto que lo escribió).
5. **Run**: `python3 tools/corrida0.py run CALC-APERTURA-{x}-0001`. El medidor corre la auditoría AST antes
   de leer; devuelve R por celda, `-DICTAMEN`, `-K`, `-N`, Wilson, `-MAE-PUNTO`, `-MARCA`.
6. **Asiento**: registro por el job de derivados; `forense/replay-evidencia.tsv` (E.7); re-rótulo de la reserva
   de la ola en el manifiesto por el acto que lo tenga en su perímetro. Contendientes servidos a la vez (E.6):
   {", ".join(C["contendientes"])}.
"""


def escribe_receta(M) -> str:
    rel = ruta_receta(M.CONTRATO["x"])
    with open(os.path.join(RAIZ, rel), "w", encoding="utf-8") as f:
        f.write(texto_receta(M))
    return rel


# ── mutaciones para la prueba (E.6: guardia probada por mutación) ───────────
MUTACIONES = [
    "def _m(df):\n    return df.groupby(['a', 'b']).size()\n",
    "def _m(df):\n    return df.groupby(by=('a', 'b')).mean()\n",
    "def _m(df):\n    return df.value_counts(subset=['a', 'b'])\n",
    "import pandas as pd\ndef _m(df):\n    return pd.crosstab(df.a, df.b)\n",
    "def _m(df):\n    return df.pivot_table(index='a', columns='b')\n",
    "def _m(df):\n    return df.unstack()\n",
    "import pandas as pd\ndef _m(r):\n    return pd.read_stata(r)\n",
    "def _m(R, r):\n    return R.lee_dta(r, [])\n",
    "import pandas as pd\ndef _m(r):\n    return pd.read_csv(r)\n",
    "def _m(M, r):\n    return M._lee_dta(r, [])\n",
]
