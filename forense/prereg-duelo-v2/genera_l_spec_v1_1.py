#!/usr/bin/env python3
"""Genera `forense/prereg-duelo-v2/L-spec-v1_1.json` — spec pre-registrada de
la pregunta `L` para las 11 celdas de `marco-M-sorteado-v1_1.tsv` con
`elegible_v1_1 = SI`.

ACTO: MAESTRA33-E9 · L-SPEC-v1_1 (nube, Opus). Escrito 1/sep/2026, contra
SHA a71c9ea. Este script NO llama a ningún modelo -- solo lee el marco y
aplica la PLANTILLA_L (única, determinista) a cinco columnas por fila:
`conducta`, `universo`, `encuesta`, `ola`, `escala`. Ninguna cifra de
`corridas-R/`, `corridas-M/` ni de `scoreboard-v1_1.md` entra en la pregunta
-- este script no abre ninguno de esos tres.

Uso:  python3 forense/prereg-duelo-v2/genera_l_spec_v1_1.py
Salida: L-spec-v1_1.json + L-spec-v1_1.sha256, en el mismo directorio.

Re-ejecutar este script sobre el mismo marco produce byte-a-byte el mismo
JSON (determinismo por construcción: ninguna fuente de aleatoriedad, orden
de filas = orden del TSV, claves ordenadas al serializar).
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

DIR = Path(__file__).resolve().parent
MARCO = DIR / "marco-M-sorteado-v1_1.tsv"
SALIDA_JSON = DIR / "L-spec-v1_1.json"
SALIDA_SHA256 = DIR / "L-spec-v1_1.sha256"

# --------------------------------------------------------------------------
# Plantilla mecánica única -- parametrizada solo por las cinco columnas que
# el encargo nombra (conducta, universo, encuesta, ola, escala). Ningún
# texto por celda se redacta a mano; cambiar la pregunta de una celda
# significa cambiar esta función para las 11, nunca una fila suelta.
# --------------------------------------------------------------------------


def derivar_pregunta_l(conducta: str, universo: str, encuesta: str, ola: str, escala: str) -> str:
    return (
        f"En la encuesta {encuesta} (ola {ola}), para el universo \"{universo}\", "
        f"¿cuál es tu estimación de la proporción del universo que presenta la "
        f"conducta \"{conducta}\"? Escala de respuesta: {escala}. Da tu mejor "
        f"estimación puntual y, si no conoces el dato, dilo explícitamente -- "
        f"no inventes una cifra plausible."
    )


def cargar_celdas_elegibles(ruta_tsv: Path) -> list[dict]:
    with ruta_tsv.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        filas = list(reader)
    return [f for f in filas if f["elegible_v1_1"].strip().upper().startswith("SI")]


def construir_spec() -> dict:
    filas = cargar_celdas_elegibles(MARCO)
    celdas = []
    for f in filas:
        celdas.append(
            {
                "id": f["id"],
                "conducta": f["conducta"],
                "universo": f["universo"],
                "encuesta": f["encuesta"],
                "ola": f["ola"],
                "escala": f["escala"],
                "pregunta_L": derivar_pregunta_l(
                    conducta=f["conducta"], universo=f["universo"],
                    encuesta=f["encuesta"], ola=f["ola"], escala=f["escala"],
                ),
            }
        )
    return {
        "acto": "MAESTRA33-E9 · L-SPEC-v1_1",
        "sha_redaccion": "a71c9ea",
        "fecha": "2026-09-01",
        "fuente_marco": "forense/prereg-duelo-v2/marco-M-sorteado-v1_1.tsv",
        "columna_elegibilidad": "elegible_v1_1",
        "n_celdas": len(celdas),
        "derivacion": (
            "Cada pregunta_L se deriva MECÁNICAMENTE de las columnas "
            "conducta/universo/encuesta/ola/escala del marco vía la función "
            "derivar_pregunta_l() de forense/prereg-duelo-v2/genera_l_spec_v1_1.py "
            "-- una plantilla única, sin texto redactado a mano por celda."
        ),
        "declaracion": (
            "Al congelar esta spec existían corridas R para 4 de las 11 celdas "
            "(CIV-M-01/06/08/09, forense/prereg-duelo-v2/corridas-R/). Ninguna "
            "cifra de R entra en esta spec ni en los prompts que de ella se "
            "deriven -- este script no lee corridas-R/, corridas-M/ ni "
            "scoreboard-v1_1.md. El modelo L es externo (sesión limpia fuera "
            "del proyecto, D-iii) y no ve este repo: solo recibe el prompt que "
            "el cargador de forense/prereg-duelo-v2/carga_l_v1_1.py construye "
            "a partir de pregunta_L (ó, en variante L+corpus, pregunta_L más el "
            "corpus tierizado que el pipeline sellado ya contempla)."
        ),
        "pipeline_consumidor": "forense/prereg-duelo-v2/pipeline-L-adv1-m2.py (sellado, no editado por este acto)",
        "cargador": "forense/prereg-duelo-v2/carga_l_v1_1.py",
        "celdas": celdas,
    }


def main() -> None:
    spec = construir_spec()
    serial = json.dumps(spec, ensure_ascii=False, indent=2, sort_keys=True)
    SALIDA_JSON.write_text(serial + "\n", encoding="utf-8")
    digest = hashlib.sha256(SALIDA_JSON.read_bytes()).hexdigest()
    SALIDA_SHA256.write_text(f"{digest}  {SALIDA_JSON.name}\n", encoding="utf-8")
    print(f"{SALIDA_JSON} -- {spec['n_celdas']} celdas")
    print(f"{SALIDA_SHA256} -- {digest}")


if __name__ == "__main__":
    main()
