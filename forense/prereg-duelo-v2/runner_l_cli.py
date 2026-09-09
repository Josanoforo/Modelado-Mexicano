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

ENMIENDA F5 (firma de mesa 9/sep/2026, ACTO GEN2-F5-RECAPTURA-L, P1 -- ver
tabla de re-sellado al pie de este docstring): tres invariantes que el
runner heredado no traía y que P1(a)/(d) de ese encargo exige, ninguno
ejercido por este acto (sigue siendo CONTADOR: cero, `--dry-run` no invoca
`claude`):
    contexto L+corpus  = ensamblado real desde el paquete-corpus congelado
                          (`paquete-corpus-F5-v1_0/manifiesto.json`), por
                          celda, con el corte temporal de esa celda ya
                          aplicado por construcción -- reemplaza el
                          placeholder literal "[contexto tierizado -- no
                          construido en este acto]" que este runner traía
                          desde MAESTRA33-E17. Specs sin paquete-corpus
                          (v1_1/v1_2) caen al placeholder histórico, sin
                          romper la regresión.
    orden de captura   = permutación determinista de las 224 tuplas
                          (`orden_captura()`, semilla 42 -- reutiliza el
                          seed ya sellado de `scoring-adv1-m3.py`/FP-168),
                          contrabalanceada entre variantes en vez de
                          "todas L-solo, luego todas L+corpus"
    reintentos         = hasta 2 por captura (`MAX_REINTENTOS`), contados
                          en el registro (`intentos`); agotados, la captura
                          se escribe como `RECHAZADO_TRAS_REINTENTOS` en vez
                          de tumbar el lote completo con una excepción

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
import random
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

# D3 (firma de mesa 3/sep/2026, propagado por ACTO MAESTRA37-N8 ·
# CONSOLIDA-DECISIONES): corrección hacia adelante -- las corridas nuevas
# (v1_3 en adelante) llevan `__<SPEC_VERSION>` en el nombre de archivo, para
# poder distinguir, por nombre, qué spec de prereg las gobernó sin abrir el
# JSON. Las 424 capturas existentes (v1_1/v1_2) NO se re-nombran ni
# re-corren -- ver la línea nueva en el registro sellado de corridas L
# (README de esta carpeta).
SPEC_VERSION = "v1_3"

# --------------------------------------------------------------------------
# ENMIENDA F5 (firma de mesa 9/sep/2026, ACTO GEN2-F5-RECAPTURA-L, P1):
# tres invariantes que P1(a)/(d) exige y que el runner heredado no traía --
# ninguno cambia el comportamiento ya sellado para L-solo ni para specs
# anteriores a v1_3, verificado por regresión (--dry-run con L-spec-v1_1.json
# y L-spec-v1_2.json en verde, sin cambio de conteo). Hash antes de esta
# enmienda: `b2c3965851423d07f164d11da914972742924e70bfb5f9f71cc8f70ad5aeb7e3`
# (P4/D3, commit e8a95d0, FP-235/FP-240) -- ver tabla de re-sellado al pie
# de este archivo (docstring de módulo la referencia, no se retranscribe
# aquí para no duplicar la fuente de verdad).
# --------------------------------------------------------------------------

# (1) Paquete-corpus real, en vez del placeholder literal que `_iter_plan()`
# traía para L+corpus ("[contexto tierizado -- no construido en este acto]").
# Directorio congelado en el mismo COMMIT-1 que esta enmienda; manifiesto.json
# mapea id_celda -> lista de documentos permitidos por el corte temporal de
# esa celda (P1(a)), cada uno con su sha256 individual.
PAQUETE_CORPUS_DIR = DIR / "paquete-corpus-F5-v1_0"
PAQUETE_CORPUS_MANIFIESTO = PAQUETE_CORPUS_DIR / "manifiesto.json"
# Presupuesto de caracteres del contexto ensamblado por invocación L+corpus.
# Declarado, no medido contra un límite real del cliente CLI (que no expone
# uno) -- conservador frente a una ventana de contexto de ~200k tokens
# (~800k caracteres) dejando margen para el prompt de celda, el system-prompt
# y la respuesta. Truncamiento determinista: orden alfabético de ruta,
# se trunca el último documento que no cabe completo, el corte se declara
# en los metadatos de la captura -- nunca en silencio (PLAN-DE-OBRA-GEN2-v1_1
# F5: "«acceso al corpus» no promete que todos sus bytes quepan en contexto").
MAX_CHARS_CONTEXTO_CORPUS = 600_000


