#!/usr/bin/env python3
"""Corredor L SUCESOR -- consume `L-spec-v1_2.json` (14 celdas) directo.

ACTO GEN2-E7 · READINESS-2 · Pieza A, A3. Archivo NUEVO: no edita
`runner_l_cli.py`, no edita `carga_l_v1_1.py`, no edita
`pipeline-L-adv1-m2.py`, no re-nombra ni re-corre una sola captura existente.

## Por qué un sucesor y no un parche

`runner_l_cli.py` importa `carga_l_v1_1.py`, y `carga_l_v1_1.py` tiene
cableado `L_SPEC_JSON = DIR / "L-spec-v1_1.json"`: es el **cargador del
universo v1.1**, 11 celdas, con un `assert len(celdas) == 11` en su dry-run.
El universo del marcador es el de `L-spec-v1_2.json`: **14 celdas**. Un parche
sobre el cargador v1.1 lo convertiria en dos cosas a la vez y romperia el
dry-run que ese archivo ya declara. Se sucede, no se parchea.

De paso, este sucesor deja de necesitar el `celda_a_spec` de v1.1, que
rellenaba `variable`/`estimador` colapsando a `conducta` y dejaba
`frase_discriminacion` vacia para poder alimentar un `SpecCelda` escrito
para el marco piloto. `L-spec-v1_2.json` ya trae el campo `pregunta_L`
redactado y sellado por celda: el prompt se toma **verbatim** de ahi, sin
re-derivarlo y sin pasar por el pipeline del piloto.

## LEGACY-NO-LEIDO

Las 424 capturas de `corridas-L/` son **GEN1**. Este corredor no las abre:
ni para reusarlas, ni para saltear trabajo hecho, ni para verificar su propio
esquema de salida contra un ejemplo de ellas (que es lo que hacen el dry-run
de `runner_l_cli.py` y el de `carga_l_v1_1.py`). El esquema de salida se
declara aqui, en `ESQUEMA_SALIDA`, y se comprueba contra esa declaracion.

Su directorio de salida es **`corridas-L-gen2/`**, no `corridas-L/`: ninguna
corrida de este acto puede aterrizar encima de una captura GEN1 ni
confundirse con ella al listar.

## CONTADOR: cero

Este acto **no llama a ningun modelo**. El unico modo que se ejerce es
`--dry-run`: construye las 14 x 2 x 8 = 224 corridas (rutas, prompts, comando
CLI exacto, parametros) y no toca la red. El modo `--correr` queda escrito
para la sesion ejecutora futura y **no se ejerce aqui**.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT = DIR.parents[1]

L_SPEC_JSON = DIR / "L-spec-v1_2.json"
SALIDA = DIR / "corridas-L-gen2"

# El legado GEN1 que este corredor NO abre (Pieza B, check LEGACY-NO-LEIDO).
LEGADO_PROHIBIDO = ("corridas-L", "corridas-M", "corridas-R",
                    "agregado_v1_3.py", "L-spec-v1_1.json",
                    "carga_l_v1_1.py", "runner_l_cli.py")

# Invariantes sellados por `prereg-corrida-v1_0.md` F2(a) + enmienda
# 2026-09-01 (la que sustituyo la API por el CLI). NO se re-declaran con otro
# valor: se copian.
MODELO_ALIAS = "opus"
SISTEMA_MINIMO = ("Responde únicamente a la pregunta. No uses herramientas ni "
                  "consultes fuentes.")
K_CORRIDAS_SELLADO = 8
VARIANTES = ("L-solo", "L+corpus")
CORPUS_ID = "corpus-tierizado-v1_1"
SPEC_VERSION = "v1_2-gen2"
N_CELDAS_ESPERADAS = 14

# Esquema de salida DECLARADO -- no derivado de una captura GEN1.
ESQUEMA_SALIDA = (
    "id_celda", "variante", "indice", "spec_version", "modelo_alias",
    "modelo_real", "sistema_prompt", "prompt", "sha256_prompt",
    "comando", "k_corridas", "corpus_id_si_aplica", "texto_crudo",
    "fecha_utc", "generacion",
)


class UniversoInesperado(AssertionError):
    """`L-spec-v1_2.json` dejo de traer 14 celdas. Se levanta en vez de correr
    sobre un universo que no es el que este corredor declara."""


def cargar_celdas() -> list[dict]:
    """Consume `L-spec-v1_2.json`. No re-deriva la spec (ese es el trabajo del
    generador que la sello) y no la completa con nada de v1.1."""
    datos = json.loads(L_SPEC_JSON.read_text(encoding="utf-8"))
    celdas = datos["celdas"]
    if len(celdas) != N_CELDAS_ESPERADAS:
        raise UniversoInesperado(
            f"{L_SPEC_JSON.name} trae {len(celdas)} celdas, este corredor "
            f"declara {N_CELDAS_ESPERADAS}")
    return celdas


def prompt_de(celda: dict, variante: str) -> str:
    """El prompt VERBATIM de `pregunta_L`. La variante `L+corpus` antepone el
    encabezado de corpus sellado; no reescribe la pregunta."""
    pregunta = celda["pregunta_L"]
    if variante == "L+corpus":
        return f"[corpus disponible: {CORPUS_ID}]\n\n{pregunta}"
    return pregunta


def ruta_salida(id_celda: str, variante: str, indice: int) -> Path:
    """`corridas-L-gen2/L-<id>__<variante>__<k>__<spec>.json`. Directorio
    NUEVO: ninguna captura GEN1 de `corridas-L/` se pisa ni se relee."""
    return SALIDA / f"L-{id_celda}__{variante}__{indice:02d}__{SPEC_VERSION}.json"


def construir_comando_cli(prompt: str) -> list[str]:
    """Comando exacto, uno por corrida -- mismos invariantes que la enmienda
    del CLI sello: herramientas deshabilitadas, una sola vuelta, prompt de
    sistema REEMPLAZADO (no agregado)."""
    return ["claude", "-p", "--model", MODELO_ALIAS, "--output-format", "json",
            "--system-prompt", SISTEMA_MINIMO, "--tools", "", "--max-turns", "1",
            prompt]


def registro(celda: dict, variante: str, indice: int, prompt: str,
             texto_crudo: str | None = None,
             modelo_real: str | None = None) -> dict:
    """El JSON de una corrida. `modelo_real` queda `None` mientras el CLI no
    lo reporte -- nunca se inventa a partir del alias."""
    return {
        "id_celda": celda["id"],
        "variante": variante,
        "indice": indice,
        "spec_version": SPEC_VERSION,
        "modelo_alias": MODELO_ALIAS,
        "modelo_real": modelo_real,
        "sistema_prompt": SISTEMA_MINIMO,
        "prompt": prompt,
        "sha256_prompt": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "comando": construir_comando_cli(prompt),
        "k_corridas": K_CORRIDAS_SELLADO,
        "corpus_id_si_aplica": CORPUS_ID if variante == "L+corpus" else None,
        "texto_crudo": texto_crudo,
        "fecha_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generacion": "GEN2",
    }


def plan() -> list[tuple[dict, str, int]]:
    """Las 14 x 2 x 8 = 224 corridas, en orden estable."""
    return [(celda, variante, k)
            for celda in cargar_celdas()
            for variante in VARIANTES
            for k in range(1, K_CORRIDAS_SELLADO + 1)]


def dry_run() -> int:
    entradas = plan()
    problemas = []
    vistos = set()
    for celda, variante, k in entradas:
        prompt = prompt_de(celda, variante)
        reg = registro(celda, variante, k, prompt)
        faltan = set(ESQUEMA_SALIDA) - set(reg)
        sobran = set(reg) - set(ESQUEMA_SALIDA)
        if faltan or sobran:
            problemas.append(f"{celda['id']}/{variante}/{k}: esquema "
                             f"faltan={sorted(faltan)} sobran={sorted(sobran)}")
        ruta = ruta_salida(celda["id"], variante, k)
        if str(ruta) in vistos:
            problemas.append(f"ruta duplicada: {ruta}")
        vistos.add(str(ruta))
        if "/corridas-L/" in str(ruta).replace("\\", "/"):
            problemas.append(f"salida caeria en legado GEN1: {ruta}")

    print(f"corredor L sucesor · {L_SPEC_JSON.name} · {N_CELDAS_ESPERADAS} celdas")
    print(f"  variantes = {VARIANTES}   k = {K_CORRIDAS_SELLADO}")
    print(f"  corridas planificadas = {len(entradas)}")
    print(f"  rutas unicas          = {len(vistos)}")
    print(f"  salida                = {SALIDA.relative_to(ROOT)}  (NUEVO, no corridas-L/)")
    print(f"  legado NO abierto     = {', '.join(LEGADO_PROHIBIDO)}")
    print("  CONTADOR: cero -- este modo no invoca `claude` ni toca la red.")
    celda0, var0, k0 = entradas[0]
    print("\n  ejemplo (celda 1, L-solo, k=1):")
    print(f"    ruta   = {ruta_salida(celda0['id'], var0, k0).relative_to(ROOT)}")
    print(f"    sha256_prompt = {hashlib.sha256(prompt_de(celda0, var0).encode()).hexdigest()}")
    if problemas:
        print("\nPROBLEMAS:")
        for p in problemas:
            print("  -", p)
        return 1
    print("\nDRY-RUN: OK")
    return 0


def correr() -> int:
    """MODO REAL -- no ejercido por este acto. Reanudable por existencia de
    archivo: una corrida ya escrita no se repite."""
    SALIDA.mkdir(parents=True, exist_ok=True)
    for celda, variante, k in plan():
        ruta = ruta_salida(celda["id"], variante, k)
        if ruta.exists():
            continue
        prompt = prompt_de(celda, variante)
        proc = subprocess.run(construir_comando_cli(prompt),
                              capture_output=True, text=True)
        if proc.returncode != 0:
            print(f"FALLO {ruta.name}: exit={proc.returncode} {proc.stderr[:200]}",
                  file=sys.stderr)
            return 1
        datos = json.loads(proc.stdout)
        reg = registro(celda, variante, k, prompt,
                       texto_crudo=datos.get("result", ""),
                       modelo_real=datos.get("model"))
        ruta.write_text(json.dumps(reg, ensure_ascii=False, indent=1,
                                   sort_keys=True) + "\n", encoding="utf-8")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    modo = p.add_mutually_exclusive_group(required=True)
    modo.add_argument("--dry-run", action="store_true",
                      help="Unico modo que este acto ejerce -- no invoca `claude`.")
    modo.add_argument("--correr", action="store_true",
                      help="Modo real, NO ejercido por este acto.")
    args = p.parse_args()
    return dry_run() if args.dry_run else correr()


if __name__ == "__main__":
    raise SystemExit(main())
