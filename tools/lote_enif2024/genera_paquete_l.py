#!/usr/bin/env python3
"""Genera el paquete L FINAL del lote ENIF 2024: los prompts por celda, a
partir de la PLANTILLA de `PAQUETE-L-LOTE-ENIF2024-v0_1.md` (importada, no
copiada: se leen sus dos bloques de código), la REJILLA de `spec.yaml` (leída
del árbitro) y los MARGINALES SELLADOS de `#971` (citados por id de RESULT).
**Ningún prompt por celda se redacta a mano.**

ACTO `GEN2-DIN-LOTE-ENIF2024-COMMIT-1`. Uso:
    python3 tools/lote_enif2024/genera_paquete_l.py [--escribe]
Escribe `forense/prereg-duelo-v2/paquete-l-lote-enif2024-v1_0/prompts.jsonl`
(44 celdas × 2 variantes = 88 prompts; mesa repite cada uno k = 8 veces) y
`forense/prereg-duelo-v2/PAQUETE-L-LOTE-ENIF2024-v1_0.md`. No corre nada.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[2]
PLANTILLA = RAIZ / "forense" / "prereg-duelo-v2" / "PAQUETE-L-LOTE-ENIF2024-v0_1.md"
SPEC_YAML = RAIZ / "data" / "corrida0" / "CALC-DIN-LOTE-ENIF2024-EMISIONES-0001" / "spec.yaml"
CALC_971 = RAIZ / "data" / "corrida0" / "CALC-ARBITRO-MARGINALES-ENIF2024-0001" / "resultados.json"
SALIDA_DIR = RAIZ / "forense" / "prereg-duelo-v2" / "paquete-l-lote-enif2024-v1_0"
SALIDA_MD = RAIZ / "forense" / "prereg-duelo-v2" / "PAQUETE-L-LOTE-ENIF2024-v1_0.md"

# Etiquetas en castellano llano para el prompt (la rejilla y su orden vienen
# del árbitro; aquí sólo se escribe cómo se lee cada categoría).
EJE_TXT = {"sexo": "sexo", "edad": "edad", "escolaridad": "escolaridad",
           "localidad": "tamaño de localidad", "formalidad": "formalidad laboral",
           "cuenta_formal": "tenencia de cuenta formal"}
CAT_TXT = {"1 Hombre": "hombre", "2 Mujer": "mujer",
           "18-29": "18 a 29 años", "30-44": "30 a 44 años", "45-59": "45 a 59 años", "60+": "60 años y más",
           "hasta primaria": "hasta primaria (ninguno, preescolar o primaria)",
           "secundaria": "secundaria",
           "media superior": "media superior (preparatoria, bachillerato, normal básica o estudios técnicos)",
           "superior": "superior (licenciatura, especialidad, maestría o doctorado)",
           "menor de 15 000": "localidades de menos de 15 000 habitantes",
           "15 000 y mas": "localidades de 15 000 habitantes y más"}


def _slug(s):
    t = "".join(ch if ch.isalnum() else "-" for ch in str(s).upper())
    while "--" in t:
        t = t.replace("--", "-")
    return t.strip("-")


def bloques_de_la_plantilla() -> tuple:
    texto = PLANTILLA.read_text(encoding="utf-8")
    bloques = re.findall(r"```[a-z]*\n(.*?)```", texto, flags=re.S)
    if len(bloques) != 3:
        raise SystemExit(f"la plantilla trae {len(bloques)} bloques; se esperaban L1, CONTEXTO y el formato de captura")
    return bloques[0].rstrip("\n"), bloques[1].rstrip("\n")


def _pct(p: float) -> str:
    return f"{100.0 * float(p):.1f} %"


def prompts() -> list:
    spec = yaml.safe_load(SPEC_YAML.read_text(encoding="utf-8"))
    par = spec["parametros"]
    res = json.loads(CALC_971.read_text(encoding="utf-8"))["resultados"]
    ids = par["marginales_sellados"]["puntos"]["ids"]
    nac_id = par["marginales_sellados"]["puntos"]["nacional_id"]
    l1, contexto = bloques_de_la_plantilla()
    out = []
    for nombre, p in par["pares"].items():
        if p["grupo"] != par["grupo_primario"]:
            continue
        ea, eb = p["a"], p["b"]
        for ca in par["ejes"][ea]["orden"]:
            for cb in par["ejes"][eb]["orden"]:
                celda_id = f"{_slug(nombre)}-{_slug(ca)}-X-{_slug(cb)}"
                sust = {"«eje_A»": EJE_TXT[ea], "«categoría_A»": CAT_TXT[ca],
                        "«eje_B»": EJE_TXT[eb], "«categoría_B»": CAT_TXT[cb], "«celda_id»": celda_id}
                base = l1
                for k, v in sust.items():
                    base = base.replace(k, v)
                out.append({"celda_id": celda_id, "variante": "L1", "par": nombre, "eje_a": ea, "cat_a": ca,
                            "eje_b": eb, "cat_b": cb, "prompt": base,
                            "prompt_sha256": hashlib.sha256(base.encode("utf-8")).hexdigest(),
                            "marginales_citados": {}})
                otras_a = " — ".join(f"{EJE_TXT[ea]} = {CAT_TXT[c]}: {_pct(res[ids[ea][c]])}" for c in par["ejes"][ea]["orden"] if c != ca)
                otras_b = " — ".join(f"{EJE_TXT[eb]} = {CAT_TXT[c]}: {_pct(res[ids[eb][c]])}" for c in par["ejes"][eb]["orden"] if c != cb)
                ctx = contexto
                ctx = ctx.replace("«eje_A» = «categoría_A»: «p_A» — «eje_A» = «otras categorías del eje A con su p»",
                                  f"{EJE_TXT[ea]} = {CAT_TXT[ca]}: {_pct(res[ids[ea][ca]])} — {otras_a}")
                ctx = ctx.replace("«eje_B» = «categoría_B»: «p_B» — «eje_B» = «otras categorías del eje B con su p»",
                                  f"{EJE_TXT[eb]} = {CAT_TXT[cb]}: {_pct(res[ids[eb][cb]])} — {otras_b}")
                ctx = ctx.replace("Nacional: «p».", f"Nacional: {_pct(res[nac_id])}.")
                if "«" in ctx:
                    raise SystemExit("CONTEXTO con campo sin sustituir")
                l2 = base.replace("\nCELDA.", "\n" + ctx + "\n\nCELDA.", 1)
                if "«" in l2:
                    raise SystemExit("L2 con campo sin sustituir")
                citados = {f"{ea}|{c}": ids[ea][c] for c in par["ejes"][ea]["orden"]}
                citados.update({f"{eb}|{c}": ids[eb][c] for c in par["ejes"][eb]["orden"]})
                citados["nacional"] = nac_id
                out.append({"celda_id": celda_id, "variante": "L2", "par": nombre, "eje_a": ea, "cat_a": ca,
                            "eje_b": eb, "cat_b": cb, "prompt": l2,
                            "prompt_sha256": hashlib.sha256(l2.encode("utf-8")).hexdigest(),
                            "marginales_citados": citados})
    return out


def documento(filas: list, sha_jsonl: str) -> str:
    celdas = [f for f in filas if f["variante"] == "L1"]
    por_par = {}
    for f in celdas:
        por_par.setdefault(f["par"], []).append(f["celda_id"])
    lineas = [
        "# Paquete de la corrida `L` — lote de cruces ENIF 2024, `ahorra_solo_informal` · **v1.0 (FINAL)**", "",
        "**Acto que lo produce:** `ACTO GEN2-DIN-LOTE-ENIF2024-COMMIT-1` · pieza P5 · 21/sep/2026 · CAJA ·",
        "rama `acto/gen2-din-lote-enif2024-commit-1`. **Sucede** a `PAQUETE-L-LOTE-ENIF2024-v0_1.md` (`#967`),",
        "de la que **importa** la plantilla de los prompts (sus bloques de código, verbatim) y hereda sin cambio",
        "§0 (prohibición), §1 (qué se elicita), §4 (k = 8, mediana, modelo fijado al correr), §5 (formato de",
        "captura), §6 (sellado antes del COMMIT-2 mecánico) y §7. **CONTADOR: cero.** Este acto **no corre**",
        "ninguna `L`; mesa la ejecuta por CLI y sin `ANTHROPIC_API_KEY` (FP-228).", "",
        "## Lo que este v1.0 fija y el v0.1 dejaba pendiente", "",
        "- **La rejilla, leída del árbitro** vía `data/corrida0/CALC-DIN-LOTE-ENIF2024-EMISIONES-0001/spec.yaml`",
        "  (`parametros.ejes`, orden del árbitro): 44 celdas de los 5 pares primarios.",
        "- **Los prompts por celda, generados** por `tools/lote_enif2024/genera_paquete_l.py`:",
        f"  `paquete-l-lote-enif2024-v1_0/prompts.jsonl` — **{len(filas)} prompts** (44 celdas × 2 variantes),",
        f"  sha256 `{sha_jsonl}`. Cada línea trae `celda_id`, `variante`, `prompt`, `prompt_sha256` y, en `L2`,",
        "  los ids de RESULT de `CALC-ARBITRO-MARGINALES-ENIF2024-0001` (`#971`) de los marginales citados.",
        "- **`celda_id`** = el mismo rótulo de celda que usan los emisores mecánicos",
        "  (`RESULT-DIN-LOTE24-EM-<celda_id>-…`).",
        "- **Marginales del `CONTEXTO` de `L2`:** los sellados en `#971` (D9, precisión completa), redondeados a",
        "  un decimal de porcentaje en el prompt; el id citado permite reconstruir el número exacto.",
        "- **Agregador:** `tools/agrega_l_v1_0.py` (`#973`, mediana con regla de inválidas fijada antes de",
        "  contar). **`#973` no está en `main` al cerrar este acto**: se cita, no se importa (procedencia tipo 3);",
        "  si no fusiona antes del sello de capturas, mesa decide agregador (spec v1_0 §16, Q3).", "",
        "## Celdas del paquete (44)", "", "| par | celdas (`celda_id`) |", "|---|---|"]
    for par, cs in por_par.items():
        lineas.append(f"| `{par}` ({len(cs)}) | " + " · ".join(f"`{c}`" for c in cs) + " |")
    lineas += ["", "## Cómo se corre (mesa)", "",
               "1. Sesión limpia, fuera del proyecto, sin abrir nada de §0 del v0.1. `L1` y `L2` en sesiones distintas.",
               "2. Por cada línea de `prompts.jsonl`, `k = 8` llamadas idénticas; cada captura al formato de §5 del v0.1",
               "   (`celda_id`, `variante`, `rep`, `p`, `estado_captura`, `modelo`, `version`, `temperatura`,",
               "   `corte_entrenamiento`, `prompt_sha256`, `ts_utc`). Respuesta inválida → `RECHAZO`, se conserva, no",
               "   se reintenta; celda con < 5 válidas → `L-INSUFICIENTE`.",
               "3. Se sellan (sha256 + conteo OK/RECHAZO + mediana por celda y variante) **antes** de que exista",
               "   `CALC-DIN-LOTE-ENIF2024-EMISIONES-0001/sello.json`. El orden del diff es el sello.", "",
               "## Lo que este paquete NO hace", "",
               "No corre las llamadas · no abre microdato · no toca `corridas-R/` ni `corridas-M/` · no adjudica: `L1` y",
               "`L2` son retadores **secundarios** y se rotulan así.", ""]
    return "\n".join(lineas)


def main(argv=None) -> int:
    escribe = "--escribe" in (argv or sys.argv[1:])
    filas = prompts()
    jsonl = "".join(json.dumps(f, ensure_ascii=False) + "\n" for f in filas)
    sha = hashlib.sha256(jsonl.encode("utf-8")).hexdigest()
    doc = documento(filas, sha)
    print(f"{len(filas)} prompts · sha256 prompts.jsonl = {sha}")
    if escribe:
        SALIDA_DIR.mkdir(parents=True, exist_ok=True)
        (SALIDA_DIR / "prompts.jsonl").write_text(jsonl, encoding="utf-8")
        SALIDA_MD.write_text(doc, encoding="utf-8")
        print(f"escrito: {SALIDA_DIR / 'prompts.jsonl'} y {SALIDA_MD}")
    else:
        print(filas[0]["prompt"])
        print("-----")
        print(filas[1]["prompt"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