def cargar_contexto_corpus(id_celda: str) -> tuple[str, dict]:
    """Ensambla el contexto documental para la variante L+corpus de una
    celda, desde el paquete-corpus congelado en P1 -- nunca desde `corpus/`
    directamente (la sesión ejecutora de D-iii tampoco tendría ese acceso;
    este runner replica, en la caja, exactamente lo que P2 blinda). Si la
    celda no tiene entrada en el manifiesto (specs anteriores a v1_3, que no
    tienen paquete-corpus construido -- CIV-M-06/08/09/11, TRA-M-05 de
    v1_1/v1_2), cae al placeholder histórico sin romper la regresión, con la
    razón declarada en los metadatos en vez de fallar en silencio."""
    if not PAQUETE_CORPUS_MANIFIESTO.exists():
        return (
            "[contexto tierizado -- no construido en este acto]",
            {"estado": "SIN_PAQUETE_CORPUS", "razon": "manifiesto.json ausente"},
        )
    manifiesto = json.loads(PAQUETE_CORPUS_MANIFIESTO.read_text(encoding="utf-8"))
    entrada = manifiesto.get("celdas", {}).get(id_celda)
    if entrada is None:
        return (
            "[contexto tierizado -- no construido en este acto]",
            {"estado": "SIN_PAQUETE_CORPUS", "razon": f"{id_celda} no está en manifiesto.json (spec no cubierta por F5)"},
        )
    documentos = sorted(entrada["documentos_incluidos"])  # orden determinista, alfabético por ruta
    partes: list[str] = []
    chars_acumulados = 0
    documentos_leidos: list[str] = []
    truncado_en: str | None = None
    for ruta_rel in documentos:
        ruta_abs = PAQUETE_CORPUS_DIR / ruta_rel
        texto_doc = ruta_abs.read_text(encoding="utf-8")
        cabecera = f"\n\n=== {ruta_rel} ===\n\n"
        bloque = cabecera + texto_doc
        if chars_acumulados + len(bloque) > MAX_CHARS_CONTEXTO_CORPUS:
            restante = MAX_CHARS_CONTEXTO_CORPUS - chars_acumulados
            if restante > len(cabecera):
                partes.append(bloque[:restante])
                documentos_leidos.append(ruta_rel)
            truncado_en = ruta_rel
            break
        partes.append(bloque)
        documentos_leidos.append(ruta_rel)
        chars_acumulados += len(bloque)
    texto_final = "".join(partes)
    metadata = {
        "estado": "OK",
        "id_celda": id_celda,
        "corte_temporal": entrada.get("corte_temporal"),
        "documentos_disponibles": len(documentos),
        "documentos_incluidos": documentos_leidos,
        "documentos_excluidos": entrada.get("documentos_excluidos", []),
        "chars_incluidos": len(texto_final),
        "truncado": truncado_en is not None,
        "truncado_en_documento": truncado_en,
    }
    return texto_final, metadata


# (2) Orden de captura contrabalanceado, semilla declarada (P1(d)). Reutiliza
# seed=42 -- la misma semilla ya sellada en todo bootstrap de
# scoring-adv1-m3.py (FP-168) -- para un propósito distinto pero análogo
# (determinismo declarado, no una segunda semilla arbitraria).
SEMILLA_ORDEN = 42


def orden_captura(tuplas: list) -> list:
    """Permutación determinista de las tuplas de `_iter_plan()`: ni todas las
    L-solo antes que todas las L+corpus, ni celda por celda en el orden del
    marco. `random.Random(SEMILLA_ORDEN).shuffle()` sobre una copia -- la
    misma lista de entrada produce, siempre, la misma salida."""
    barajada = list(tuplas)
    random.Random(SEMILLA_ORDEN).shuffle(barajada)
    return barajada


