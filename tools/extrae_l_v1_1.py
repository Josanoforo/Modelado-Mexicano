#!/usr/bin/env python3
"""Extractor congelado de `valor_extraido` para las 176 capturas de
`corridas-L/*-M-*.json` (marco-M v1_1).

ACTO: MAESTRA33-E21 · L-EXTRAE-v1_1 (nube). Aplica, SIN CAMBIARLA, la regla
sellada en `forense/prereg-duelo-v2/regla-extraccion-L-v1_1.md` (P1,
COMMIT-1 del acto). Este script es el P2 del mismo acto.

*** Este script NO edita ninguna captura. *** Solo lee `corridas-L/*.json`
y escribe `forense/prereg-duelo-v2/L-extraido-v1_1.tsv`. No llama a ningún
modelo. No re-corre L.

Uso:
    python3 tools/extrae_l_v1_1.py
        -- aplica la regla a las 176 capturas `*-M-*.json`, escribe el TSV,
           imprime (y deja en el TSV de log) el conteo de NO-EXTRAIBLE por
           variante (A.13).
    python3 tools/extrae_l_v1_1.py --regresion
        -- aplica la MISMA regla a las 8 capturas del piloto CIV-08
           (que ya traen `valor_extraido` puesto a mano/por el criterio del
           ejecutor original) y compara. No escribe el TSV principal.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR_PAQUETE = ROOT / "forense" / "prereg-duelo-v2"
CORRIDAS_L = DIR_PAQUETE / "corridas-L"
SALIDA_TSV = DIR_PAQUETE / "L-extraido-v1_1.tsv"
LOG_CIERRE = DIR_PAQUETE / "L-extraido-v1_1-notas-cierre.md"

# ENMIENDA 4 (3/sep/2026, contra 68742de; ADR-282, precedente N4 firma DL-(1)):
# única edición autorizada a este script. `CELDAS_ESPERADAS` es la constante
# de módulo que sustituye al literal `176` de la línea de aserción de abajo
# (176 == 11 celdas * 2 variantes * 8 corridas, para la corrida sellada
# v1_1). Las cuatro constantes de este bloque (`CORRIDAS_L`, `SALIDA_TSV`,
# `LOG_CIERRE`, `CELDAS_ESPERADAS`) son las que un llamador externo
# sobreescribe en runtime, patrón `PAQUETE-L-v1_2.md` §4 (mismo mecanismo
# usado ahí para `runner_l_cli.py` / `carga_l_v1_1.L_SPEC_JSON`): importar
# este módulo por ruta, asignar los atributos de módulo, y solo entonces
# llamar a `procesar_176()`. Nada más de este archivo se edita.
CELDAS_ESPERADAS = 11

# --- patrones de la regla congelada (regla-extraccion-L-v1_1.md, paso 3) ---
_NUM = r"\d{1,3}(?:\.\d+)?"
RE_ENCABEZADO = re.compile(r"^(#+)\s*(.+?)\s*$", re.MULTILINE)
RE_RANGO_PCT = re.compile(rf"({_NUM})\s*%?\s*[-–—]\s*({_NUM})\s*%")
RE_PCT_SIMPLE = re.compile(rf"(?:[≈~]\s*)?({_NUM})\s*%")
RE_DECIMAL01 = re.compile(rf"(0\.\d+)(?!\s*%)")


def _sin_acentos(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def _localizar_seccion(texto: str) -> str:
    """Paso 1-2 de la regla: encabezado que contenga 'estimaci', delimitado
    por el siguiente encabezado del mismo nivel o superior; si no hay tal
    encabezado, el documento completo (fallback declarado en la regla)."""
    encabezados = list(RE_ENCABEZADO.finditer(texto))
    for i, m in enumerate(encabezados):
        nivel, titulo = m.group(1), m.group(2)
        if "estimaci" in _sin_acentos(titulo).lower():
            inicio = m.end()
            fin = len(texto)
            for m2 in encabezados[i + 1 :]:
                if len(m2.group(1)) <= len(nivel):
                    fin = m2.start()
                    break
            return texto[inicio:fin]
    return texto


@dataclass
class Extraccion:
    valor: float | None
    estado: str  # "EXTRAIBLE" | "NO-EXTRAIBLE"
    fragmento_citado: str


def extraer_valor(texto_crudo: str) -> Extraccion:
    seccion = _localizar_seccion(texto_crudo)

    candidatos: list[tuple[int, float, str]] = []  # (posicion, valor[0,1], fragmento)

    m = RE_RANGO_PCT.search(seccion)
    if m:
        a, b = float(m.group(1)), float(m.group(2))
        candidatos.append((m.start(), ((a + b) / 2.0) / 100.0, m.group(0)))

    m = RE_PCT_SIMPLE.search(seccion)
    if m:
        candidatos.append((m.start(), float(m.group(1)) / 100.0, m.group(0)))

    m = RE_DECIMAL01.search(seccion)
    if m:
        candidatos.append((m.start(), float(m.group(1)), m.group(0)))

    if not candidatos:
        return Extraccion(None, "NO-EXTRAIBLE", "")

    candidatos.sort(key=lambda t: t[0])
    _, valor, fragmento = candidatos[0]
    return Extraccion(valor, "EXTRAIBLE", fragmento.strip())


def _fragmento_tsv(frag: str) -> str:
    return frag.replace("\t", " ").replace("\n", " ").strip()


def procesar_176() -> int:
    rutas = sorted(CORRIDAS_L.glob("*-M-*.json"))
    filas: list[tuple[str, str, str, str, str, str]] = []
    conteo_no_extraible = {"L-solo": 0, "L+corpus": 0}
    conteo_extraible = {"L-solo": 0, "L+corpus": 0}

    for ruta in rutas:
        with ruta.open(encoding="utf-8") as fh:
            datos = json.load(fh)
        id_celda = datos["id_celda"]
        variante = datos["variante"]
        indice = datos["indice"]
        ext = extraer_valor(datos["texto_crudo"])
        if ext.estado == "NO-EXTRAIBLE":
            conteo_no_extraible[variante] = conteo_no_extraible.get(variante, 0) + 1
        else:
            conteo_extraible[variante] = conteo_extraible.get(variante, 0) + 1
        filas.append(
            (
                id_celda,
                variante,
                str(indice),
                "" if ext.valor is None else f"{ext.valor:.4f}",
                ext.estado,
                _fragmento_tsv(ext.fragmento_citado),
            )
        )

    _esperadas = CELDAS_ESPERADAS * 2 * 8
    assert len(rutas) == _esperadas, f"esperaba {_esperadas} capturas *-M-*.json, encontré {len(rutas)}"

    with SALIDA_TSV.open("w", encoding="utf-8") as fh:
        fh.write("id_celda\tvariante\tindice\tvalor\testado\tfragmento_citado\n")
        for fila in filas:
            fh.write("\t".join(fila) + "\n")

    total_no_extraible = sum(conteo_no_extraible.values())
    reporte = [
        f"OK -- {len(rutas)} capturas examinadas (censo exhaustivo, A.13), 0 editadas.",
        f"OK -- TSV escrito en {SALIDA_TSV.relative_to(ROOT)}",
        "Conteo NO-EXTRAIBLE por variante (A.13):",
        f"  L-solo:    {conteo_no_extraible.get('L-solo', 0)} NO-EXTRAIBLE / {conteo_no_extraible.get('L-solo', 0) + conteo_extraible.get('L-solo', 0)} examinadas",
        f"  L+corpus:  {conteo_no_extraible.get('L+corpus', 0)} NO-EXTRAIBLE / {conteo_no_extraible.get('L+corpus', 0) + conteo_extraible.get('L+corpus', 0)} examinadas",
        f"  total NO-EXTRAIBLE: {total_no_extraible} / {len(rutas)}",
    ]
    for linea in reporte:
        print(linea)

    with LOG_CIERRE.open("w", encoding="utf-8") as fh:
        fh.write("# Notas de cierre -- tools/extrae_l_v1_1.py (P2, A.13)\n\n")
        fh.write("Corrida real sobre las 176 capturas `corridas-L/*-M-*.json`.\n\n")
        for linea in reporte:
            fh.write(f"- {linea}\n")
        fh.write("\nVer regresión CIV-08 con `python3 tools/extrae_l_v1_1.py --regresion`.\n")

    return 0


def regresion_civ08() -> int:
    """Aplica la misma regla a las 8 capturas del piloto CIV-08 (todas
    L-solo) y compara contra su `valor_extraido` ya puesto. Declara
    explícitamente las diferencias de criterio/unidad -- no las oculta."""
    rutas = sorted(CORRIDAS_L.glob("CIV-08__*.json"))
    assert rutas, "no encontré capturas de piloto CIV-08"

    print(f"Regresión sobre {len(rutas)} capturas de piloto CIV-08 (A.13: {len(rutas)} examinadas)")
    print(f"{'archivo':40s} {'piloto':>10s} {'regla(x100)':>12s} {'regla_raw':>10s} {'coincide?':>10s}")

    n_coincide = 0
    n_diverge_valor = 0
    n_piloto_none_regla_no = 0
    for ruta in rutas:
        with ruta.open(encoding="utf-8") as fh:
            datos = json.load(fh)
        piloto = datos.get("valor_extraido")
        ext = extraer_valor(datos["texto_crudo"])
        # El piloto guardó las cifras en escala porcentual (61.0, 23.5), no
        # en [0,1] -- la regla congelada (paso 6) normaliza a [0,1]. Para
        # comparar como el criterio del piloto, multiplicamos x100.
        regla_pct = None if ext.valor is None else round(ext.valor * 100.0, 1)
        coincide = (
            piloto is None and ext.estado == "NO-EXTRAIBLE"
        ) or (
            piloto is not None and regla_pct is not None and abs(piloto - regla_pct) < 0.05
        )
        if coincide:
            n_coincide += 1
        elif piloto is None:
            n_piloto_none_regla_no += 1
        else:
            n_diverge_valor += 1
        print(
            f"{ruta.name:40s} {str(piloto):>10s} {str(regla_pct):>12s} "
            f"{'' if ext.valor is None else f'{ext.valor:.4f}':>10s} {'SI' if coincide else 'NO':>10s}"
        )

    print()
    print(f"Coinciden (mismo NO-EXTRAIBLE, o mismo valor tras x100): {n_coincide}/{len(rutas)}")
    print(f"Divergen en valor: {n_diverge_valor}/{len(rutas)}")
    print(f"Piloto NO-DISPONIBLE, regla SI extrae (o viceversa): {n_piloto_none_regla_no}/{len(rutas)}")
    print()
    print(
        "Declaración honesta de por qué NO se fuerza la coincidencia (encargo P2):\n"
        "1. UNIDAD: el piloto guardó valor_extraido en escala porcentual sin dividir\n"
        "   (61.0, 23.5), no en [0,1]. La regla congelada normaliza a [0,1] (regla-\n"
        "   extraccion-L-v1_1.md paso 6) -- por eso la comparación de arriba multiplica\n"
        "   por 100 antes de comparar, y el TSV real (P2, corrida sobre las 176) queda\n"
        "   en [0,1], NO en la unidad del piloto.\n"
        "2. CRITERIO DE SELECCION: el piloto (CIV-08 indice 1, valor 61.0) no tomó el\n"
        "   primer número que aparece en el texto -- el primer número por posición ahí\n"
        "   es el rango del reactivo específico ('67-73%', mercado), y el piloto en\n"
        "   cambio eligió una cifra posterior, etiquetada por el propio texto como\n"
        "   'dato público de INEGI' (más autoritativa) sobre la percepción general.\n"
        "   La regla congelada de este acto NO pondera fuente/autoridad (regla paso 7,\n"
        "   declarado explícitamente antes de correrla) -- toma el primer número por\n"
        "   posición, sin ese juicio. Esta es la causa de la divergencia en el indice 1,\n"
        "   no un error del extractor: es la consecuencia declarada de congelar una\n"
        "   regla mecánica en vez de repetir el juicio humano/de modelo del piloto."
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--regresion", action="store_true",
        help="Corre la regla sobre las 8 capturas de piloto CIV-08 y compara contra su valor_extraido ya puesto, en vez de procesar las 176.",
    )
    args = parser.parse_args()
    if args.regresion:
        return regresion_civ08()
    return procesar_176()


if __name__ == "__main__":
    raise SystemExit(main())
