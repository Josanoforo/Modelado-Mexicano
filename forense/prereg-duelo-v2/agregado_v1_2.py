#!/usr/bin/env python3
"""Agregado sellado v1_2 sobre las 14 celdas de `marco-M-sorteado-v1_2.tsv`.

ACTO: MAESTRA36-N2 · CIERRA-N3-AGREGA-2 (nube). Ejecuta P1 del encargo
`MAESTRA34-N3 · AGREGA-2` (`forense/encargos/cola/2026-09-01-MAESTRA34-N3
-AGREGA-2.md`, cuerpo línea 25 + ENMIENDA 5). Aplica, SIN editarlo, el
mismo procedimiento SELLADO `procedimiento-scoring-v1_1.md` que
`agregado_v1_1.py`/`agregado_v1_1b.py` ya aplican para v1.1 — este script
IMPORTA `agregado_v1_1.py` POR RUTA (mismo patrón que `agregado_v1_1b.py`
usa para importar la misma base) y no le toca ni una línea. Solo
sobreescribe, en la instancia importada, cuatro cosas — monkeypatch
quirúrgico, mismo patrón que `agregado_v1_1b.py` declara para su único
override (`_leer_l_variante`):

  1. `MARCO_TSV` → `marco-M-sorteado-v1_2.tsv` (14 celdas en vez de 11).
  2. `UNIVERSO_11` → las 14 celdas de v1_2 (el nombre de la constante en
     el módulo base sigue diciendo "11": renombrarla sería editar
     `agregado_v1_1.py`, fuera de perímetro; aquí se sobreescribe su
     VALOR en la instancia importada, no su nombre en el archivo).
  3. `_leer_m` → intenta primero `M-<id>.json` (las 7 celdas heredadas de
     v1_1 — `CIV-M-01`, `CIV-M-12`, `CIV-M-13`, `FAM-M-01`, `TRA-M-02`,
     `TRA-M-03`, `TRA-M-07` — cuyo M no cambió de valor entre versiones
     del marco) y si no existe, `M-<id>__v1_2.json` (las 7 celdas nuevas
     de v1_2 — `CIV-M-02`, `CIV-M-04`, `CIV-M-10`, `DIN-M-01`,
     `FAM-M-05`, `FAM-M-06`, `FAM-M-07`). Son los dos patrones de nombre
     REALES que `corridas-M/` trae hoy — verificados por `ls` antes de
     escribir este script, no supuestos.
  4. `_leer_l_variante` → lee de `L-extraido-v1_2.tsv` en vez de
     `valor_extraido` (siempre `null` en las capturas crudas), mismo
     patrón que `agregado_v1_1b.py` aplica para v1_1 con
     `L-extraido-v1_1.tsv` — 224 filas esperadas (14 celdas × 2 variantes
     × 8 réplicas) en vez de 176.

`DIN-M-01` NO recibe ningún tratamiento especial en este script: entra al
bucle igual que las otras 13, con su `R`/`EE_R` real de
`corridas-R/DIN-M-01.json` (`EE_R` = la aproximada, cota inferior, factor
de diseño `1.1997866170250338` — `exclusiones-v1_2.md:36-47`, firma `d1`)
y su `M` real de `corridas-M/M-DIN-M-01__v1_2.json`. La RESERVA de `d1`
(veredicto con las DOS `EE`, aproximada y sin_diseño) ya fue calculada
aparte por `din_m_01_doble_ee.py` (ENMIENDA 5) y NO se recalcula aquí — el
veredicto de banda es el MISMO con ambas `EE` (`FUERA-DE-BANDA`), así que
la cifra que este agregado usa (con `EE_R` aproximada) es consistente con
esa reserva, citada en el scoreboard, no reproducida.

Efecto secundario declarado, no oculto, del bloque `tra_m_02_informativo`
de `agregado_v1_1.py` (sin editar): en v1.1, `TRA-M-02` vivía FUERA del
universo de 11 celdas (esquema `v1_0`, pre-F-DD, `FP-213`) y ese bloque
existía para reportarla aparte. En v1.2, `TRA-M-02` SÍ está en el universo
de 14 — la entrada autoritativa es `celdas.TRA-M-02`. El bloque
`tra_m_02_informativo` de la salida queda como un duplicado vestigial (ya
con `R`/`M` reales, porque el `_leer_m` sobreescrito también lo alimenta) —
no se suprime porque suprimirlo exigiría editar el módulo base; se declara
aquí y en la nota de cierre.

Uso::

    python3 forense/prereg-duelo-v2/agregado_v1_2.py
        -- escribe agregado-v1_2-resultado.json y lo imprime a stdout
           (mismo formato determinista que agregado_v1_1.py/agregado_v1_1b.py).
"""
from __future__ import annotations

import csv
import importlib.util
import json
import statistics
import sys
from pathlib import Path
from typing import Any