# (3) Reintentos acotados y contados (P1(d)) -- `ejecutar_corrida()` ya no
# deja que una sola invocación fallida tumbe las 224. Hasta MAX_REINTENTOS
# reintentos por captura (MAX_REINTENTOS+1 intentos totales); agotados, la
# captura se declara RECHAZADO_TRAS_REINTENTOS y se escribe igual -- no se
# pierde la fila, el embudo de P3 la cuenta como rechazo, no como silencio.
MAX_REINTENTOS = 2


def ruta_salida(id_celda: str, variante: str, indice: int) -> Path:
    """corridas-L/L-<id>-M__<variante>__<k>__<spec>.json -- misma
    convención de nombres que `carga_l_v1_1.py::ruta_salida` (prefijo L-,
    sufijo -M para no colisionar con las 120 capturas del marco piloto),
    con el sufijo `__<SPEC_VERSION>` añadido por D3 para las corridas
    nuevas que este script ejecute de aquí en adelante. No se importa esa
    función directamente porque este runner escribe archivos reales (el
    dry-run del cargador nunca escribe) -- se replica la misma expresión."""
    return DIR / "corridas-L" / f"L-{id_celda}-M__{variante}__{indice:02d}__{SPEC_VERSION}.json"


def construir_comando_cli() -> list[str]:
    """Comando exacto que P2 fija, uno por corrida. `--tools ""` deshabilita
    herramientas; `--max-turns 1` fuerza una sola vuelta ciega; el prompt de
    sistema por defecto del CLI se reemplaza, no se agrega.

    ENMIENDA F5-2 (9/sep/2026, medida en P3, no supuesta): el prompt YA NO se
    pasa como argumento posicional -- `subprocess.run(..., input=prompt)` lo
    entrega por stdin (`claude -p` lo lee cuando no recibe `[prompt]`,
    verificado empíricamente antes de aplicar el cambio). Defecto real: con
    contexto de paquete-corpus (hasta 600 000 caracteres), el argumento
    excedía el límite por-argumento de `execve` en Linux (`MAX_ARG_STRLEN`,
    ~128 KiB) -- `OSError: [Errno 7] Argument list too long`, medido en la
    primera invocación `L+corpus` real de P3 (4 capturas `L-solo` ya habían
    corrido bien, sin contexto, sin tocar este límite). El comando de línea
    ya no depende del tamaño del prompt."""
    return [
        "claude", "-p",
        "--model", MODELO_ALIAS,
        "--output-format", "json",
        "--system-prompt", SISTEMA_MINIMO,
        "--tools", "",
        "--max-turns", "1",
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


def ejecutar_corrida(spec, params_variante: str, prompt: str, id_celda: str, indice: int, params, contexto_metadata: dict | None = None) -> dict:
    """`sha256_prompt` es el sha256 del prompt EXACTO que se envía (el último
    argumento de `construir_comando_cli`, hasheado utf-8) y `params` es lo que
    `construir_params` devuelve, serializado. Las dos claves restauran el
    esquema de 9 que `carga_l_v1_1.py:130` valida y que la corrida v1_1 perdió
    -- sin ellas, una captura no lleva prueba propia de con qué prompt nació
    (defecto medido el 2/sep sobre las 176 de v1_1: K=96). Firma DL-(1).

    ENMIENDA F5: hasta `MAX_REINTENTOS` reintentos si el subproceso falla o
    la salida no parsea -- cada intento contado (`intentos`). Agotados los
    reintentos, NO se levanta excepción: se devuelve un registro con
    `estado_captura=RECHAZADO_TRAS_REINTENTOS` para que `correr()` siga con
    la siguiente tupla y el embudo de P3 cuente el rechazo en vez de perder
    la fila o tumbar el lote completo."""
    comando = construir_comando_cli()
    sha_prompt = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    ultimo_error: str | None = None
    for intento in range(1, MAX_REINTENTOS + 2):
        try:
            resultado = subprocess.run(comando, input=prompt, capture_output=True, text=True, check=True, timeout=180)
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
                "sha256_prompt": sha_prompt,
                "intentos": intento,
                "estado_captura": "OK",
                "contexto_corpus_metadata": contexto_metadata,
            }
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
            ultimo_error = f"{type(exc).__name__}: {exc}"
            continue
    return {
        "id_celda": id_celda,
        "variante": params_variante,
        "indice": indice,
        "texto_crudo": None,
        "valor_extraido": None,
        "fuente_citada": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "modelo_real": None,
        "params": asdict(params),
        "sha256_prompt": sha_prompt,
        "intentos": MAX_REINTENTOS + 1,
        "estado_captura": "RECHAZADO_TRAS_REINTENTOS",
        "error_declarado": ultimo_error,
        "contexto_corpus_metadata": contexto_metadata,
    }


