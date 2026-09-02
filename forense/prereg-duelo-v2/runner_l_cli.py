#!/usr/bin/env python3
"""Runner de la corrida `L` (marco-M v1_1, 11 celdas) vía Claude Code CLI en
modo print -- sustituye a la llamada directa a la API (`llamar_modelo()`,
`PAQUETE-L-v1_1.md` §4) que `PAQUETE-L-v1_1.md` §4-bis documenta.

ACTO: MAESTRA33-E17 · L-ENMIENDA-CLI (nube, `cloud_default`, repo-only).
Enmienda pre-registrada en `prereg-corrida-v1_0.md` (sección "F2 · enmienda
2026-09-01", fila fechada, procedimiento de `prereg-corrida-v1_0.md:56`).
Razón verbatim de la enmienda: firma de mesa, 2/sep/2026 -- "dame una opcion
donde no tenga que usar API ni gastar en API, la anterior se consumió 20
dolares de API y fue un reto la api key y todo eso."

*** ESTE SCRIPT NO LLAMA A NINGÚN MODELO EN ESTE ACTO. *** Igual que
`carga_l_v1_1.py`, el único modo que este acto ejercita es `--dry-run`:
construye rutas + prompts + comando CLI exacto para las 11 celdas × 2
variantes × k=8 y verifica el esquema de salida contra un ejemplo real de
`corridas-L/`, sin tocar la red y sin invocar `claude`. El modo real
(ejecutar corridas) queda implementado para la sesión ejecutora futura,
pero no se ejerce aquí -- CONTADOR: cero.

Invariantes de la corrida, sin cambio salvo los que la enmienda de P1 fija
(`prereg-corrida-v1_0.md` F2(a) + enmienda 2026-09-01):
    cliente             = Claude Code CLI en modo print (`claude -p`);
                          versión del cliente derivada de `claude --version`
                          al correr, no declarada aquí
    temperatura         = default del cliente, NO declarable (el CLI no
                          expone una bandera de temperatura en modo print)
    prompt de sistema   = reemplazo total por la cadena mínima fija de P1
                          (constante SISTEMA_MINIMO abajo)
    herramientas        = deshabilitadas (`--tools ""`)
    modelo_id           = "opus" (alias del CLI); nombre real de modelo
                          registrado por corrida desde el campo de modelo
                          del JSON de salida (`--output-format json`)
    k_corridas          = 8, SIN cambio
    variantes           = ("L-solo", "L+corpus"), SIN cambio

Uso:
    python3 forense/prereg-duelo-v2/runner_l_cli.py --dry-run
        -- construye specs+params+prompts+comando CLI+rutas para las 11
           celdas × 2 variantes × k=8, verifica el esquema contra un
           ejemplo real de corridas-L/, imprime un resumen. No escribe
           nada, no invoca `claude`.

    python3 forense/prereg-duelo-v2/runner_l_cli.py --correr
        -- MODO REAL, no ejercido por este acto. Invoca `claude -p` una vez
           por (celda, variante, índice), 176 llamadas en total. Reanudable:
           si un archivo de salida ya existe, esa corrida se salta -- no se
           repite lo ya hecho. Requiere `claude` en PATH con sesión de
           claude.ai activa (`claude auth status`, PAQUETE-L-v1_1.md §4-bis)
           -- NO requiere ni usa ANTHROPIC_API_KEY.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT = DIR.parents[1]

# `carga_l_v1_1.py` ya construye specs+params+rutas para las 11 celdas de
# L-spec-v1_1.json -- se importa por ruta, sin editarlo ni duplicar su
# derivación (mismo patrón que ese script usa para importar el pipeline).
_RUTA_CARGA = DIR / "carga_l_v1_1.py"
_SPEC_CARGA = importlib.util.spec_from_file_location("carga_l_v1_1", _RUTA_CARGA)
_CARGA = importlib.util.module_from_spec(_SPEC_CARGA)
sys.modules[_SPEC_CARGA.name] = _CARGA
_SPEC_CARGA.loader.exec_module(_CARGA)  # carga_l_v1_1.py NO se edita -- se importa por ruta

cargar_celdas_l_spec = _CARGA.cargar_celdas_l_spec
celda_a_spec = _CARGA.celda_a_spec
VARIANTES = _CARGA.VARIANTES
K_CORRIDAS_SELLADO = _CARGA.K_CORRIDAS_SELLADO

construir_prompt = _CARGA._PIPELINE.construir_prompt

# --------------------------------------------------------------------------
# Invariantes sellados por P1 (prereg-corrida-v1_0.md, "F2 · enmienda
# 2026-09-01") -- NO se re-declaran con otro valor aquí.
# --------------------------------------------------------------------------
MODELO_ALIAS = "opus"
SISTEMA_MINIMO = "Responde únicamente a la pregunta. No uses herramientas ni consultes fuentes."


def ruta_salida(id_celda: str, variante: str, indice: int) -> Path:
    """corridas-L/L-<id>-M__<variante>__<k>.json -- misma convención de
    nombres que `carga_l_v1_1.py::ruta_salida` (prefijo L-, sufijo -M para
    no colisionar con las 120 capturas del marco piloto). No se importa esa
    función directamente porque este runner escribe archivos reales (el
    dry-run del cargador nunca escribe) -- se replica la misma expresión."""
    return DIR / "corridas-L" / f"L-{id_celda}-M__{variante}__{indice:02d}.json"


def construir_comando_cli(prompt: str) -> list[str]:
    """Comando exacto que P2 fija, uno por corrida. `--tools ""` deshabilita
    herramientas; `--max-turns 1` fuerza una sola vuelta ciega; el prompt de
    sistema por defecto del CLI se reemplaza, no se agrega."""
    return [
        "claude", "-p",
        "--model", MODELO_ALIAS,
        "--output-format", "json",
        "--system-prompt", SISTEMA_MINIMO,
        "--tools", "",
        "--max-turns", "1",
        prompt,
    ]


def parsear_salida_cli(bruto: str) -> tuple[str, str | None]:
    """Extrae (texto_crudo, modelo_real) del JSON que `claude -p
    --output-format json` imprime en stdout. El texto de respuesta viaja en
    el campo `result`; el nombre real de modelo resuelto del alias viaja en
    `model` cuando el CLI lo reporta -- si esa clave no está presente en la
    versión del cliente que corra, `modelo_real` queda `None` y se declara
    así en el archivo, nunca inventado."""
    datos = json.loads(bruto)
    texto = datos.get("result", "")
    modelo_real = datos.get("model") or datos.get("modelo") or None
    return texto, modelo_real


def extraer_fuente_citada(texto: str) -> str | None:
    """Sonda canario -- misma heurística que el piloto: primer párrafo que
    mencione una fuente. Parseo real de `valor_extraido`/`fuente_citada`
    queda para el extractor congelado aparte (PAQUETE-L-v1_1.md §5, mismo
    patrón que el piloto) -- este runner solo captura, no interpreta."""
    return None


def ejecutar_corrida(spec, params_variante: str, prompt: str, id_celda: str, indice: int, params) -> dict:
    """`sha256_prompt` es el sha256 del prompt EXACTO que se envía (el último
    argumento de `construir_comando_cli`, hasheado utf-8) y `params` es lo que
    `construir_params` devuelve, serializado. Las dos claves restauran el
    esquema de 9 que `carga_l_v1_1.py:130` valida y que la corrida v1_1 perdió
    -- sin ellas, una captura no lleva prueba propia de con qué prompt nació
    (defecto medido el 2/sep sobre las 176 de v1_1: K=96). Firma DL-(1)."""
    comando = construir_comando_cli(prompt)
    resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
    texto_crudo, modelo_real = parsear_salida_cli(resultado.stdout)
    return {
        "id_celda": id_celda,
        "variante": params_variante,
        "indice": indice,
        "texto_crudo": texto_crudo,
        "valor_extraido": None,
        "fuente_citada": extraer_fuente_citada(texto_crudo),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "modelo_real": modelo_real,
        "params": asdict(params),
        "sha256_prompt": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
    }


def _iter_plan():
    """Genera (celda, spec, variante, indice, prompt, ruta) para las 11
    celdas x 2 variantes x k=8 -- mismo recorrido para --dry-run y --correr,
    así el conteo y el esquema que valida uno son los que el otro ejecuta."""
    celdas = cargar_celdas_l_spec()
    for celda in celdas:
        spec = celda_a_spec(celda)
        for variante in VARIANTES:
            contexto_corpus = "" if variante == "L-solo" else "[contexto tierizado -- no construido en este acto]"
            params = _CARGA.construir_params(variante, "corpus-tierizado-v1_1" if variante == "L+corpus" else None)
            prompt = construir_prompt(spec, params, contexto_corpus)
            for indice in range(1, K_CORRIDAS_SELLADO + 1):
                ruta = ruta_salida(celda["id"], variante, indice)
                yield celda, spec, variante, indice, prompt, ruta, params


def dry_run() -> int:
    n_rutas = 0
    n_prompts_vistos = set()
    rutas_vistas: set[Path] = set()

    ejemplos = sorted((DIR / "corridas-L").glob("CIV-08__L-solo__*.json"))
    assert ejemplos, "no encontré ningún ejemplo en corridas-L/ para verificar esquema"
    ejemplo = json.loads(ejemplos[0].read_text(encoding="utf-8"))
    claves_piloto = {"id_celda", "variante", "indice", "texto_crudo", "valor_extraido", "fuente_citada", "timestamp", "params", "sha256_prompt"}
    assert claves_piloto.issubset(ejemplo.keys()), f"esquema de ejemplo no trae las claves esperadas: {claves_piloto - ejemplo.keys()}"

    for celda, spec, variante, indice, prompt, ruta, _params in _iter_plan():
        assert prompt, f"prompt vacío para {celda['id']}/{variante}"
        n_prompts_vistos.add((celda["id"], variante))
        assert ruta not in rutas_vistas, f"ruta colisionada: {ruta}"
        rutas_vistas.add(ruta)
        comando = construir_comando_cli(prompt)
        assert comando[0] == "claude" and "-p" in comando
        assert "--tools" in comando and comando[comando.index("--tools") + 1] == ""
        assert SISTEMA_MINIMO in comando
        n_rutas += 1

    n_celdas = len(cargar_celdas_l_spec())
    total_esperado = n_celdas * len(VARIANTES) * K_CORRIDAS_SELLADO
    assert n_rutas == total_esperado, f"{n_rutas} rutas construidas, esperaba {total_esperado}"

    print(f"OK -- {len(n_prompts_vistos)} pares (celda, variante) x k={K_CORRIDAS_SELLADO} = {n_rutas} rutas de salida verificadas")
    print(f"OK -- esquema de salida (campos del piloto) verificado contra {ejemplos[0].name}")
    print(f"OK -- comando CLI construido para las {n_rutas} corridas: claude -p --model {MODELO_ALIAS} --output-format json --system-prompt '<P1>' --tools '' --max-turns 1 '<prompt>'")
    print("OK -- ningún subproceso `claude` invocado en este acto (--dry-run)")
    primer_celda, _, primera_variante, _, _, primera_ruta, _ = next(_iter_plan())
    print(f"Ejemplo de ruta: {primera_ruta.relative_to(ROOT)}")
    print(f"Total esperado: {total_esperado}")
    return 0


def correr() -> int:
    """MODO REAL -- no ejercido por este acto (CONTADOR: cero). Reanudable:
    salta cualquier (celda, variante, indice) cuyo archivo de salida ya
    exista, para que un corte por límite horario no repita lo ya hecho."""
    n_hechas = 0
    n_saltadas = 0
    for celda, spec, variante, indice, prompt, ruta, params in _iter_plan():
        if ruta.exists():
            n_saltadas += 1
            continue
        registro = ejecutar_corrida(spec, variante, prompt, celda["id"], indice, params)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
        n_hechas += 1

    total = n_hechas + n_saltadas
    print(f"OK -- {n_hechas} corridas nuevas, {n_saltadas} ya existentes (reanudación), total {total}")
    total_esperado = len(cargar_celdas_l_spec()) * len(VARIANTES) * K_CORRIDAS_SELLADO
    assert total == total_esperado, f"total {total} != {total_esperado} esperado"
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modo = parser.add_mutually_exclusive_group(required=True)
    modo.add_argument("--dry-run", action="store_true", help="Único modo que este acto ejerce -- no invoca `claude`.")
    modo.add_argument("--correr", action="store_true", help="Modo real, no ejercido por este acto. Invoca `claude -p` por corrida.")
    args = parser.parse_args()
    if args.dry_run:
        return dry_run()
    return correr()


if __name__ == "__main__":
    raise SystemExit(main())