DIR = Path(__file__).resolve().parent

_RUTA_AGREGADO = DIR / "agregado_v1_1.py"
_SPEC = importlib.util.spec_from_file_location("agregado_v1_1_base_para_v1_2", _RUTA_AGREGADO)
_BASE = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _BASE
_SPEC.loader.exec_module(_BASE)  # agregado_v1_1.py NO se edita -- se importa por ruta

MARCO_TSV_V1_2 = DIR / "marco-M-sorteado-v1_2.tsv"
L_TSV_V1_2 = DIR / "L-extraido-v1_2.tsv"
N_FILAS_L_ESPERADAS = 224  # 14 celdas x 2 variantes x 8 replicas

UNIVERSO_V1_2 = [
    "CIV-M-01", "CIV-M-02", "CIV-M-04", "CIV-M-10", "CIV-M-12", "CIV-M-13",
    "DIN-M-01", "FAM-M-01", "FAM-M-05", "FAM-M-06", "FAM-M-07",
    "TRA-M-02", "TRA-M-03", "TRA-M-07",
]

# --- 1) marco y universo: sobreescribe el VALOR de las constantes del
#     modulo importado, sin tocar el archivo agregado_v1_1.py ------------
_BASE.MARCO_TSV = MARCO_TSV_V1_2
_BASE.UNIVERSO_11 = UNIVERSO_V1_2  # nombre heredado del modulo base, sin renombrar


# --- 2) M: dos patrones de nombre reales en corridas-M/ (verificado por
#     `ls` antes de escribir esto, ver nota de cierre) -------------------
def _leer_m_v1_2(id_celda: str) -> dict[str, Any] | None:
    for nombre in (f"M-{id_celda}.json", f"M-{id_celda}__v1_2.json"):
        ruta = _BASE.CORRIDAS_M / nombre
        if ruta.exists():
            with ruta.open(encoding="utf-8") as fh:
                return json.load(fh)
    return None


_BASE._leer_m = _leer_m_v1_2


# --- 3) L: mismo patron que agregado_v1_1b.py, sobre L-extraido-v1_2.tsv -
def _cargar_l_tsv_v1_2() -> dict[tuple[str, str], list[float]]:
    """id_celda,variante -> lista de valores EXTRAIBLE (ya en [0,1])."""
    tabla: dict[tuple[str, str], list[float]] = {}
    n_filas = 0
    with L_TSV_V1_2.open(encoding="utf-8") as fh:
        for fila in csv.DictReader(fh, delimiter="\t"):
            n_filas += 1
            if fila["estado"] != "EXTRAIBLE":
                continue
            clave = (fila["id_celda"], fila["variante"])
            tabla.setdefault(clave, []).append(float(fila["valor"]))
    assert n_filas == N_FILAS_L_ESPERADAS, (
        f"esperaba {N_FILAS_L_ESPERADAS} filas en {L_TSV_V1_2.name}, encontré {n_filas}"
    )
    return tabla


_TABLA_L_V1_2 = _cargar_l_tsv_v1_2()


def _leer_l_variante_v1_2(id_celda: str, variante: str) -> tuple[float | None, int, int]:
    """Reemplaza a `agregado_v1_1._leer_l_variante` -- mismo colapso
    mecánico (media de las réplicas EXTRAIBLE), ahora sobre
    `L-extraido-v1_2.tsv` en vez de `valor_extraido` (siempre null en las
    capturas crudas), igual que `agregado_v1_1b.py` hace para v1.1."""
    valores = _TABLA_L_V1_2.get((id_celda, variante), [])
    n_examinadas = _BASE.K_REPLICAS_L  # las 8 replicas por (celda,variante) existen como archivo
    if not valores:
        return None, n_examinadas, 0
    return statistics.fmean(valores), n_examinadas, len(valores)


_BASE._leer_l_variante = _leer_l_variante_v1_2