def _iter_plan():
    """Genera (celda, spec, variante, indice, prompt, ruta, params,
    contexto_metadata) para las N celdas x 2 variantes x k=8 -- mismo
    recorrido para --dry-run y --correr, así el conteo y el esquema que
    valida uno son los que el otro ejecuta.

    ENMIENDA F5: el contexto de L+corpus ya no es el placeholder literal --
    se ensambla desde `cargar_contexto_corpus()` (paquete-corpus congelado
    en P1). `contexto_metadata` viaja hasta `ejecutar_corrida()` para que
    quede en el registro de cada captura (qué documentos entraron, si hubo
    truncamiento)."""
    celdas = cargar_celdas_l_spec()
    for celda in celdas:
        spec = celda_a_spec(celda)
        for variante in VARIANTES:
            if variante == "L-solo":
                contexto_corpus, contexto_metadata = "", None
            else:
                contexto_corpus, contexto_metadata = cargar_contexto_corpus(celda["id"])
            params = _CARGA.construir_params(variante, "paquete-corpus-F5-v1_0" if variante == "L+corpus" else None)
            prompt = construir_prompt(spec, params, contexto_corpus)
            for indice in range(1, K_CORRIDAS_SELLADO + 1):
                ruta = ruta_salida(celda["id"], variante, indice)
                yield celda, spec, variante, indice, prompt, ruta, params, contexto_metadata


