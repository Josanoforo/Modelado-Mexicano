#!/usr/bin/env python3
"""Cargador propio de `marco-M-sorteado-v1_1.tsv` para `pipeline-L-adv1-m2.py`
-- mismo patrón que `sorteo_v2.py` (importa el módulo sellado por ruta de
archivo, `SIN` editar una sola línea de `pipeline-L-adv1-m2.py`).

ACTO: MAESTRA33-E9 · L-SPEC-v1_1 (nube, Opus). Escrito 1/sep/2026, SHA a71c9ea.

*** ESTE SCRIPT NO LLAMA A NINGÚN MODELO EN ESTE ACTO. *** Igual que el
pipeline que envuelve, `llamar_modelo` sigue lanzando `NotImplementedError` --
este cargador no la rellena ni la parchea. Su función en este acto es
puramente de smoke-test: construir, para las 11 celdas de
`L-spec-v1_1.json`, el `SpecCelda` + `ParametrosCorredorL` que una sesión
ejecutora real usaría, y verificar que las rutas de salida y el esquema
coinciden con los de `corridas-L/` ya existentes -- sin tocar la red, sin
tocar `corridas-R/`, sin abrir `scoreboard-v1_1.md`.

Parámetros -- NO se re-declaran con otro valor, se importan de
`prereg-corrida-v1_0.md` F2(a)/(b)/(c) (mismos que `lanzamiento-L-v1_0.md`
usó para el marco piloto):
    modelo_id          = "claude-opus-4-6"
    temperatura         = 1.0
    k_corridas          = 8
    variantes           = ("L-solo", "L+corpus")
    agregado            = agregar_continua / agregar_categorica
                           (pipeline-L-adv1-m2.py, sección 5, NO reinventado
                           aquí -- se importa el módulo, no se copia código)

Uso:
    python3 forense/prereg-duelo-v2/carga_l_v1_1.py --dry-run
        -- construye specs+params+prompts+rutas para las 11 celdas × 2
           variantes, verifica el esquema contra un ejemplo real de
           corridas-L/, imprime un resumen. No escribe nada, no llama a
           ningún modelo.

Este script NUNCA se invoca sin --dry-run desde este acto -- no existe otro
modo. La sesión ejecutora real (fuera de este proyecto, D-iii) usa su propio
driver, descrito en PAQUETE-L-v1_1.md, que sí implementa `llamar_modelo`.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT = DIR.parents[1]

_RUTA_PIPELINE = DIR / "pipeline-L-adv1-m2.py"
_SPEC = importlib.util.spec_from_file_location("pipeline_L_adv1_m2", _RUTA_PIPELINE)
_PIPELINE = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _PIPELINE
_SPEC.loader.exec_module(_PIPELINE)  # pipeline-L-adv1-m2.py NO se edita -- se importa por ruta

SpecCelda = _PIPELINE.SpecCelda
ParametrosCorredorL = _PIPELINE.ParametrosCorredorL
construir_prompt = _PIPELINE.construir_prompt
hash_salida = _PIPELINE.hash_salida

L_SPEC_JSON = DIR / "L-spec-v1_1.json"

# Parámetros sellados por `prereg-corrida-v1_0.md` F2(a)/(b) -- idénticos a
# los que `lanzamiento-L-v1_0.md` usó para el marco piloto. No se cambian.
MODELO_ID_SELLADO = "claude-opus-4-6"
TEMPERATURA_SELLADA = 1.0
K_CORRIDAS_SELLADO = 8
VARIANTES = ("L-solo", "L+corpus")
FECHA_CONGELACION = "2026-09-01"


def cargar_celdas_l_spec() -> list[dict]:
    """Lee L-spec-v1_1.json -- NUNCA se reconstruye la derivación aquí; ese
    es el trabajo de genera_l_spec_v1_1.py. Este cargador solo consume."""
    with L_SPEC_JSON.open(encoding="utf-8") as fh:
        return json.load(fh)["celdas"]


def celda_a_spec(celda: dict) -> SpecCelda:
    """Adapta una fila de L-spec-v1_1.json al SpecCelda que
    pipeline-L-adv1-m2.py espera. El pipeline fue escrito para el marco
    piloto (columnas variable/estimador/frase_discriminacion); el marco-M
    no las trae bajo esos nombres -- se rellenan con la mejor
    correspondencia disponible sin inventar contenido: `variable` y
    `estimador` colapsan a la `conducta` (no hay columna separada en
    marco-M para esa distinción), `frase_discriminacion` queda vacía (esa
    columna del marco-M es de otro propósito -- censo de existencia, no
    reactivo -- y el encargo prohíbe redactar texto a mano por celda)."""
    return SpecCelda(
        id=celda["id"],
        encuesta=celda["encuesta"],
        ola=celda["ola"],
        universo=celda["universo"],
        variable=celda["conducta"],
        estimador=celda["conducta"],
        escala=celda["escala"],
        frase_discriminacion="",
    )


def ruta_salida(id_celda: str, variante: str, indice: int) -> Path:
    """corridas-L/L-<id>-M__<variante>__<k>.json -- esquema del encargo,
    prefijo L- y sufijo -M para no colisionar con las 120 capturas del
    marco piloto (CIV-08__L-solo__01.json, sin prefijo)."""
    return DIR / "corridas-L" / f"L-{id_celda}-M__{variante}__{indice:02d}.json"


def construir_params(variante: str, corpus_id: str | None = None) -> ParametrosCorredorL:
    return ParametrosCorredorL(
        modelo_id=MODELO_ID_SELLADO,
        version_declarada=MODELO_ID_SELLADO,  # provisional; la real la fija r.model en la corrida real
        fecha_congelacion=FECHA_CONGELACION,
        temperatura=TEMPERATURA_SELLADA,
        k_corridas=K_CORRIDAS_SELLADO,
        variante=variante,  # type: ignore[arg-type]
        corpus_id_si_aplica=corpus_id,
    )


def dry_run() -> int:
    celdas = cargar_celdas_l_spec()
    assert len(celdas) == 11, f"esperaba 11 celdas elegible_v1_1, encontré {len(celdas)}"

    # Esquema de referencia: un archivo real ya existente del marco piloto.
    ejemplos = sorted((DIR / "corridas-L").glob("CIV-08__L-solo__*.json"))
    assert ejemplos, "no encontré ningún ejemplo en corridas-L/ para verificar esquema"
    ejemplo = json.loads(ejemplos[0].read_text(encoding="utf-8"))
    claves_esperadas = {"id_celda", "variante", "indice", "texto_crudo", "valor_extraido", "fuente_citada", "timestamp", "params", "sha256_prompt"}
    assert claves_esperadas.issubset(ejemplo.keys()), f"esquema de ejemplo no trae las claves esperadas: {claves_esperadas - ejemplo.keys()}"

    n_prompts = 0
    n_rutas = 0
    rutas_vistas: set[Path] = set()
    for celda in celdas:
        spec = celda_a_spec(celda)
        for variante in VARIANTES:
            corpus_id = "corpus-tierizado-v1_1" if variante == "L+corpus" else None
            params = construir_params(variante, corpus_id)
            contexto_corpus = "" if variante == "L-solo" else "[contexto tierizado -- no construido en este acto]"
            prompt = construir_prompt(spec, params, contexto_corpus)
            assert prompt, f"prompt vacío para {celda['id']}/{variante}"
            n_prompts += 1
            for indice in range(1, params.k_corridas + 1):
                ruta = ruta_salida(celda["id"], variante, indice)
                assert ruta not in rutas_vistas, f"ruta colisionada: {ruta}"
                rutas_vistas.add(ruta)
                n_rutas += 1

    total_esperado = 11 * len(VARIANTES) * K_CORRIDAS_SELLADO
    assert n_rutas == total_esperado, f"{n_rutas} rutas construidas, esperaba {total_esperado}"

    # commit_hash_registry() se puede invocar con diccionarios vacíos/placeholder
    # para verificar que la función sigue firmando -- sin producir un registro
    # real (eso exige L, M, B, E reales, ninguno corre en este acto).
    _ = hash_salida({"smoke_test": True})

    print(f"OK -- {len(celdas)} celdas x {len(VARIANTES)} variantes x k={K_CORRIDAS_SELLADO} = {n_rutas} rutas de salida verificadas")
    print(f"OK -- {n_prompts} prompts construidos vía construir_prompt() (pipeline-L-adv1-m2.py, sin editar)")
    print(f"OK -- esquema de salida verificado contra {ejemplos[0].name}")
    print("OK -- llamar_modelo() NO se invocó ni se implementó en este acto (NotImplementedError intacto)")
    print(f"Ejemplo de ruta: {ruta_salida(celdas[0]['id'], 'L-solo', 1).relative_to(ROOT)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", required=True,
                         help="Único modo soportado en este acto -- no ejecuta L.")
    args = parser.parse_args()
    if args.dry_run:
        return dry_run()
    return 1  # inalcanzable -- --dry-run es required


if __name__ == "__main__":
    raise SystemExit(main())
