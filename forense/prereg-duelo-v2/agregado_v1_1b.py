#!/usr/bin/env python3
"""Re-agregado v1_1-b -- carga L extraído (P3 de MAESTRA33-E21).

ACTO: MAESTRA33-E21 · L-EXTRAE-v1_1 (nube). Re-corre el mismo cálculo que
`agregado_v1_1.py` (mismo procedimiento SELLADO `procedimiento-scoring-v1_1
.md`, mismos parámetros `delta=0.5`, `nivel_ic=0.95`, `seed=42`,
`replicas=10000`), con la ÚNICA diferencia de que el punto de corredor `L`
por (celda, variante) ya NO sale de `valor_extraido` (null en las 176
capturas reales) sino de `forense/prereg-duelo-v2/L-extraido-v1_1.tsv`
(tools/extrae_l_v1_1.py, P2 del mismo acto).

`agregado_v1_1.py` NO se edita -- está fuera del perímetro de este acto y
es, en sí mismo, el registro histórico de que el extractor no existía el
1/sep/2026. Este script lo IMPORTA por ruta (mismo patrón que
`carga_l_v1_1.py` usa con `pipeline-L-adv1-m2.py`) y solo reemplaza, en la
instancia importada, la función `_leer_l_variante` -- toda la demás
mecánica (lectura de R/M, bootstrap, adjudicación, FP-221) es la MISMA
función, sin copiarla.

Uso:
    python3 forense/prereg-duelo-v2/agregado_v1_1b.py
        -- escribe agregado-v1_1b-resultado.json y deja el resultado
           también disponible para `scoreboard-v1_1-AGREGADO-b.md`.
"""
from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent

_RUTA_AGREGADO = DIR / "agregado_v1_1.py"
_SPEC = importlib.util.spec_from_file_location("agregado_v1_1_base", _RUTA_AGREGADO)
_BASE = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _BASE
_SPEC.loader.exec_module(_BASE)  # agregado_v1_1.py NO se edita -- se importa por ruta

L_TSV = DIR / "L-extraido-v1_1.tsv"


def _cargar_l_tsv() -> dict[tuple[str, str], list[float]]:
    """id_celda,variante -> lista de valores EXTRAIBLE (ya en [0,1])."""
    tabla: dict[tuple[str, str], list[float]] = {}
    n_filas = 0
    with L_TSV.open(encoding="utf-8") as fh:
        for fila in csv.DictReader(fh, delimiter="\t"):
            n_filas += 1
            if fila["estado"] != "EXTRAIBLE":
                continue
            clave = (fila["id_celda"], fila["variante"])
            tabla.setdefault(clave, []).append(float(fila["valor"]))
    assert n_filas == 176, f"esperaba 176 filas en {L_TSV.name}, encontré {n_filas}"
    return tabla


_TABLA_L = _cargar_l_tsv()


def _leer_l_variante_desde_tsv(id_celda: str, variante: str):
    """Reemplaza a `agregado_v1_1._leer_l_variante`: colapso mecánico de las
    réplicas EXTRAIBLE de (id_celda, variante) por MEDIA -- misma regla de
    colapso que la función original declaraba (media sobre las réplicas con
    punto disponible; NO-DISPONIBLE si cero réplicas EXTRAIBLE), ahora
    sobre el TSV de P2 en vez de sobre `valor_extraido` (siempre null en
    las capturas)."""
    valores = _TABLA_L.get((id_celda, variante), [])
    n_examinadas = _BASE.K_REPLICAS_L  # las 8 réplicas por (celda,variante) siempre existen como archivo
    if not valores:
        return None, n_examinadas, 0
    import statistics as _st
    return _st.fmean(valores), n_examinadas, len(valores)


# Monkeypatch quirúrgico: SOLO la función de colapso de L cambia de fuente.
_BASE._leer_l_variante = _leer_l_variante_desde_tsv


def main() -> dict:
    resultado = _BASE.main()
    # `hallazgo_declarado` en el módulo base describe el estado ANTES de
    # este acto (valor_extraido null en las 176). Ya no es cierto aquí --
    # se corrige explícitamente en vez de dejar el texto viejo colgando.
    resultado["hallazgo_declarado"] = {
        "valor_extraido_null_en_las_176_capturas_l": True,
        "nota_v1_1b": (
            "Sigue siendo cierto que `valor_extraido` es null en las 176 "
            "capturas -- ESO no cambió (las capturas no se editan). Lo que "
            "cambia en v1_1b es que el punto de L ya no se lee de "
            "`valor_extraido`: se lee de L-extraido-v1_1.tsv (P2 de este "
            "acto, tools/extrae_l_v1_1.py), que aplicó la regla congelada "
            "sobre texto_crudo. n_archivos_l_con_valor_extraido_no_nulo de "
            "abajo cuenta EXTRAIBLE en el TSV, no valor_extraido != null."
        ),
        "n_archivos_l_examinados": resultado["hallazgo_declarado"]["n_archivos_l_examinados"],
        "n_archivos_l_con_valor_extraido_no_nulo": resultado["hallazgo_declarado"]["n_archivos_l_con_valor_extraido_no_nulo"],
    }
    resultado["fuente_l"] = {
        "tsv": str(L_TSV.relative_to(DIR.parents[1])),
        "regla": "forense/prereg-duelo-v2/regla-extraccion-L-v1_1.md",
        "extractor": "tools/extrae_l_v1_1.py",
        "nota": (
            "agregado_v1_1.py (base, sin editar) queda como estaba: registra "
            "que valor_extraido es null en las 176 capturas y que el "
            "universo L/pareado sale en 0. Este script (b) es el mismo "
            "cálculo con el punto de L tomado de L-extraido-v1_1.tsv en vez "
            "de valor_extraido."
        ),
    }
    return resultado


if __name__ == "__main__":
    resultado = main()
    salida = DIR / "agregado-v1_1b-resultado.json"
    with salida.open("w", encoding="utf-8") as fh:
        json.dump(resultado, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps(resultado, ensure_ascii=False, indent=1, sort_keys=True))