def dry_run() -> int:
    n_rutas = 0
    n_prompts_vistos = set()
    rutas_vistas: set[Path] = set()

    ejemplos = sorted((DIR / "corridas-L").glob("CIV-08__L-solo__*.json"))
    assert ejemplos, "no encontré ningún ejemplo en corridas-L/ para verificar esquema"
    ejemplo = json.loads(ejemplos[0].read_text(encoding="utf-8"))
    claves_piloto = {"id_celda", "variante", "indice", "texto_crudo", "valor_extraido", "fuente_citada", "timestamp", "params", "sha256_prompt"}
    assert claves_piloto.issubset(ejemplo.keys()), f"esquema de ejemplo no trae las claves esperadas: {claves_piloto - ejemplo.keys()}"

    contexto_corpus_ok = 0
    contexto_corpus_sin_paquete = 0
    for celda, spec, variante, indice, prompt, ruta, _params, contexto_metadata in _iter_plan():
        assert prompt, f"prompt vacío para {celda['id']}/{variante}"
        n_prompts_vistos.add((celda["id"], variante))
        assert ruta not in rutas_vistas, f"ruta colisionada: {ruta}"
        rutas_vistas.add(ruta)
        comando = construir_comando_cli()
        assert comando[0] == "claude" and "-p" in comando
        assert "--tools" in comando and comando[comando.index("--tools") + 1] == ""
        assert SISTEMA_MINIMO in comando
        assert prompt not in comando, "el prompt NO debe viajar en argv (ENMIENDA F5-2, arg-list-too-long)"
        if variante == "L+corpus":
            assert contexto_metadata is not None, f"L+corpus sin contexto_metadata para {celda['id']}"
            if contexto_metadata.get("estado") == "OK":
                contexto_corpus_ok += 1
            else:
                contexto_corpus_sin_paquete += 1
        n_rutas += 1

    n_celdas = len(cargar_celdas_l_spec())
    total_esperado = n_celdas * len(VARIANTES) * K_CORRIDAS_SELLADO
    assert n_rutas == total_esperado, f"{n_rutas} rutas construidas, esperaba {total_esperado}"

    # ENMIENDA F5: orden contrabalanceado -- verifica que la permutación
    # sellada (SEMILLA_ORDEN) es determinista y cubre exactamente el mismo
    # conjunto de tuplas que _iter_plan() produce, sin perder ni duplicar
    # ninguna. No invoca `claude` -- solo permuta una lista en memoria.
    plan_lista = list(_iter_plan())
    orden_a = orden_captura(plan_lista)
    orden_b = orden_captura(plan_lista)
    assert [t[5] for t in orden_a] == [t[5] for t in orden_b], "orden_captura() no es determinista"
    assert {t[5] for t in orden_a} == {t[5] for t in plan_lista}, "orden_captura() perdió o duplicó una ruta"
    assert len(orden_a) == total_esperado

    print(f"OK -- {len(n_prompts_vistos)} pares (celda, variante) x k={K_CORRIDAS_SELLADO} = {n_rutas} rutas de salida verificadas")
    print(f"OK -- esquema de salida (campos del piloto) verificado contra {ejemplos[0].name}")
    print(f"OK -- comando CLI construido para las {n_rutas} corridas: claude -p --model {MODELO_ALIAS} --output-format json --system-prompt '<P1>' --tools '' --max-turns 1  (prompt por stdin, ENMIENDA F5-2)")
    print(f"OK -- contexto_corpus real para {contexto_corpus_ok} invocaciones L+corpus; {contexto_corpus_sin_paquete} sin paquete-corpus (spec no cubierta por F5, placeholder declarado)")
    print(f"OK -- orden_captura() determinista (semilla={SEMILLA_ORDEN}), cubre las {total_esperado} tuplas sin pérdida ni duplicado")
    print("OK -- ningún subproceso `claude` invocado en este acto (--dry-run)")
    primer_celda, _, primera_variante, _, _, primera_ruta, _, _ = next(_iter_plan())
    print(f"Ejemplo de ruta: {primera_ruta.relative_to(ROOT)}")
    print(f"Total esperado: {total_esperado}")
    return 0


def correr() -> int:
    """MODO REAL -- no ejercido por este acto (CONTADOR: cero). Reanudable:
    salta cualquier (celda, variante, indice) cuyo archivo de salida ya
    exista, para que un corte por límite horario no repita lo ya hecho.

    ENMIENDA F5: (1) recorre las tuplas en el orden contrabalanceado de
    `orden_captura()`, no en el orden natural celda-por-celda; (2) una
    captura rechazada tras agotar reintentos (`ejecutar_corrida` ya no
    levanta excepción) NO detiene el lote -- se escribe igual, con su
    `estado_captura` declarado, y se cuenta aparte en el embudo; (3) el
    embudo final reporta éxitos/rechazos/reanudadas por separado, sobre TODO
    el marco -- no solo sobre las celdas donde un brazo tuvo éxito (P3 lo
    exige explícitamente: cobertura sobre el marco completo, no solo sobre
    los éxitos)."""
    n_hechas = 0
    n_saltadas = 0
    n_rechazadas = 0
    plan_ordenado = orden_captura(list(_iter_plan()))
    for celda, spec, variante, indice, prompt, ruta, params, contexto_metadata in plan_ordenado:
        if ruta.exists():
            n_saltadas += 1
            continue
        registro = ejecutar_corrida(spec, variante, prompt, celda["id"], indice, params, contexto_metadata)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
        if registro.get("estado_captura") == "OK":
            n_hechas += 1
        else:
            n_rechazadas += 1

    total = n_hechas + n_saltadas + n_rechazadas
    print(f"OK -- {n_hechas} corridas nuevas OK, {n_rechazadas} rechazadas tras {MAX_REINTENTOS + 1} intentos, {n_saltadas} ya existentes (reanudación), total {total}")
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