def main() -> dict[str, Any]:
    resultado = _BASE.main()

    # `hallazgo_declarado` en el modulo base describe el estado de v1_1
    # ANTES del extractor (176 capturas, todas valor_extraido=null). Ya no
    # es cierto aqui -- se corrige explicitamente, mismo patron que
    # agregado_v1_1b.py aplica para su propio hallazgo_declarado, en vez de
    # dejar el texto viejo colgando con la cifra equivocada (176 en vez de
    # 224).
    resultado["hallazgo_declarado"] = {
        "valor_extraido_null_en_las_224_capturas_l": True,
        "nota_v1_2": (
            "Sigue siendo cierto que valor_extraido es null en las 224 capturas crudas de "
            "corridas-L/ para v1.2 -- eso no cambia (las capturas no se editan). El punto de L "
            "de este agregado se lee de L-extraido-v1_2.tsv (extractor tools/extrae_l_v1_1.py, "
            "parcheado por PR #497/ENMIENDA 3), no de valor_extraido. "
            "n_archivos_l_con_valor_extraido_no_nulo de abajo cuenta EXTRAIBLE en el TSV, no "
            "valor_extraido != null."
        ),
        "n_archivos_l_examinados": resultado["hallazgo_declarado"]["n_archivos_l_examinados"],
        "n_archivos_l_con_valor_extraido_no_nulo": (
            resultado["hallazgo_declarado"]["n_archivos_l_con_valor_extraido_no_nulo"]
        ),
    }

    resultado["version_marco"] = "v1_2"
    resultado["fuente_l"] = {
        "tsv": str(L_TSV_V1_2.relative_to(DIR.parents[1])),
        "extractor": "tools/extrae_l_v1_1.py (parcheado por PR #497, ENMIENDA 3, sha efb71de1...)",
        "nota": (
            "agregado_v1_1.py (base, sin editar) queda como estaba, describiendo v1_1 con "
            "valor_extraido null. Este script (v1_2) es el mismo cálculo con marco, universo, "
            "fuente de M y fuente de L sobreescritos por monkeypatch quirúrgico, sin tocar el "
            "módulo base."
        ),
    }
    resultado["din_m_01_reserva_d1"] = {
        "descripcion": (
            "DIN-M-01 puntúa en este agregado con EE_R (aproximada, cota inferior, factor de "
            "diseño 1.1997866170250338). La reserva d1/FP-249 exige declarar si el veredicto de "
            "banda cambia con EE_R_sin_diseno: NO cambia (FUERA-DE-BANDA en ambas), calculado por "
            "forense/prereg-duelo-v2/din_m_01_doble_ee.py (ENMIENDA 5), NO recalculado aquí."
        ),
        "fuente": "forense/prereg-duelo-v2/din-m-01-doble-ee-resultado.json",
        "veredicto_cambia_entre_EE": False,
        "cuenta_como_puntuada": True,
    }
    resultado["tra_m_02_informativo"]["nota_v1_2"] = (
        "En v1.1 TRA-M-02 vivía fuera del universo de 11 (esquema v1_0, pre-F-DD, FP-213); este "
        "bloque del módulo base la reportaba aparte. En v1.2 TRA-M-02 SÍ está en el universo de "
        "14 -- la entrada autoritativa es celdas.TRA-M-02, no este bloque, que queda vestigial "
        "(duplicado, ahora con R/M reales) por venir del script sellado sin editar."
    )

    # --- Segunda mitad de la "pregunta doble" del whitepaper (P2 del
    # encargo, cuerpo línea 26): IC pareado L+corpus-M, ADEMAS del
    # L_solo-M que agregado_v1_1.py ya computa como su única "comparación
    # principal" del contrato F1 (procedimiento-scoring-v1_1.md §3).
    # NO se copian _bootstrap_pareado_z ni _adjudicar -- se REUTILIZAN por
    # referencia desde el módulo base, mismas funciones que
    # comparacion_principal_pareada ya usa, con datos distintos (L+corpus
    # en vez de L-solo). Es diagnóstico secundario, no la comparación
    # principal sellada.
    pares_l_corpus_m = [
        (c["z_L_corpus"], c["z_M"])
        for c in resultado["celdas"].values()
        if c.get("z_L_corpus") is not None and c.get("z_M") is not None
    ]
    pareado_l_corpus = _BASE._bootstrap_pareado_z("pareado::L_CORPUS_vs_M::v1_2", pares_l_corpus_m)
    veredicto_l_corpus = _BASE._adjudicar(pareado_l_corpus.get("ic_lo"), pareado_l_corpus.get("ic_hi"))
    resultado["comparacion_secundaria_l_corpus_vs_m"] = {
        "id": "L_CORPUS_vs_M",
        "universo_pareado_ids": [
            cid for cid, c in resultado["celdas"].items()
            if c.get("z_L_corpus") is not None and c.get("z_M") is not None
        ],
        **pareado_l_corpus,
        "veredicto": veredicto_l_corpus,
        "nota": (
            "Diagnóstico secundario para la 'pregunta doble' del whitepaper (P2 del encargo, "
            "cuerpo línea 26: 'pareado L_solo-M, L+corpus-M'). NO es la 'comparación principal' "
            "del contrato F1 -- esa sigue siendo L_SOLO_vs_M "
            "(procedimiento-scoring-v1_1.md §3, comparacion_principal_pareada arriba). Reutiliza, "
            "sin copiar ni editar, _bootstrap_pareado_z y _adjudicar de agregado_v1_1.py, con "
            "los pares (z_L_corpus, z_M) en vez de (z_L_solo, z_M)."
        ),
    }

    return resultado


if __name__ == "__main__":
    resultado = main()
    salida = DIR / "agregado-v1_2-resultado.json"
    with salida.open("w", encoding="utf-8") as fh:
        json.dump(resultado, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps(resultado, ensure_ascii=False, indent=1, sort_keys=True))
